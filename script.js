/* 正宇新材静态站 – 交互脚本 */
(function () {
  'use strict';

  /* ---------- mobile nav ---------- */
  var btn = document.querySelector('.menu-btn');
  var nav = document.querySelector('.nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? '×' : '☰';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        btn.textContent = '☰';
        btn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target) && !btn.contains(e.target)) {
        nav.classList.remove('open');
        btn.textContent = '☰';
      }
    });
  }

  /* ---------- current nav highlight fallback ---------- */
  var path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav > li > a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === path) a.classList.add('active');
  });
})();

/* ---------- company video modal ---------- */
(function () {
  var modal = document.getElementById('video-modal');
  if (!modal) return;
  var video = document.getElementById('company-video');

  function openVideo() {
    modal.hidden = false;
    document.body.classList.add('no-scroll');
    if (video) {
      try { video.currentTime = 0; } catch (e) {}
      var p = video.play();
      if (p && p.catch) p.catch(function () {});
    }
  }

  function closeVideo() {
    modal.hidden = true;
    document.body.classList.remove('no-scroll');
    if (video) video.pause();
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-video-open]'), function (b) {
    b.addEventListener('click', openVideo);
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-video-close]'), function (b) {
    b.addEventListener('click', closeVideo);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) closeVideo();
  });
})();
