"""
Views for the data Django app
"""
import os
import shutil
import time
from typing import List
from pathlib import Path

from django.http import HttpResponse, HttpResponseServerError
from django.views import View
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from common.logging import logger


class ResumableJsUpload(View):
    """
    Class based Django view for handling file/data uploads using ResumableJs
    """
    # Use root '/tmp' if not running code locally, else use '<project_root>/tmp'
    _base_dir_path = Path(settings.BASE_DIR).parent if settings.ON_LOCAL else Path('/')
    FILE_UPLOAD_DIR = _base_dir_path / 'tmp' / 'file_uploads'
    LOG_PREFIX = 'ResumableJS Upload'

    @classmethod
    def target_file_path(cls, plant_name_key: str, uploaded_file_name: str) -> Path:
        """
        Return the path for where the target file will be stored
        """
        return cls.FILE_UPLOAD_DIR / plant_name_key / uploaded_file_name

    def post(self, request) -> HttpResponse:
        """
        Handle post request to write chunks from incoming ResumableJS requests

        If one of the requests notices all the chunks have been fully written
        it will write the full file to
            <self.FILE_UPLOAD_DIR>/<user.plant.name_key>/<uploaded_file_name>
        """
        total_chunks = int(request.POST.get('resumableTotalChunks'))
        chunk_num = int(request.POST.get('resumableChunkNumber', 1))
        uploaded_file_name = request.POST.get('resumableFilename')
        resumable_identifier = request.POST.get('resumableIdentifier', 'error')
        chunk_data = request.FILES['file']
        user = request.user
        plant_name_key = user.plant.name_key

        # Get - tmp file dir path for the ResumableJS upload chunks
        #     - target file path
        target_file_path = self.target_file_path(plant_name_key, uploaded_file_name)
        chunk_dir = self.FILE_UPLOAD_DIR / plant_name_key / resumable_identifier

        # Save this chunk data using a lock file
        self._save_chunk_data(uploaded_file_name, chunk_num,
                              chunk_data, chunk_dir)

        # Check if the all chunk files created in all Resumable JS Requests
        all_chunk_paths = self._all_chunk_paths(uploaded_file_name,
                                                chunk_dir,
                                                total_chunks)

        all_chunks_exists = all([p.exists() for p in all_chunk_paths])
        if all_chunks_exists:

            # Make sure all files are finished writing, but do not wait forever
            tried = 0
            while self._all_chunks_not_written(chunk_dir, total_chunks):
                tried += 1
                if tried >= 5:
                    error_msg = f'Error uploading files with temp_dir: {chunk_dir!r}'
                    logger.error(f'[{self.LOG_PREFIX}] {error_msg}')
                    return HttpResponseServerError(error_msg)
                time.sleep(1)

            # If all chunks writen create full file and remove chunk dir/files
            self._create_full_file_from_chunks(target_file_path,
                                               all_chunk_paths,
                                               chunk_dir)
            logger.info(f'[{self.LOG_PREFIX}] User {user!r} successfully created '
                        f'file {target_file_path}')

        return HttpResponse(status=200)

    def _save_chunk_data(self,
                         uploaded_file_name: str,
                         chunk_num: int,
                         chunk_data: InMemoryUploadedFile,
                         chunk_dir: Path) -> None:
        """
        Save this request chunk data in a temporary file with a lock so other
        resumable requests can't edit/delete it until finishes uploading

        Args:
            uploaded_file_name:  File name uploaded
            chunk_num: Resumable Chunk Number
            chunk_data: Request chunk file data
            chunk_dir: Dir to store chunk files
        """
        # Make the dirs if not created yet
        if not chunk_dir.is_dir():
            chunk_dir.mkdir(parents=True)

        # Save chunk file with lock file until finished saving
        chunk_name = self._chunk_file_name(uploaded_file_name, chunk_num)
        lock_file_path = self._chunk_lock_file_path(chunk_dir, chunk_num)
        with open(lock_file_path, 'a'):
            os.utime(lock_file_path, None)
        fs = FileSystemStorage(location=chunk_dir)
        fs.save(chunk_name, chunk_data)
        os.unlink(lock_file_path)
        logger.debug(f'[{self.LOG_PREFIX}] Created chunk file {chunk_dir / chunk_name!r}')

    @staticmethod
    def _all_chunk_paths(uploaded_file_name: str,
                         chunk_dir: Path,
                         total_chunks: int) -> List[Path]:
        """
        Return a list of all the chunk file paths from all the ResumableJS requests
        """
        all_chunk_paths = []
        for chunk_num in range(1, total_chunks + 1):
            chunk_path = chunk_dir / f"{uploaded_file_name}_{chunk_num:03d}"
            all_chunk_paths.append(chunk_path)
        return all_chunk_paths

    def _all_chunks_not_written(self,
                                chunk_dir: Path,
                                total_chunks: int) -> bool:
        """
        Return true if all the chunks have not finished writing
        by checking the if any of their lock files still exists
        """
        all_lock_file_paths = []
        for chunk_num in range(1, total_chunks + 1):
            lock_file_path = self._chunk_lock_file_path(chunk_dir, chunk_num)
            all_lock_file_paths.append(lock_file_path)
        return any([x.is_file() for x in all_lock_file_paths])

    def _create_full_file_from_chunks(self,
                                      target_file_path: Path,
                                      all_chunk_paths: List[Path],
                                      chunk_dir: Path):
        """
        Once all the chunk data has been written create the full file
        with the aggregated chunks
        """
        # Make sure some other chunk didn't trigger file reconstruction
        if target_file_path.exists():
            logger.debug(
                f'[{self.LOG_PREFIX}] File {target_file_path!r} exists already. Overwriting..'
            )
            target_file_path.unlink()

        # Save file from all uploaded chunk data
        with open(target_file_path, "ab") as fp:
            for p in all_chunk_paths:
                with open(p, 'rb') as stored_chunk_file:
                    fp.write(stored_chunk_file.read())
            logger.info(f'[{self.LOG_PREFIX}] File saved to {target_file_path!r}')

        # Remove the chunk dir all all files in it
        shutil.rmtree(chunk_dir)

    @staticmethod
    def _chunk_file_name(uploaded_file_name: str, chunk_num: int) -> str:
        """
        Return name of the chunk file to write for a chunk num
        """
        return f"{uploaded_file_name}_{chunk_num:03d}"

    @staticmethod
    def _chunk_lock_file_path(chunk_dir: Path, chunk_num: int) -> Path:
        """
        Return path of the lock file for a chunk num
        """
        return chunk_dir / f'.lock_{chunk_num}'
