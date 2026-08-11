# -*- coding: utf-8 -*-
"""Single source of truth for the shared page tail.

Everything from the "Get In Touch" contact block downward — contact grid + map,
partner brand marquee, footer and the WhatsApp bubble — lives here so every page
renders it identically. Styling comes from site-common.css, which each page
loads after its own inline <style>.

Consumed by:
  * inject_common_tail.py  — stamps it into the existing static pages
  * build_from_sanity.py   — swaps it into generated project pages
"""

CSS_LINK = '<link rel="stylesheet" href="/site-common.css" />'

# Placeholder that PAGE_TEMPLATE carries; replaced after .format() so the
# braces in this HTML never reach str.format().
TAIL_MARKER = '<!--COMMON_TAIL-->'

PIN_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
           '<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>'
           '<circle cx="12" cy="9" r="2.5"/></svg>')

WA_SVG = ('<svg viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>'
          '<path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.115 1.523 5.845L.057 23.427a.5.5 0 0 0 .606.63l5.7-1.494A11.953 11.953 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.953 9.953 0 0 1-5.17-1.447l-.37-.22-3.38.885.9-3.3-.24-.38A9.964 9.964 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>')

_BRANDS = [
    ("public/Hettich.png", "Hettich"),
    ("public/Surya%20ply.png", "Surya Ply"),
    ("public/Kohler.jpg", "Kohler"),
    ("public/Merino%20Laminates.webp", "Merino Laminates"),
    ("public/Advance%20Laminates.png", "Advance Laminates"),
    ("public/Sagun%20Ply.jpg", "Sagun Ply"),
    ("public/Hafele.png", u"Häfele"),
    ("public/Favicol.png", "Pidilite (Fevicol)"),
    ("public/Greenlam.png", "Greenlam Industries"),
    ("public/Action%20tesa.png", "Action TESA"),
    ("public/Roco.png", "Roca"),
    ("public/Kajaria-Ceramics.webp", "Kajaria Ceramics"),
    ("public/Nitco.png", "NITCO"),
    ("public/Laminam.webp", "Laminam"),
]

# Track is duplicated so the marquee loops seamlessly (keyframe translates -50%).
_LOGO_ITEMS = "\n".join(
    '        <div class="logo-item"><img src="/%s" alt="%s" loading="lazy"/></div>' % (src, alt)
    for src, alt in _BRANDS * 2
)

MAP_EMBED = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d56510.56567813358!2d85.29506209077144"
             "!3d27.720053990615902!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb19ae1ff33c11"
             "%3A0x6942936f55f67bf2!2sNextGen%20interiors%20and%20architects!5e0!3m2!1sen!2snp!4v1777571670970"
             "!5m2!1sen!2snp")

COMMON_TAIL = u'''  <!-- ===== COMMON TAIL (shared across all pages) ===== -->
  <section class="contact sc-section" id="contact">
    <div class="sc-wrap">
      <div class="contact-grid">
        <div>
          <div class="sc-tag rv">Get In Touch</div>
          <div class="contact-head rv">
            <h2>START YOUR<br><span>PROJECT</span></h2>
            <p>Whether it&rsquo;s your dream home, a boutique hotel, or a commercial space &mdash; send us the site details and what you have in mind. We typically share an indicative scope &amp; fee within 5 working days.</p>
          </div>
          <div class="contact-deets rv">
            <a href="tel:+9779849151220" class="cd-item">
              <div class="cd-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="17" height="17"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.09 4.18 2 2 0 0 1 4.08 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div>
              <div><span class="cd-label">Call Us</span><span class="cd-val">+977 9849151220</span></div>
            </a>
            <!--email_off--><a href="mailto:info@nextgeninterior.com" class="cd-item">
              <div class="cd-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="17" height="17"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg></div>
              <div><span class="cd-label">Email Us</span><span class="cd-val">info@nextgeninterior.com</span></div>
            </a><!--/email_off-->
            <div class="cd-item">
              <div class="cd-icon">''' + PIN_SVG.replace('stroke-width="2"', 'stroke-width="1.8" width="17" height="17"') + u'''</div>
              <div><span class="cd-label">Head Office</span><span class="cd-val">Baluwatar, Kathmandu</span></div>
            </div>
          </div>
          <div class="service-locations rv">
            <div class="service-locations-label">We Serve</div>
            <div class="location-tags">
              <span class="location-tag">''' + PIN_SVG + u'''All Over Nepal</span>
            </div>
          </div>
          <div class="contact-socials rv">
            <a href="https://www.instagram.com/nextgen_interiors_architects?igsh=OGtuYjZhbmUzamgy" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="18" height="18"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><circle cx="12" cy="12" r="4.5"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>
            <a href="https://www.facebook.com/architectsandinteriorshouse" target="_blank" rel="noopener" aria-label="Facebook" title="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
            <a href="https://www.linkedin.com/company/nextgen-interiors-architects-pvt-ltd/?originalSubdomain=np" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
            <a href="https://www.youtube.com/@nextgeninteriors" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46a2.78 2.78 0 0 0-1.95 1.96A29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58 2.78 2.78 0 0 0 1.95 1.96C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.96A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58z"/><polygon fill="white" points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02"/></svg></a>
            <a href="https://wa.me/9779849151220" target="_blank" rel="noopener" style="background:rgba(37,211,102,0.12);border-color:rgba(37,211,102,0.28);color:#25d366;" aria-label="WhatsApp" title="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.115 1.523 5.845L.057 23.427a.5.5 0 0 0 .606.63l5.7-1.494A11.953 11.953 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.953 9.953 0 0 1-5.17-1.447l-.37-.22-3.38.885.9-3.3-.24-.38A9.964 9.964 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg></a>
          </div>
        </div>
        <div class="map-wrap rv d1">
          <div class="map-label">''' + PIN_SVG.replace('stroke-width="2"', 'stroke-width="2" width="13" height="13"') + u'''NextGen Interiors &amp; Architects</div>
          <iframe src="''' + MAP_EMBED + u'''" title="NextGen Interiors &amp; Architects on Google Maps" loading="lazy" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </div>
  </section>

  <section class="partners-section" id="partners">
    <div class="sc-wrap">
      <div class="partners-eyebrow rv">Trusted Partner Brands</div>
      <h2 class="partners-title rv">We Build With The <em>Best</em></h2>
    </div>
    <div class="logo-marquee">
      <div class="logo-track">
''' + _LOGO_ITEMS + u'''
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="sc-wrap">
      <div class="footer-inner">
        <div class="footer-logo"><img src="/logo/logo.png" class="logo-img" alt="NextGen Interiors" style="height:30px;"/></div>
        <p class="footer-copy">&copy; 2025 NextGen Interiors &amp; Architects &middot; Baluwatar, Kathmandu, Nepal</p>
        <div class="footer-socials">
          <a href="https://www.instagram.com/nextgen_interiors_architects?igsh=OGtuYjZhbmUzamgy" target="_blank" rel="noopener">Instagram</a>
          <a href="https://www.facebook.com/architectsandinteriorshouse" target="_blank" rel="noopener">Facebook</a>
          <a href="https://www.linkedin.com/company/nextgen-interiors-architects-pvt-ltd/?originalSubdomain=np" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://www.youtube.com/@nextgeninteriors" target="_blank" rel="noopener">YouTube</a>
        </div>
      </div>
    </div>
  </footer>

  <div class="wa-bubble">
    <div class="wa-tooltip">Chat with us on WhatsApp!</div>
    <a href="https://wa.me/9779849151220?text=Hello%20NextGen%20Interiors%2C%20I%27d%20like%20to%20discuss%20a%20project." class="wa-btn" target="_blank" rel="noopener" aria-label="WhatsApp">''' + WA_SVG + u'''</a>
  </div>
  <!-- ===== /COMMON TAIL ===== -->
'''
