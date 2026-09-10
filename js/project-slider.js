// NextGen Interiors & Architects — featured & contextual project slider
(function () {
  'use strict';

  var AUTOPLAY_MS = 3800;
  var DRAG_THRESHOLD = 50;

  function init(root, sliderIdx) {
    var viewport = root.querySelector('.pslider-viewport');
    var track = root.querySelector('.pslider-track');
    var allSlides = Array.prototype.slice.call(root.querySelectorAll('.pslide'));
    if (!viewport || !track || !allSlides.length) return;

    var filterWrap = root.querySelector('.pslider-filters') || (root.parentElement && root.parentElement.querySelector('.pslider-filters'));
    var filterBtns = filterWrap ? Array.prototype.slice.call(filterWrap.querySelectorAll('[data-filter]')) : [];

    var dotsWrap = root.querySelector('.pslider-dots');
    var catLabel = root.querySelector('.pslider-cat');
    var counter = root.querySelector('.pslider-count');
    var prevBtn = root.querySelector('[data-pslider="prev"]');
    var nextBtn = root.querySelector('[data-pslider="next"]');

    var reduceMotion = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var slides = allSlides.slice();
    var index = 0;
    for (var i = 0; i < slides.length; i++) {
      if (slides[i].getAttribute('data-featured') === 'true') { index = i; break; }
    }

    var timer = null;
    var paused = false;
    var dragging = false;
    var pointerId = null;
    var startX = 0;
    var deltaX = 0;
    var baseX = 0;
    var dots = [];

    function buildDots() {
      if (!dotsWrap) return;
      dotsWrap.innerHTML = '';
      dots = [];
      slides.forEach(function (slide, i) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'pslider-dot';
        dot.setAttribute('role', 'tab');
        dot.setAttribute('aria-label', slide.getAttribute('data-name') || ('Project ' + (i + 1)));
        dot.addEventListener('click', function () { go(i, true); });
        dotsWrap.appendChild(dot);
        dots.push(dot);
      });
    }
    buildDots();

    function offsetFor(i) {
      if (!slides[i]) return 0;
      var slide = slides[i];
      return (viewport.clientWidth / 2) - (slide.offsetLeft + (slide.offsetWidth / 2));
    }

    function paint(x, animate) {
      track.style.transition = (animate && !reduceMotion)
        ? 'transform .85s cubic-bezier(.16,1,.3,1)'
        : 'none';
      track.style.transform = 'translate3d(' + Math.round(x) + 'px,0,0)';
    }

    function render(animate) {
      if (!slides.length) return;
      if (index >= slides.length) index = 0;
      if (index < 0) index = slides.length - 1;

      baseX = offsetFor(index);
      paint(baseX, animate !== false);

      allSlides.forEach(function (s) { s.classList.remove('is-active'); });
      if (slides[index]) slides[index].classList.add('is-active');

      dots.forEach(function (dot, i) {
        dot.classList.toggle('is-active', i === index);
        dot.setAttribute('aria-selected', i === index ? 'true' : 'false');
      });
      if (catLabel && slides[index]) {
        catLabel.textContent = slides[index].getAttribute('data-category') || '';
      }
      if (counter) {
        counter.textContent = String(index + 1).padStart(2, '0') + ' / ' +
          String(slides.length).padStart(2, '0');
      }
    }

    function go(i, userInitiated) {
      if (!slides.length) return;
      index = (i + slides.length) % slides.length;
      render(true);
      if (userInitiated) restart();
    }

    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    function start() {
      stop();
      if (reduceMotion || slides.length < 2) return;
      var delay = AUTOPLAY_MS + ((sliderIdx || 0) % 3) * 400;
      timer = setInterval(function () {
        if (!paused && !dragging && !document.hidden) go(index + 1);
      }, delay);
    }

    function restart() { start(); }
    function pause() { paused = true; }
    function resume() { paused = false; }

    root.addEventListener('mouseenter', pause);
    root.addEventListener('mouseleave', resume);
    root.addEventListener('focusin', pause);
    root.addEventListener('focusout', function (e) {
      if (!root.contains(e.relatedTarget)) resume();
    });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop(); else start();
    });

    if (prevBtn) prevBtn.addEventListener('click', function () { go(index - 1, true); });
    if (nextBtn) nextBtn.addEventListener('click', function () { go(index + 1, true); });

    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { go(index - 1, true); }
      else if (e.key === 'ArrowRight') { go(index + 1, true); }
    });

    // Category filter tabs support
    if (filterBtns.length) {
      filterBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var targetFilter = btn.getAttribute('data-filter');
          filterBtns.forEach(function (b) { b.classList.remove('is-active'); });
          btn.classList.add('is-active');

          allSlides.forEach(function (s) {
            var cat = (s.getAttribute('data-group') || '').toLowerCase();
            if (targetFilter === 'all' || cat.indexOf(targetFilter.toLowerCase()) !== -1) {
              s.style.display = '';
            } else {
              s.style.display = 'none';
            }
          });

          slides = allSlides.filter(function (s) {
            return s.style.display !== 'none';
          });

          index = 0;
          buildDots();
          render(false);
          restart();
        });
      });
    }

    // Touch & Pointer drag
    var moved = false;

    viewport.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      dragging = true;
      moved = false;
      pointerId = e.pointerId;
      startX = e.clientX;
      deltaX = 0;
      track.style.transition = 'none';
      if (viewport.setPointerCapture) viewport.setPointerCapture(pointerId);
    });

    viewport.addEventListener('pointermove', function (e) {
      if (!dragging || e.pointerId !== pointerId) return;
      deltaX = e.clientX - startX;
      if (Math.abs(deltaX) > 4) moved = true;
      paint(baseX + deltaX, false);
    });

    function endDrag(e) {
      if (!dragging || (e && e.pointerId !== pointerId)) return;
      dragging = false;
      if (pointerId !== null && viewport.hasPointerCapture &&
          viewport.hasPointerCapture(pointerId)) {
        viewport.releasePointerCapture(pointerId);
      }
      pointerId = null;
      if (deltaX <= -DRAG_THRESHOLD) go(index + 1, true);
      else if (deltaX >= DRAG_THRESHOLD) go(index - 1, true);
      else render(true);
      deltaX = 0;
    }

    viewport.addEventListener('pointerup', endDrag);
    viewport.addEventListener('pointercancel', endDrag);

    allSlides.forEach(function (slide) {
      slide.addEventListener('click', function (e) {
        if (moved) { e.preventDefault(); moved = false; return; }
        var currentActiveIdx = slides.indexOf(slide);
        if (currentActiveIdx !== -1 && currentActiveIdx !== index) {
          e.preventDefault();
          go(currentActiveIdx, true);
        }
      });
    });

    var resizeTimer = null;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () { render(false); }, 120);
    });

    window.addEventListener('load', function () { render(false); });

    root.classList.add('is-ready');
    render(false);
    start();
  }

  function boot() {
    var sliders = Array.prototype.slice.call(document.querySelectorAll('[data-project-slider]'));
    sliders.forEach(function (slider, idx) {
      init(slider, idx);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
