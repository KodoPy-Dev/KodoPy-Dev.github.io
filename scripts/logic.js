
function highlightActiveLink() {
    const sidebarLinks = document.querySelectorAll(".sidebar a");
    const currentPath = window.location.pathname;
    const currentHash = window.location.hash;

    sidebarLinks.forEach(link => {
        const linkPath = new URL(link.href, window.location.origin).pathname;
        const linkHash = new URL(link.href, window.location.origin).hash;

        if (linkPath === currentPath && (linkHash === "" || linkHash === currentHash)) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
}

// Document Loaded Callback
document.addEventListener("DOMContentLoaded", highlightActiveLink);

