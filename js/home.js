    // CURSOR (Removed)
    document.querySelectorAll('.cursor-dot, .cursor-ring, #cursorDot, #cursorRing').forEach(el => el.remove());



    // NAV SCROLL
    window.addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',window.scrollY>60));

    // MOBILE MENU
    const btn=document.getElementById('menuBtn'),mm=document.getElementById('mMenu');
    function openMenu(){
      mm.style.display='grid';
      requestAnimationFrame(()=>{btn.classList.add('open');mm.classList.add('open');document.body.style.overflow='hidden';});
    }
    function closeMenu(){
      btn.classList.remove('open');mm.classList.remove('open');document.body.style.overflow='';
      setTimeout(()=>{if(!mm.classList.contains('open')) mm.style.display='none';}, 550);
    }
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

    // HERO SLIDESHOW (PROGRESSIVE LAZY-LOADING WITH SEAMLESS CROSSFADE)
    const slides = document.querySelectorAll('.hero-bg-slide');
    let si = 0;

    function ensureSlideImg(slide) {
      if (!slide || slide.querySelector('img') || !slide.dataset.src) return;
      const pic = document.createElement('picture');
      if (slide.dataset.mob) {
        const srcMob = document.createElement('source');
        srcMob.media = '(max-width: 768px)';
        srcMob.srcset = slide.dataset.mob;
        pic.appendChild(srcMob);
      }
      const img = document.createElement('img');
      img.src = slide.dataset.src;
      img.alt = slide.dataset.alt || 'NextGen Architecture and Interior Design';
      img.decoding = 'async';
      img.width = 1600;
      img.height = 1131;
      pic.appendChild(img);
      slide.appendChild(pic);
    }

    // Preload slide 1 shortly after page load
    setTimeout(() => {
      if (slides.length > 1) ensureSlideImg(slides[1]);
    }, 600);

    function nextHeroSlide() {
      if (slides.length <= 1) return;
      const prevIdx = si;
      const nextIdx = (si + 1) % slides.length;

      ensureSlideImg(slides[nextIdx]);
      const upcomingIdx = (nextIdx + 1) % slides.length;
      ensureSlideImg(slides[upcomingIdx]);

      const prevSlide = slides[prevIdx];
      const nextSlide = slides[nextIdx];

      // Keep previous slide visible underneath while new slide fades in on top
      prevSlide.classList.add('prev');
      prevSlide.classList.remove('active');
      nextSlide.classList.add('active');

      setTimeout(() => {
        prevSlide.classList.remove('prev');
      }, 1800);

      si = nextIdx;
    }

    setInterval(nextHeroSlide, 5200);

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

    // HERO CHAR-BY-CHAR BLUR REVEAL
    (function buildHeroText() {
      const line1 = document.getElementById('heroLine1');
      const line2 = document.getElementById('heroLine2');
      if (!line1 || !line2) return;

      const lines = [
        { el: line1, words: ['CRAFTING', 'VISIONS,'], accentWord: -1 },
        { el: line2, words: ['BUILDING', 'DREAMS'],  accentWord: 1  }
      ];
      const BASE = 0.25;
      const CHAR_STEP = 0.038;
      const LINE_OFFSET = 0.08;
      let idx = 0;
      lines.forEach((line, li) => {
        line.el.textContent = '';
        line.words.forEach((word, wi) => {
          if (wi > 0) {
            const sp = document.createElement('span');
            sp.className = 'hw-space';
            line.el.appendChild(sp);
          }
          const hw = document.createElement('span');
          hw.className = 'hw';
          if (wi === line.accentWord) hw.style.color = 'var(--blue-mid)';
          Array.from(word).forEach(ch => {
            const hc = document.createElement('span');
            hc.className = 'hc';
            hc.textContent = ch;
            hc.style.animationDelay = (BASE + li * LINE_OFFSET + idx * CHAR_STEP).toFixed(3) + 's';
            hw.appendChild(hc);
            idx++;
          });
          line.el.appendChild(hw);
        });
      });
    })();

    
    // FAQ ACCORDION DROPDOWN
    (function initFAQAccordion() {
      const faqItems = document.querySelectorAll('.faq-item');
      faqItems.forEach(item => {
        const btn = item.querySelector('.faq-q-btn');
        if (!btn) return;
        btn.addEventListener('click', () => {
          const isActive = item.classList.contains('is-active');
          faqItems.forEach(other => {
            other.classList.remove('is-active');
            const otherBtn = other.querySelector('.faq-q-btn');
            if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
          });
          if (!isActive) {
            item.classList.add('is-active');
            btn.setAttribute('aria-expanded', 'true');
          }
        });
      });
    })();

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
        if (modal) {
          modal.style.display = 'flex';
          requestAnimationFrame(() => modal.classList.add('active'));
        }
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
