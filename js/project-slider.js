// NextGen Interiors & Architects — featured project slider
//
// Drives the "Our Interesting Projects" showcase. The slides themselves are
// rendered into the HTML by build_from_sanity.py, so every project name,
// category, location and link is crawlable with JavaScript switched off — this
// file only adds the motion.
//
// Movement is done entirely with transform and opacity so the animation stays
// on the compositor, matching the rest of the site's PageSpeed work. Slide
// widths never change; the centre slide is scaled up instead, which keeps the
// layout maths stable while still reading as a larger featured card.
(function () {
  'use strict';

  var AUTOPLAY_MS = 3800;
  var DRAG_THRESHOLD = 55;

  function init(root) {
    var viewport = root.querySelector('.pslider-viewport');
    var track = root.querySelector('.pslider-track');
    var slides = Array.prototype.slice.call(root.querySelectorAll('.pslide'));
    if (!viewport || !track || !slides.length) return;

    var dotsWrap = root.querySelector('.pslider-dots');
    var catLabel = root.querySelector('.pslider-cat');
    var counter = root.querySelector('.pslider-count');
    var prevBtn = root.querySelector('[data-pslider="prev"]');
    var nextBtn = root.querySelector('[data-pslider="next"]');

    var reduceMotion = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

    // ---- dots -------------------------------------------------------------
    var dots = [];
    if (dotsWrap) {
      dotsWrap.innerHTML = '';
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

    // ---- positioning ------------------------------------------------------
    function offsetFor(i) {
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
      baseX = offsetFor(index);
      paint(baseX, animate !== false);

      slides.forEach(function (slide, i) {
        slide.classList.toggle('is-active', i === index);
      });
      dots.forEach(function (dot, i) {
        dot.classList.toggle('is-active', i === index);
        dot.setAttribute('aria-selected', i === index ? 'true' : 'false');
      });
      if (catLabel) catLabel.textContent = slides[index].getAttribute('data-category') || '';
      if (counter) {
        counter.textContent = String(index + 1).padStart(2, '0') + ' / ' +
          String(slides.length).padStart(2, '0');
      }
    }

    function go(i, userInitiated) {
      index = (i + slides.length) % slides.length;
      render(true);
      if (userInitiated) restart();
    }

    // ---- autoplay ---------------------------------------------------------
    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    function start() {
      stop();
      if (reduceMotion || slides.length < 2) return;
      timer = setInterval(function () {
        if (!paused && !dragging && !document.hidden) go(index + 1);
      }, AUTOPLAY_MS);
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

    // ---- pointer drag / touch swipe ---------------------------------------
    // The slides are links, so a drag must not fire a navigation. Movement past
    // a few pixels sets a flag that the click handler below cancels on.
    var moved = false;

    viewport.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      dragging = true;
      moved = false;
      pointerId = e.pointerId;
      startX = e.clientX;
      deltaX = 0;
      track.style.transition = 'none';
      viewport.setPointerCapture(pointerId);
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

    slides.forEach(function (slide, i) {
      slide.addEventListener('click', function (e) {
        if (moved) { e.preventDefault(); moved = false; return; }
        // A click on a side card brings it to the centre rather than navigating,
        // which is what people expect from a carousel of this shape.
        if (i !== index) { e.preventDefault(); go(i, true); }
      });
    });

    // ---- lifecycle --------------------------------------------------------
    var resizeTimer = null;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () { render(false); }, 120);
    });

    // Images settle after load and change offsetLeft; re-measure once they have.
    window.addEventListener('load', function () { render(false); });

    root.classList.add('is-ready');
    render(false);
    start();
  }

  function boot() {
    Array.prototype.slice
      .call(document.querySelectorAll('[data-project-slider]'))
      .forEach(init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
