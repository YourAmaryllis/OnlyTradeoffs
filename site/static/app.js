// Only Tradeoffs: view tabs, open-on-link for value cards, quote highlighting, copy-prompt.
// Every page works without this script; it only adds the tabs and conveniences.
(function () {
  document.documentElement.classList.add("js");

  // Tabs: "By value" / "By section of the text". Without JS both views show, one after the other.
  var tabs = document.querySelector(".tabs");
  if (tabs) {
    var buttons = tabs.querySelectorAll("[role=tab]");
    var show = function (id) {
      buttons.forEach(function (b) {
        var on = b.getAttribute("aria-controls") === id;
        b.setAttribute("aria-selected", on ? "true" : "false");
        document.getElementById(b.getAttribute("aria-controls")).hidden = !on;
      });
    };
    buttons.forEach(function (b) { b.addEventListener("click", function () { show(b.getAttribute("aria-controls")); }); });
    tabs.hidden = false;
    show("by-value");
  }

  // A link to a value (chip, mirror link) switches to the value view and opens that card.
  function openValue(id) {
    var card = document.getElementById(id);
    if (!card || card.tagName !== "DETAILS") return;
    var view = card.closest(".view");
    if (view && view.hidden) {
      var t = document.querySelector('[aria-controls="' + view.id + '"]');
      if (t) t.click();
    }
    card.open = true;
  }
  document.querySelectorAll("[data-open]").forEach(function (a) {
    a.addEventListener("click", function () { openValue(a.dataset.open); });
  });
  if (location.hash) openValue(location.hash.slice(1));

  // "Open all" in a view.
  document.querySelectorAll("[data-expand]").forEach(function (b) {
    b.addEventListener("click", function () {
      var cards = document.querySelectorAll(b.dataset.expand + " details");
      var anyClosed = Array.prototype.some.call(cards, function (d) { return !d.open; });
      cards.forEach(function (d) { d.open = anyClosed; });
      b.textContent = anyClosed ? "Close all" : "Open all";
    });
  });

  // Quote link: flash the matching highlight in the full text.
  document.querySelectorAll("a.quote").forEach(function (a) {
    a.addEventListener("click", function () {
      var ref = a.dataset.ref;
      document.querySelectorAll("mark").forEach(function (m) {
        var on = (m.dataset.refs || "").split(" ").indexOf(ref) >= 0;
        m.classList.toggle("flash", on);
      });
    });
  });

  // Copy prompt.
  document.querySelectorAll("button.copy").forEach(function (b) {
    b.addEventListener("click", function () {
      fetch(b.dataset.src).then(function (r) { return r.text(); }).then(function (t) {
        return navigator.clipboard.writeText(t);
      }).then(function () {
        b.textContent = "Copied";
      }).catch(function () {
        window.location.href = b.dataset.src; // fallback: open the text so it can be copied by hand
      });
    });
  });
})();
