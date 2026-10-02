// Small enhancements. The site works without this file.

(function () {
  "use strict";

  // 1. Phone menu: close it after a link is chosen, or when Escape is pressed.
  var menu = document.querySelector("details.mobile-nav");
  if (menu) {
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) menu.removeAttribute("open");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.hasAttribute("open")) {
        menu.removeAttribute("open");
        menu.querySelector("summary").focus();
      }
    });
  }

  // 2. Event status. Pages are built ahead of time, so an event could still read
  //    "Upcoming" after it has happened. Re-check against today's date here.
  //    An event is past once its day has ended in Malaysia time (UTC+8).
  var now = Date.now();
  document.querySelectorAll("[data-event-date]").forEach(function (el) {
    var end = Date.parse(el.getAttribute("data-event-date") + "T23:59:59+08:00");
    if (isNaN(end) || end >= now) return;
    if (el.hasAttribute("data-hide-when-past")) el.hidden = true;
    if (el.hasAttribute("data-past-label")) el.textContent = el.getAttribute("data-past-label");
  });
})();
