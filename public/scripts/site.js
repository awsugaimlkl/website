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
    // A page that knows the exact end time gives it in data-event-end.
    var end = Date.parse(
      el.getAttribute("data-event-end") || el.getAttribute("data-event-date") + "T23:59:59+08:00"
    );
    if (isNaN(end)) return;
    if (end >= now) {
      // While the event is on, a label can say so: data-event-start and data-live-label.
      var start = Date.parse(el.getAttribute("data-event-start") || "");
      if (!isNaN(start) && now >= start && el.hasAttribute("data-live-label")) {
        el.textContent = el.getAttribute("data-live-label");
      }
      return;
    }
    if (el.hasAttribute("data-hide-when-past")) el.hidden = true;
    if (el.hasAttribute("data-past-label")) el.textContent = el.getAttribute("data-past-label");
  });

  // 3. Countdown to the start of an event. The start and end times are in the
  //    data-countdown and data-countdown-end attributes. The numbers are created
  //    here and are not written in the page itself, so anything that reads the page
  //    without running scripts never sees a row of zeros. While the event is on,
  //    the countdown reads "Happening now". After it ends, the countdown is removed.
  document.querySelectorAll("[data-countdown]").forEach(function (el) {
    var start = Date.parse(el.getAttribute("data-countdown"));
    if (isNaN(start)) return;
    var end = Date.parse(el.getAttribute("data-countdown-end") || "");

    var units = ["days", "hours", "minutes", "seconds"];
    var summary = el.querySelector("[data-countdown-summary]");
    var cells = null;
    var timer;

    function pad(n) {
      return n < 10 ? "0" + n : String(n);
    }

    function buildCells() {
      var wrap = document.createElement("div");
      wrap.className = "cells";
      // Screen readers get one plain sentence instead of numbers that change every second.
      wrap.setAttribute("aria-hidden", "true");
      cells = {};
      units.forEach(function (unit) {
        var cell = document.createElement("div");
        var number = document.createElement("strong");
        if (unit === "days") number.className = "days";
        var label = document.createElement("span");
        cell.appendChild(number);
        cell.appendChild(document.createTextNode(" "));
        cell.appendChild(label);
        wrap.appendChild(cell);
        cells[unit] = { number: number, label: label };
      });
      el.appendChild(wrap);
    }

    function set(unit, value, text) {
      cells[unit].number.textContent = text;
      // "1 day", not "1 days"
      cells[unit].label.textContent = value === 1 ? unit.slice(0, -1) : unit;
    }

    function clear() {
      var old = el.querySelector(".cells, .now");
      if (old) el.removeChild(old);
      cells = null;
      if (summary) summary.textContent = "";
    }

    function tick() {
      var now = Date.now();
      var seconds = Math.floor((start - now) / 1000);

      // Before the event: count down.
      if (seconds > 0) {
        if (!cells) {
          buildCells();
          if (summary) {
            var days = Math.floor(seconds / 86400);
            summary.textContent =
              days > 1 ? days + " days to go." : days === 1 ? "1 day to go." : "Starts in less than a day.";
          }
          el.classList.add("is-live");
        }
        var d = Math.floor(seconds / 86400);
        var h = Math.floor((seconds % 86400) / 3600);
        var m = Math.floor((seconds % 3600) / 60);
        var s = seconds % 60;
        set("days", d, String(d));
        set("hours", h, pad(h));
        set("minutes", m, pad(m));
        set("seconds", s, pad(s));
        return;
      }

      // During the event: say so.
      if (!isNaN(end) && now < end) {
        if (!el.querySelector(".now")) {
          clear();
          var live = document.createElement("p");
          live.className = "now";
          live.textContent = "Happening now";
          el.appendChild(live);
          el.classList.add("is-live");
        }
        return;
      }

      // After the event: remove the countdown.
      clear();
      el.hidden = true;
      clearInterval(timer);
    }

    timer = setInterval(tick, 1000);
    tick();
  });
})();
