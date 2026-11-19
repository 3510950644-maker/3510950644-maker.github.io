/* ------------------------------------------------------------------
 * i18n.js — 中英文切换 / Chinese-English language switch
 * 用法：
 *   1. 需要翻译的元素加 data-en="对应的英文内容"（可包含 <br> <strong> 等标签）
 *   2. 输入框占位符加 data-en-ph="英文 placeholder"
 *   3. 页面内放置 <button data-lang-toggle> 作为切换按钮
 *   4. 动态渲染的内容监听 document 上的 px:langchange 事件重新渲染
 * ------------------------------------------------------------------ */
(function () {
  'use strict';

  var STORAGE_KEY = 'px-lang';
  var SUPPORTED = ['zh', 'en'];
  var html = document.documentElement;

  /* 当前语言：'zh' 或 'en' */
  function lang() {
    return html.getAttribute('data-lang') === 'en' ? 'en' : 'zh';
  }
  window.pxLang = lang;

  function save(value) {
    try { localStorage.setItem(STORAGE_KEY, value); } catch (e) { /* 隐私模式等情况下忽略 */ }
  }

  /* 支持用 ?lang=en 直接打开英文版（便于分享链接） */
  function fromQuery() {
    try {
      var value = new URLSearchParams(window.location.search).get('lang');
      return SUPPORTED.indexOf(value) > -1 ? value : null;
    } catch (e) { return null; }
  }

  function fromStorage() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      return SUPPORTED.indexOf(saved) > -1 ? saved : null;
    } catch (e) { return null; }
  }

  function restore() {
    return fromQuery() || fromStorage();
  }

  /* 应用语言：保存首次出现的中文原文，之后在两种语言之间切换 */
  function apply(next, persist) {
    if (SUPPORTED.indexOf(next) < 0) next = 'zh';
    var isEn = next === 'en';

    html.setAttribute('data-lang', next);
    html.setAttribute('lang', isEn ? 'en' : 'zh-CN');

    document.querySelectorAll('[data-en]').forEach(function (el) {
      if (el.dataset.zh === undefined) el.dataset.zh = el.innerHTML;
      el.innerHTML = isEn ? el.dataset.en : el.dataset.zh;
    });

    document.querySelectorAll('[data-en-ph]').forEach(function (el) {
      if (el.dataset.zhPh === undefined) el.dataset.zhPh = el.getAttribute('placeholder') || '';
      el.setAttribute('placeholder', isEn ? el.dataset.enPh : el.dataset.zhPh);
    });

    document.querySelectorAll('[data-lang-toggle]').forEach(function (btn) {
      var label = isEn ? '切换为中文 / Switch to Chinese' : 'Switch to English / 切换为英文';
      btn.setAttribute('aria-label', label);
      btn.setAttribute('title', label);
      btn.setAttribute('aria-pressed', isEn ? 'true' : 'false');
    });

    if (persist) {
      save(next);
      syncUrl(next);
    }
    document.dispatchEvent(new CustomEvent('px:langchange', { detail: { lang: next } }));
  }

  window.pxSetLang = function (next) { apply(next, true); };

  /* 切换后把语言写入地址栏参数，刷新或分享链接时保持同一语言 */
  function syncUrl(next) {
    try {
      var url = new URL(window.location.href);
      url.searchParams.set('lang', next);
      window.history.replaceState(null, '', url.href);
    } catch (e) { /* 忽略 */ }
  }

  /* 初始化：优先使用上次选择，其次使用页面默认（中文） */
  apply(restore() || 'zh', false);

  /* 切换按钮（事件委托，兼容任意位置、任意数量的按钮） */
  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('[data-lang-toggle]') : null;
    if (!btn) return;
    e.preventDefault();
    window.pxSetLang(lang() === 'zh' ? 'en' : 'zh');
  });
})();
