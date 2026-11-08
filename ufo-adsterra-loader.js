/* UFO Invaders — original Adsterra publisher GET CODE, menu only.
 * One ad request per initial page load on the approved hostname;
 * no requests without explicit, current first-party advertising consent.
 * The existing menu overlay class controls visibility without changing
 * the game engine. No refresh on returning to menu / no auto-retry.
 * Parser-time document.write replicates previous Apps & Games pilots.
 */
(() => {
  "use strict";
  if (location.hostname !== "ufo-invaders.appsandgames.org") return;
  if (document.readyState !== "loading") return;
  if (navigator.onLine === false) return;
  const current = document.currentScript;
  const slot = current?.parentElement;
  const area = slot?.parentElement;
  if (!slot?.classList.contains("ufo-ad-unit") ||
      area?.id !== "ufo-ad-area") return;
  if (!matchMedia("(min-width: 320px)").matches) return;
  const desktop = matchMedia("(min-width: 800px)").matches;
  const unit = current.dataset.unit;
  if ((desktop && unit !== "desktop") || (!desktop && unit !== "mobile")) return;

  let allowed = false;
  try {
    const entry = document.cookie.split(";").map(s => s.trim())
      .find(s => s.startsWith("ag_privacy_choices_v1="));
    const data = entry && JSON.parse(decodeURIComponent(
      entry.slice("ag_privacy_choices_v1=".length)));
    const age = data && Date.now() - data.timestamp;
    allowed = !!data && data.version === 1 &&
      data.partnerRevision === "adsterra-2026-11" &&
      data.advertising === true &&
      Number.isFinite(age) && age >= 0 &&
      age <= 180 * 24 * 60 * 60 * 1000;
  } catch (_) { allowed = false; }
  if (!allowed) return;

  const tags = {
    desktop: "<script>\n  atOptions = {\n    'key' : 'ca9311b59dff0d10c866a4771bda909a',\n    'format' : 'iframe',\n    'height' : 90,\n    'width' : 728,\n    'params' : {}\n  };\n</script>\n<script src=\"https://bauval.org/22/ca9311b59dff0d10c866a4771bda909a\"></script>",
    mobile: "<script>\n  atOptions = {\n    'key' : 'a4b69fdafe78b3f96a02dfeee5a92a59',\n    'format' : 'iframe',\n    'height' : 50,\n    'width' : 320,\n    'params' : {}\n  };\n</script>\n<script src=\"https://bauval.org/22/a4b69fdafe78b3f96a02dfeee5a92a59\"></script>"
  };
  area.hidden = false;
  slot.hidden = false;
  const label = document.createElement("span");
  label.className = "ufo-ad-label";
  label.textContent = "Advertisement";
  slot.insertBefore(label, current);
  document.write(tags[unit]);
})();
