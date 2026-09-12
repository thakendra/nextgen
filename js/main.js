// NextGen Interiors & Architects - Core Site Script
document.addEventListener('DOMContentLoaded', () => {

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

  // Dynamic Lazy-load Google Maps on scroll
  const mapWrap = document.querySelector('.map-wrap');
  if (mapWrap) {
    const mapObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const iframe = mapWrap.querySelector('iframe[data-src]');
          if (iframe) {
            iframe.src = iframe.dataset.src;
            iframe.removeAttribute('data-src');
          }
          obs.unobserve(mapWrap);
        }
      });
    }, { rootMargin: '350px 0px' });
    mapObserver.observe(mapWrap);
  }
