    // CURSOR
    const dot=document.getElementById('cursorDot'),ring=document.getElementById('cursorRing');
    let mx=0,my=0,rx=0,ry=0;
    document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;dot.style.left=mx+'px';dot.style.top=my+'px';});
    (function animRing(){rx+=(mx-rx)*.11;ry+=(my-ry)*.11;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(animRing);})();
    document.querySelectorAll('a,button').forEach(el=>{el.addEventListener('mouseenter',()=>document.body.classList.add('c-hover'));el.addEventListener('mouseleave',()=>document.body.classList.remove('c-hover'));});



    // NAV SCROLL
    window.addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',window.scrollY>60));

    // MOBILE MENU
    const btn=document.getElementById('menuBtn'),mm=document.getElementById('mMenu');
    function openMenu(){btn.classList.add('open');mm.classList.add('open');document.body.style.overflow='hidden';}
    function closeMenu(){btn.classList.remove('open');mm.classList.remove('open');document.body.style.overflow='';}
    btn.addEventListener('click',()=>mm.classList.contains('open')?closeMenu():openMenu());
    document.getElementById('mMenuClose').addEventListener('click', closeMenu);
    mm.querySelectorAll('a').forEach(a=>a.addEventListener('click', closeMenu));

    // Mobile portfolio accordion
    const mPortfolioBtn = document.getElementById('mPortfolioBtn');
    const mPortfolioSub = document.getElementById('mPortfolioSub');
    mPortfolioBtn.addEventListener('click', () => {
      const isOpen = mPortfolioSub.classList.contains('open');
      mPortfolioSub.classList.toggle('open', !isOpen);
      mPortfolioBtn.classList.toggle('active', !isOpen);
    });

    // REVEAL ON SCROLL
    const ro=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');ro.unobserve(e.target);}});},{threshold:0.06});
    document.querySelectorAll('.rv').forEach(el=>ro.observe(el));

    // HERO SLIDESHOW (PROGRESSIVE LAZY-LOADING)
    const slides = document.querySelectorAll('.hero-bg-slide');
    let si = 0;
    const isMobile = window.innerWidth <= 768;

    function ensureSlideImg(slide) {
      if (!slide || slide.querySelector('img')) return;
      const src = isMobile && slide.dataset.mob ? slide.dataset.mob : slide.dataset.src;
      if (src) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = slide.dataset.alt || 'NextGen Architecture and Interior Design';
        img.loading = 'lazy';
        img.decoding = 'async';
        slide.appendChild(img);
      }
    }

    // Preload slide 2 after initial page settles
    setTimeout(() => { if (slides[1]) ensureSlideImg(slides[1]); }, 2000);

    setInterval(() => {
      slides[si].classList.remove('active');
      si = (si + 1) % slides.length;
      ensureSlideImg(slides[si]);
      const nextIdx = (si + 1) % slides.length;
      ensureSlideImg(slides[nextIdx]);
      slides[si].classList.add('active');
    }, 5200);

    // DYNAMIC LAZY-LOAD GOOGLE MAPS ON SCROLL
    (function initLazyMap() {
      const mapWrap = document.querySelector('.map-wrap');
      if (!mapWrap) return;
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
    })();

    // WHATSAPP BUBBLE
    setTimeout(()=>{const wb=document.getElementById('waBubble');wb.style.opacity='1';wb.style.transform='translateY(0)';},2600);

    // HERO TITLE: smooth CSS reveal (no DOM destruction)
    // buildHeroText bypassed to achieve sub-second LCP paint without layout mutation

    // RUNNING PROJECTS AUTO-MARQUEE & LIGHTBOX MODAL
    (function initRunningMarquee() {
      const track = document.getElementById('runningSliderTrack');
      if (!track) return;

      // Duplicate cards dynamically via JS for seamless infinite CSS marquee loop.
      // Cloned elements are marked aria-hidden="true" so search crawlers & screen readers ignore them.
      const originalCards = Array.from(track.children);
      originalCards.forEach(card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        track.appendChild(clone);
      });

      // Pause marquee on hover or touch
      track.addEventListener('mouseenter', () => track.classList.add('is-paused'));
      track.addEventListener('mouseleave', () => {
        if (!modal || !modal.classList.contains('active')) {
          track.classList.remove('is-paused');
        }
      });
      track.addEventListener('touchstart', () => track.classList.add('is-paused'), { passive: true });
      track.addEventListener('touchend', () => {
        if (!modal || !modal.classList.contains('active')) {
          track.classList.remove('is-paused');
        }
      }, { passive: true });

      // Lightbox Modal
      const modal = document.getElementById('runningModal');
      const modalImg = document.getElementById('runningModalImg');
      const modalTitle = document.getElementById('runningModalTitle');
      const modalLoc = document.getElementById('runningModalLoc');
      const modalClose = document.getElementById('runningModalClose');
      const modalWa = document.getElementById('runningModalWa');

      // Use event delegation on track so both original and cloned cards trigger the modal
      track.addEventListener('click', (e) => {
        const card = e.target.closest('.running-card');
        if (!card) return;
        track.classList.add('is-paused');
        const title = card.getAttribute('data-title');
        const loc = card.getAttribute('data-loc');
        const src = card.getAttribute('data-src');
        if (modalImg) modalImg.src = src;
        if (modalTitle) modalTitle.textContent = title;
        if (modalLoc) modalLoc.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg> ${loc}`;
        if (modalWa) {
          modalWa.href = `https://wa.me/9779849151220?text=Hello%20NextGen%2C%20I%20saw%20your%20ongoing%20site%20${encodeURIComponent(title)}%20in%20${encodeURIComponent(loc)}%20and%20would%20like%20to%20enquire.`;
        }
        if (modal) modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      });

      function closeModal() {
        if (modal) modal.classList.remove('active');
        document.body.style.overflow = '';
        track.classList.remove('is-paused');
      }

      if (modalClose) modalClose.addEventListener('click', closeModal);
      if (modal) modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
      });
    })();
