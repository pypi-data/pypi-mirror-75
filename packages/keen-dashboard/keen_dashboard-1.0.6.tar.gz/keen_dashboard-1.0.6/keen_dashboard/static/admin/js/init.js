$(function () {

    $('.toast').toast('show')

    function inIframe() {
        try {
            return window.self !== window.top;
        } catch (e) {
            return true;
        }
    }

    if (inIframe()) {
        $('#kt_header').hide()
        $('#filtros').hide()
        $('#object-tools').hide()
        $('#actions-container').hide()
        $('#breadcrumbs').hide()
        $('#content-main').removeClass('filtered')
    }

});