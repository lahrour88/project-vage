// قائمة الهاتف
document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.querySelector('.menu-toggle');
  const appbarNav = document.querySelector('.appbar-nav');
  
  if (menuToggle && appbarNav) {
    menuToggle.addEventListener('click', () => {
      appbarNav.classList.toggle('active');
    });
  }
  
  // إضافة سنة حقوق النشر
  const yearElements = document.querySelectorAll('#year');
  if (yearElements.length > 0) {
    const currentYear = new Date().getFullYear();
    yearElements.forEach(el => {
      el.textContent = currentYear;
    });
  }
  
  // تأثير التمرير لشريط التطبيق
  window.addEventListener('scroll', function() {
    const appbar = document.querySelector('.appbar');
    if (appbar) {
      if (window.scrollY > 50) {
        appbar.classList.add('scrolled');
      } else {
        appbar.classList.remove('scrolled');
      }
    }
  });
});
console.log("from abdelaadime lahrour lahrour_1902")