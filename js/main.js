// NextGen Interiors & Architects - Core Site Script
document.addEventListener('DOMContentLoaded', () => {
  // Custom Cursor
  const dot = document.getElementById('cursorDot');
  const ring = document.getElementById('cursorRing');
  let mx = 0, my = 0, rx = 0, ry = 0;

  if (dot && ring) {
    document.addEventListener('mousemove', e => {
      mx = e.clientX;
      my = e.clientY;
      dot.style.left = mx + 'px';
      dot.style.top = my + 'px';
    });

    (function animRing() {
      rx += (mx - rx) * 0.11;
      ry += (my - ry) * 0.11;
      ring.style.left = rx + 'px';
      ring.style.top = ry + 'px';
      requestAnimationFrame(animRing);
    })();

    document.querySelectorAll('a, button, input, select, textarea, .faq-item, .blog-card, .port-card, .proj-card, .m-menu-links a').forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('c-hover'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('c-hover'));
    });
  }

  // Navigation Menu & Mobile Drawer
  const menuBtn = document.getElementById('menuBtn');
  const mMenu = document.getElementById('mMenu');
  const mMenuClose = document.getElementById('mMenuClose');

  function openMenu() {
    if (menuBtn && mMenu) {
      menuBtn.classList.add('open');
      mMenu.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeMenu() {
    if (menuBtn && mMenu) {
      menuBtn.classList.remove('open');
      mMenu.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  if (menuBtn) {
    menuBtn.addEventListener('click', () => {
      mMenu && mMenu.classList.contains('open') ? closeMenu() : openMenu();
    });
  }
  if (mMenuClose) mMenuClose.addEventListener('click', closeMenu);
  if (mMenu) {
    mMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  }

  const mPBtn = document.getElementById('mPortfolioBtn');
  const mPSub = document.getElementById('mPortfolioSub');
  if (mPBtn && mPSub) {
    mPBtn.addEventListener('click', () => {
      const o = mPSub.classList.contains('open');
      mPSub.classList.toggle('open', !o);
      mPBtn.classList.toggle('active', !o);
    });
  }

  // Filter Buttons on Portfolio & Category Grids
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;
      document.querySelectorAll('.proj-card').forEach(card => {
        card.classList.toggle('hidden', f !== 'all' && card.dataset.category !== f);
      });
    });
  });

  // Scroll Reveal Animations
  const ro = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('vis');
        ro.unobserve(e.target);
      }
    });
  }, { threshold: 0.04 });
  document.querySelectorAll('.rv').forEach(el => ro.observe(el));
});
