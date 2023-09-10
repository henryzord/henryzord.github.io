function activateLink() {
    let path = window.location.pathname;
    let page = path.split("/").pop();
    page = page.substring(0, page.indexOf('.'));
    let element = null;
    if(page.length === 0) {
        element = document.getElementById('nav-link-index');
    } else {
        element = document.getElementById('nav-link-' + page);
    }
    if(element != null) {
        element.classList.add('active');
    }
}