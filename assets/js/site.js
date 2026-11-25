// Portfolio interactions: autoplay visible videos, open projects from links,
// filter projects by topic.
(() => {
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // --- videos: play while visible (unless reduced motion), click toggles ---
  const videos = [...document.querySelectorAll("video.auto")];
  const visible = new Set();
  const playable = (v) => !reduceMotion && !v.dataset.paused && !v.closest("details:not([open])");
  const sync = (v) => {
    if (visible.has(v) && playable(v)) {
      if (v.preload === "none") v.preload = "auto";
      v.play().catch(() => {});
    } else v.pause();
  };
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        e.isIntersecting ? visible.add(e.target) : visible.delete(e.target);
        sync(e.target);
      }
    }, { threshold: 0.35 });
    videos.forEach((v) => io.observe(v));
  }
  videos.forEach((v) => {
    if (reduceMotion) v.controls = true;
    v.addEventListener("click", (ev) => {
      if (v.closest(".tile")) return; // tiles navigate to their project
      ev.preventDefault();
      if (v.paused) { delete v.dataset.paused; visible.add(v); v.play(); }
      else { v.dataset.paused = "1"; v.pause(); }
    });
  });
  document.querySelectorAll("details.project").forEach((d) =>
    d.addEventListener("toggle", () => d.querySelectorAll("video.auto").forEach(sync))
  );

  // --- open a project when its #id is linked ---
  const openFromHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const el = id && document.getElementById(id);
    if (el && el.tagName === "DETAILS") {
      el.hidden = false;
      el.open = true;
      requestAnimationFrame(() => el.scrollIntoView({ block: "start" }));
    }
  };
  window.addEventListener("hashchange", openFromHash);
  openFromHash();

  // keep the URL in sync so a specific project can be shared
  document.querySelectorAll("details.project").forEach((d) =>
    d.addEventListener("toggle", () => {
      if (d.open) history.replaceState(null, "", "#" + d.id);
    })
  );

  // --- topic filter ---
  const chips = [...document.querySelectorAll(".chip")];
  chips.forEach((chip) =>
    chip.addEventListener("click", () => {
      const f = chip.dataset.filter;
      chips.forEach((c) => c.classList.toggle("on", c === chip));
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
      document.querySelectorAll("details.project").forEach((d) => {
        d.hidden = f !== "*" && !d.dataset.tags.split(" ").includes(f);
      });
    })
  );
})();
