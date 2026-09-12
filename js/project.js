// NextGen Interiors & Architects - Project Showcase Script
document.addEventListener('DOMContentLoaded', () => {

  // Navigation Menu
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

  // Scroll Reveal
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

// Lightbox logic (Exposed globally for onclick="openLb(i)")
let lbCurrent = 0;
function getLbPhotos() {
  if (window.LB_PHOTOS && Array.isArray(window.LB_PHOTOS) && window.LB_PHOTOS.length > 0) {
    return window.LB_PHOTOS;
  }
  const cards = document.querySelectorAll('.gallery .g-card img');
  const urls = [];
  cards.forEach(img => {
    const src = img.getAttribute('src');
    if (src) urls.push(src);
  });
  return urls;
}

function openLb(idx) {
  const photos = getLbPhotos();
  if (!photos.length) return;
  lbCurrent = typeof idx === 'number' ? idx : 0;
  updateLb();
  const lb = document.getElementById('lb');
  if (lb) {
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeLb() {
  const lb = document.getElementById('lb');
  if (lb) {
    lb.classList.remove('open');
    document.body.style.overflow = '';
  }
}

function closeLbOnBg(e) {
  const lb = document.getElementById('lb');
  if (e.target === lb) closeLb();
}

function lbNav(dir) {
  const photos = getLbPhotos();
  if (!photos.length) return;
  lbCurrent = (lbCurrent + dir + photos.length) % photos.length;
  updateLb();
}

function updateLb() {
  const photos = getLbPhotos();
  if (!photos.length) return;
  const lbImg = document.getElementById('lbImg');
  const lbCounter = document.getElementById('lbCounter');
  if (lbImg) lbImg.src = photos[lbCurrent];
  if (lbCounter) lbCounter.textContent = (lbCurrent + 1) + ' / ' + photos.length;
}

document.addEventListener('keydown', e => {
  const lb = document.getElementById('lb');
  if (!lb || !lb.classList.contains('open')) return;
  if (e.key === 'Escape') closeLb();
  if (e.key === 'ArrowLeft') lbNav(-1);
  if (e.key === 'ArrowRight') lbNav(1);
});
