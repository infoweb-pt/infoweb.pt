/**
 * Shared GA4 helpers: window.trackEvent, declarative data-track="*" clicks,
 * scroll depth, external HTTPS links, FAQ <details> opens.
 */
(function () {
  "use strict";

  function withoutUndefined(obj) {
    return Object.keys(obj).reduce(function (acc, k) {
      if (obj[k] !== undefined) acc[k] = obj[k];
      return acc;
    }, {});
  }

  function normalizeToolSegment(segment) {
    if (!segment) return undefined;
    return String(segment).replace(/-/g, "_");
  }

  function toolSegmentFromPath() {
    var m = location.pathname.match(/\/free-tools\/([^/]+)\/?$/i);
    if (m && m[1] !== "") return m[1];
    m = location.pathname.match(/\/free-tools\/([^/]+)\//);
    return m ? m[1] : undefined;
  }

  function baseParams() {
    var html = document.documentElement;
    var rawSeg = toolSegmentFromPath();
    return withoutUndefined({
      page_path: location.pathname || "/",
      page_location: location.href,
      page_title: document.title,
      language: html.lang || "en",
      tool_name: rawSeg ? normalizeToolSegment(rawSeg) : undefined,
      client_ts: new Date().toISOString(),
    });
  }

  window.trackEvent = function (eventName, params) {
    var merged = withoutUndefined(Object.assign({}, baseParams(), params || {}));
    if (typeof window.gtag === "function") window.gtag("event", eventName, merged);
    if (window.console) window.console.debug("[trackEvent]", eventName, merged);
  };

  document.addEventListener(
    "click",
    function (e) {
      var el = e.target && e.target.closest ? e.target.closest("[data-track]") : null;
      if (!el || !el.dataset || !el.dataset.track) return;
      var attrs = {};
      Array.prototype.forEach.call(el.attributes || [], function (a) {
        if (a.name.indexOf("data-track-") === 0)
          attrs[a.name.slice(11).replace(/-/g, "_")] = a.value;
      });
      if (el.tagName === "A" && el.href) attrs.link_url = el.href;
      window.trackEvent(el.dataset.track, attrs);
    },
    true
  );

  window.trackEvent("page_view_enriched");

  var depthHit = {};
  function scrollPercent() {
    var el = document.documentElement;
    var docH = el.scrollHeight - el.clientHeight;
    if (docH <= 0) return 100;
    return Math.round((window.scrollY / docH) * 100);
  }

  window.addEventListener(
    "scroll",
    function () {
      var p = scrollPercent();
      [25, 50, 75, 100].forEach(function (d) {
        if (p >= d && !depthHit[d]) {
          depthHit[d] = 1;
          window.trackEvent("scroll_depth", { percent: d });
        }
      });
    },
    { passive: true }
  );

  document.addEventListener(
    "click",
    function (e) {
      var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!a || (a.dataset && a.dataset.track)) return;
      var href = a.getAttribute("href") || "";
      if (href.indexOf("#") === 0 || href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0) return;
      try {
        var url = new URL(a.href, location.href);
        if ((url.protocol === "http:" || url.protocol === "https:") && url.host !== location.host)
          window.trackEvent("external_link_click", { link_url: a.href, link_domain: url.host });
      } catch (_) {}
    },
    true
  );

  document.addEventListener(
    "toggle",
    function (e) {
      var d = e.target;
      if (!d || d.tagName !== "DETAILS" || !d.open) return;
      var section = d.closest("section, main, body");
      if (!section) return;
      var items = section.querySelectorAll("details");
      var idx = Array.prototype.indexOf.call(items, d);
      if (idx >= 0) window.trackEvent("faq_open", { question_index: idx + 1 });
    },
    true
  );
})();
