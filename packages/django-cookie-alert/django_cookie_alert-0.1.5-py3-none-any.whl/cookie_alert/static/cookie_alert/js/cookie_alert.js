document.addEventListener("DOMContentLoaded", function(event) {
    const cookie_alert = document.getElementById("cookie-alert");
    if (!cookie_alert) {
        return
    }

    cookie_alert.addEventListener("animationend", function(ev) {
        if (ev.type === "animationend") {
            if (cookie_alert.classList.contains('fade_out')) {
                cookie_alert.remove();
            }
        }
    }, false);

    cookie_alert.querySelector('button.cookie--accept').addEventListener("click", function(event) {
        hideCookieConsentDialog(event);
        setCookies();
        addTrackerIframe();
    });
});

let hideCookieConsentDialog = function(e) {
    const cookie_alert = document.getElementById("cookie-alert");
    // check if element exists
    if (!cookie_alert) { console.warn('Could not find cookie element'); return }

    e.preventDefault();
    cookie_alert.classList.toggle('fade_out');

    const modal_bg = document.getElementById("cookie-modal-bg");
    modal_bg.style.display = 'none';
};

let setCookies = function() {
    // set cookies
    let expires = new Date();
    expires.setFullYear(expires.getFullYear() + 1);

    // 'cookies_confirmed=true; expires=Thu, 18 Dec 2021 12:00:00 UTC; path=/';
    document.cookie = 'cookies_confirmed=true; expires=' + expires.toUTCString() + '; path=/';

    let analysis_checkbox = document.getElementById('cookie-alert-analysis-checkbox');
    if (analysis_checkbox && analysis_checkbox.checked) {
        document.cookie = 'analysis_confirmed=true; expires=' + expires.toUTCString() + '; path=/';
    }
};

let addTrackerIframe = function() {
    // Fake call same page again in an iframe to trigger analyisis/tracker scripts
    let randomString = Math.random().toString(36).substring(7);
    let state = history.state;
    let currentUrl = new URL(window.location.href);
    currentUrl.searchParams.append('c', randomString);

    // replace browser current url for caching bug; if user wants to refresh site
    history.replaceState(state, document.title, currentUrl.toString());

    let iframe = document.createElement("iframe");
    iframe.src = currentUrl.toString();
    iframe.style.display = 'none';
    document.getElementsByTagName('body')[0].append(iframe);
}
