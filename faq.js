/* FAQ search (Chinese / English) */
(function () {
  'use strict';
  var input = document.getElementById('faq-search');
  var list = document.getElementById('faq-list');
  var count = document.getElementById('faq-count');
  var empty = document.getElementById('faq-empty');
  if (!input || !list) return;

  var isEn = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var items = Array.prototype.slice.call(list.querySelectorAll('.faq-item'));
  var total = items.length;

  function render() {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    items.forEach(function (item) {
      var hit = !q || item.textContent.toLowerCase().indexOf(q) > -1;
      item.hidden = !hit;
      if (hit) shown++;
      if (!hit) item.open = false;
    });
    if (isEn) {
      count.textContent = q ? shown + ' of ' + total + ' questions' : total + ' questions';
    } else {
      count.textContent = q ? '找到 ' + shown + ' 条 / 共 ' + total + ' 条' : '共 ' + total + ' 条问答';
    }
    empty.hidden = shown > 0;
  }

  input.addEventListener('input', render);
  render();
})();
