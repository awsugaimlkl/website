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

  // 3. Countdown to the start of an event. The start time is in the data-countdown
  //    attribute. The countdown stays hidden until this has filled in the numbers,
  //    and is removed once the event has started.
  document.querySelectorAll("[data-countdown]").forEach(function (el) {
    var start = Date.parse(el.getAttribute("data-countdown"));
    if (isNaN(start)) return;

    var cells = {};
    el.querySelectorAll("[data-unit]").forEach(function (cell) {
      cells[cell.getAttribute("data-unit")] = cell;
    });

    var timer;

    function pad(n) {
      return n < 10 ? "0" + n : String(n);
    }

    function set(unit, text) {
      if (cells[unit]) cells[unit].textContent = text;
    }

    function tick() {
      var seconds = Math.floor((start - Date.now()) / 1000);
      if (seconds <= 0) {
        el.hidden = true;
        clearInterval(timer);
        return false;
      }
      set("days", String(Math.floor(seconds / 86400)));
      set("hours", pad(Math.floor((seconds % 86400) / 3600)));
      set("minutes", pad(Math.floor((seconds % 3600) / 60)));
      set("seconds", pad(seconds % 60));
      return true;
    }

    if (!tick()) return;

    // Screen readers get one plain sentence instead of numbers that change every second.
    var summary = el.querySelector("[data-countdown-summary]");
    if (summary) {
      var days = Math.floor((start - Date.now()) / 86400000);
      summary.textContent =
        days > 1 ? days + " days to go." : days === 1 ? "1 day to go." : "Starts in less than a day.";
    }

    el.classList.add("is-live");
    timer = setInterval(tick, 1000);
  });
})();
