(() => {
  'use strict';

  const LANGS = {
    hr: { name: 'Hrvatski', flag: '<svg viewBox="0 0 24 16" aria-hidden="true"><rect width="24" height="16" fill="#fff"/><rect width="24" height="5.34" fill="#ff1f36"/><rect y="10.66" width="24" height="5.34" fill="#171796"/><g transform="translate(9 5) scale(.75)"><path d="M0 0h8v7c0 3-2 5-4 6-2-1-4-3-4-6z" fill="#fff" stroke="#1d4ed8" stroke-width=".45"/><path d="M0 0h2v2H0zm4 0h2v2H4zM2 2h2v2H2zm4 2h2v2H6zM0 4h2v2H0zm4 4h2v2H4zM2 6h2v2H2z" fill="#ef233c"/></g></svg>' },
    en: { name: 'English', flag: '<svg viewBox="0 0 24 16" aria-hidden="true"><rect width="24" height="16" fill="#1746a2"/><path d="M0 0l24 16M24 0L0 16" stroke="#fff" stroke-width="3.4"/><path d="M0 0l24 16M24 0L0 16" stroke="#e11d48" stroke-width="1.4"/><path d="M12 0v16M0 8h24" stroke="#fff" stroke-width="5"/><path d="M12 0v16M0 8h24" stroke="#e11d48" stroke-width="2.6"/></svg>' },
    de: { name: 'Deutsch', flag: '<svg viewBox="0 0 24 16" aria-hidden="true"><rect width="24" height="5.34" fill="#111"/><rect y="5.33" width="24" height="5.34" fill="#dd1e2f"/><rect y="10.66" width="24" height="5.34" fill="#ffce00"/></svg>' },
    it: { name: 'Italiano', flag: '<svg viewBox="0 0 24 16" aria-hidden="true"><rect width="8" height="16" fill="#009246"/><rect x="8" width="8" height="16" fill="#fff"/><rect x="16" width="8" height="16" fill="#ce2b37"/></svg>' },
    es: { name: 'Español', flag: '<svg viewBox="0 0 24 16" aria-hidden="true"><rect width="24" height="16" fill="#c60b1e"/><rect y="4" width="24" height="8" fill="#ffc400"/></svg>' }
  };

  const STYLE_ID = 'ag-language-menu-styles';

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent =
      '.ag-language-menu{position:relative;z-index:120;min-width:154px}' +
      '.ag-language-menu select{font:inherit;color:#e5e7eb;background:#081126;border:1px solid rgba(93,231,255,.34);border-radius:10px;padding:8px 10px;min-width:154px}' +
      '.ag-language-menu--enhanced>select{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important;border:0!important}' +
      '.ag-language-trigger{width:100%;min-height:40px;display:flex;align-items:center;gap:9px;padding:8px 10px;border:1px solid rgba(93,231,255,.34);border-radius:11px;background:linear-gradient(145deg,#111d39,#081126);color:#eafcff;font:700 12px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer;box-shadow:inset 0 1px rgba(255,255,255,.05)}' +
      '.ag-language-trigger:hover,.ag-language-trigger:focus-visible{border-color:#3cf5ff;box-shadow:0 0 0 3px rgba(60,245,255,.14)}' +
      '.ag-language-trigger svg,.ag-language-option svg{width:24px;height:16px;flex:0 0 24px;border-radius:2px;box-shadow:0 0 0 1px rgba(255,255,255,.18)}' +
      '.ag-language-caret{margin-left:auto;color:#78f7ff;font-size:10px;transition:transform .15s}.ag-language-trigger[aria-expanded="true"] .ag-language-caret{transform:rotate(180deg)}' +
      '.ag-language-list{position:absolute;top:calc(100% + 6px);left:0;right:0;display:none;padding:6px;margin:0;list-style:none;border:1px solid rgba(93,231,255,.32);border-radius:12px;background:#071022f5;box-shadow:0 18px 48px rgba(0,0,0,.62);backdrop-filter:blur(14px)}' +
      '.ag-language-list[data-open="true"]{display:block}.ag-language-option{width:100%;display:flex;align-items:center;gap:9px;padding:9px 10px;border:0;border-radius:9px;background:transparent;color:#dbeafe;font:700 12px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-align:left;cursor:pointer}' +
      '.ag-language-option:hover,.ag-language-option:focus-visible{outline:none;background:rgba(60,245,255,.1);color:#fff}.ag-language-option[aria-selected="true"]{background:linear-gradient(120deg,rgba(60,245,255,.2),rgba(0,245,200,.12));color:#75ffe9}' +
      '@media(max-width:520px){.ag-language-menu{min-width:142px}.ag-language-trigger{padding:7px 9px}.ag-language-option{padding:8px 9px}}';
    document.head.appendChild(style);
  }

  function enhance(select) {
    if (!select || select.dataset.agEnhanced === 'true') return;
    select.dataset.agEnhanced = 'true';

    const wrapper = document.createElement('div');
    wrapper.className = 'ag-language-menu';
    select.parentNode.insertBefore(wrapper, select);
    wrapper.appendChild(select);
    wrapper.classList.add('ag-language-menu--enhanced');

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'ag-language-trigger';
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');

    const list = document.createElement('div');
    list.className = 'ag-language-list';
    list.id = (select.id || 'ag-language') + '-list';
    list.setAttribute('role', 'listbox');
    trigger.setAttribute('aria-controls', list.id);

    Array.from(select.options).forEach(option => {
      const lang = LANGS[option.value];
      if (!lang) return;
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'ag-language-option';
      item.dataset.value = option.value;
      item.setAttribute('role', 'option');
      item.innerHTML = lang.flag + '<span>' + lang.name + '</span>';
      list.appendChild(item);
    });

    wrapper.appendChild(trigger);
    wrapper.appendChild(list);

    const items = () => Array.from(list.querySelectorAll('.ag-language-option'));
    const currentMeta = () => LANGS[select.value] || LANGS.en;

    function sync() {
      const meta = currentMeta();
      trigger.innerHTML = meta.flag + '<span>' + meta.name + '</span><span class="ag-language-caret">▼</span>';
      items().forEach(item => item.setAttribute('aria-selected', String(item.dataset.value === select.value)));
    }

    function close(focusTrigger = false) {
      list.dataset.open = 'false';
      trigger.setAttribute('aria-expanded', 'false');
      if (focusTrigger) trigger.focus();
    }

    function open(focusSelected = false) {
      list.dataset.open = 'true';
      trigger.setAttribute('aria-expanded', 'true');
      if (focusSelected) {
        const selected = items().find(item => item.dataset.value === select.value) || items()[0];
        selected?.focus();
      }
    }

    function moveFocus(delta) {
      const all = items();
      const index = Math.max(0, all.indexOf(document.activeElement));
      all[(index + delta + all.length) % all.length]?.focus();
    }

    trigger.addEventListener('click', () => {
      trigger.getAttribute('aria-expanded') === 'true' ? close() : open(false);
    });

    trigger.addEventListener('keydown', event => {
      if (['Enter', ' ', 'ArrowDown'].includes(event.key)) {
        event.preventDefault();
        open(true);
      } else if (event.key === 'Escape') {
        close();
      }
    });

    list.addEventListener('keydown', event => {
      if (event.key === 'ArrowDown') { event.preventDefault(); moveFocus(1); }
      else if (event.key === 'ArrowUp') { event.preventDefault(); moveFocus(-1); }
      else if (event.key === 'Home') { event.preventDefault(); items()[0]?.focus(); }
      else if (event.key === 'End') { event.preventDefault(); items().at(-1)?.focus(); }
      else if (event.key === 'Escape') { event.preventDefault(); close(true); }
      else if (event.key === 'Tab') close();
    });

    list.addEventListener('click', event => {
      const item = event.target.closest('.ag-language-option');
      if (!item) return;
      select.value = item.dataset.value;
      select.dispatchEvent(new Event('change', { bubbles: true }));
      sync();
      close(true);
    });

    select.addEventListener('change', sync);
    document.addEventListener('click', event => {
      if (!wrapper.contains(event.target)) close();
    });

    sync();
  }

  function init() {
    injectStyles();
    document.querySelectorAll('select[data-ag-language-menu]').forEach(enhance);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();