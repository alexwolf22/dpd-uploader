# AUTO GENERATED FILE - DO NOT EDIT

uploader <- function(id=NULL, label=NULL, value=NULL) {
    
    props <- list(id=id, label=label, value=value)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Uploader',
        namespace = 'dpd_uploader',
        propNames = c('id', 'label', 'value'),
        package = 'dpdUploader'
        )

    structure(component, class = c('dash_component', 'list'))
}
