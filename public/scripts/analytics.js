// Google Analytics setup. This is the standard Google tag snippet, kept in a file
// instead of inline so the Content-Security-Policy in public/_headers can stay strict.
// The measurement ID comes from src/lib/site.js through the data-measurement-id attribute.

(function () {
  "use strict";

  var id = document.currentScript && document.currentScript.getAttribute("data-measurement-id");
  if (!id) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };
  window.gtag("js", new Date());
  window.gtag("config", id);
})();
