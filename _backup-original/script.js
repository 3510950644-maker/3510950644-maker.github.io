/* index.html 交互脚本：仅保留移动端菜单开合
 * 中英文切换逻辑见 i18n.js
 */
const menuBtn = document.querySelector('.menu-btn');
const nav = document.querySelector('.nav');
if (menuBtn && nav) {
  menuBtn.addEventListener('click', () => nav.classList.toggle('mobile-open'));
}

// Application explorer: keep the overview compact while exposing all ten official industries.
const applicationItems = document.querySelectorAll('.application-item[data-application]');
const applicationDetails = document.querySelectorAll('.application-detail[data-application-detail]');
applicationItems.forEach((item) => {
  item.addEventListener('click', () => {
    const key = item.dataset.application;
    applicationItems.forEach((button) => {
      const active = button === item;
      button.classList.toggle('active', active);
      button.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    applicationDetails.forEach((detail) => detail.classList.toggle('active', detail.dataset.applicationDetail === key));
  });
});
