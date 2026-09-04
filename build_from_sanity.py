import os
import re
import glob
import json
import urllib.request
import urllib.parse

from copy_clean import clean_text
from optimize_meta import shorten_description

PROJECT_ID = "gpyk0ky0"
DATASET = "production"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <link rel="icon" type="image/png" sizes="32x32" href="/logo/favicon.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/logo/favicon.png" />
  <link rel="shortcut icon" href="/logo/favicon.png" />
  <link rel="apple-touch-icon" href="/logo/favicon.png" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{page_title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://nextgeninterior.com/{slug}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="NextGen Architects and Interiors" />
  <meta name="theme-color" content="#0d1520" />
  <meta name="geo.region" content="NP" />
  <meta name="geo.placename" content="Kathmandu, Nepal" />
  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="NextGen Architects and Interiors" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:title" content="{page_title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://nextgeninterior.com/{slug}" />
  <meta property="og:image" content="{hero_image}" />
  <meta property="og:image:alt" content="{title} — NextGen Interiors &amp; Architects" />
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{page_title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{hero_image}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet">
  <style>
    :root{{--blue-dark:#1a3d6e;--blue:#2969a6;--blue-mid:#369fce;--ink:#0d1520;--offwhite:#f5f2ed;--mist:#8a97aa;--f-head:'Bebas Neue',sans-serif;--f-body:'Poppins',sans-serif;--ease:cubic-bezier(0.16,1,0.3,1);--gap:clamp(20px,5vw,80px);--max:1440px;}}
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
    html{{scroll-behavior:smooth;}}
    body{{font-family:var(--f-body);background:var(--ink);color:var(--offwhite);overflow-x:hidden;cursor:none;}}
    img{{display:block;width:100%;height:100%;object-fit:cover;}}
    .logo-img{{display:block;width:auto!important;height:100%!important;object-fit:contain!important;}}
    a{{text-decoration:none;color:inherit;}}
    button{{border:none;background:none;cursor:none;font:inherit;}}
    ul{{list-style:none;}}
    ::-webkit-scrollbar{{width:3px;}}
    ::-webkit-scrollbar-track{{background:var(--ink);}}
    ::-webkit-scrollbar-thumb{{background:var(--blue-mid);}}
    .cursor-dot{{width:7px;height:7px;border-radius:50%;background:var(--blue-mid);position:fixed;top:0;left:0;transform:translate(-50%,-50%);z-index:9999;pointer-events:none;transition:width .2s,height .2s;mix-blend-mode:screen;}}
    .cursor-ring{{width:36px;height:36px;border-radius:50%;border:1px solid rgba(62,159,201,0.35);position:fixed;top:0;left:0;transform:translate(-50%,-50%);z-index:9998;pointer-events:none;transition:width .35s var(--ease),height .35s var(--ease),opacity .3s;}}
    body.c-hover .cursor-dot{{width:52px;height:52px;opacity:0.15;}}
    body.c-hover .cursor-ring{{opacity:0;}}
    .nav{{position:fixed;top:0;left:0;right:0;z-index:200;padding:22px var(--gap);display:flex;align-items:center;justify-content:space-between;background:rgba(13,21,32,0.96);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,0.05);}}
    .nav-logo{{height:34px;display:flex;align-items:center;}}
    .nav-links{{display:flex;gap:32px;align-items:center;}}
    .nav-links>li{{position:relative;}}
    .nav-links a,.nav-dropdown-trigger{{font-family:var(--f-body);font-size:11px;font-weight:500;letter-spacing:0.16em;text-transform:uppercase;color:rgba(245,242,237,0.45);transition:color .3s;display:flex;align-items:center;gap:5px;cursor:none;position:relative;}}
    .nav-links a::after{{content:'';position:absolute;bottom:-3px;left:0;width:0;height:1px;background:var(--blue-mid);transition:width .4s var(--ease);}}
    .nav-links a:hover,.nav-links a.active{{color:var(--offwhite);}}
    .nav-links a.active::after,.nav-links a:hover::after{{width:100%;}}
    .nav-dropdown-trigger{{background:none;border:none;padding:0;}}
    .nav-dropdown-trigger svg{{width:10px;height:10px;transition:transform .3s var(--ease);}}
    .nav-links>li:hover .nav-dropdown-trigger{{color:var(--offwhite);}}
    .nav-links>li:hover .nav-dropdown-trigger svg{{transform:rotate(180deg);}}
    .nav-dropdown-wrap{{position:absolute;top:100%;left:50%;transform:translateX(-50%);padding-top:14px;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .28s var(--ease),visibility .28s;z-index:300;}}
    .nav-links>li:hover .nav-dropdown-wrap{{opacity:1;visibility:visible;pointer-events:all;}}
    .nav-dropdown{{background:rgba(8,14,24,0.98);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.08);border-top:2px solid var(--blue-mid);min-width:220px;transform:translateY(6px);transition:transform .28s var(--ease);box-shadow:0 20px 60px rgba(0,0,0,0.5);}}
    .nav-links>li:hover .nav-dropdown{{transform:translateY(0);}}
    .nav-dropdown a{{display:flex;align-items:center;gap:10px;padding:14px 22px;font-family:var(--f-body);font-size:10.5px;font-weight:500;letter-spacing:0.16em;text-transform:uppercase;color:rgba(245,242,237,0.45);border-bottom:1px solid rgba(255,255,255,0.04);transition:color .22s,background .22s,padding-left .22s;white-space:nowrap;}}
    .nav-dropdown a::before{{content:'';width:0;height:1px;background:var(--blue-mid);transition:width .3s var(--ease);flex-shrink:0;}}
    .nav-dropdown a:last-child{{border-bottom:none;}}
    .nav-dropdown a::after{{display:none!important;}}
    .nav-dropdown a:hover{{color:var(--blue-mid);background:rgba(54,159,206,0.05);padding-left:28px;}}
    .nav-dropdown a:hover::before{{width:12px;}}
    .nav-dropdown a.active{{color:var(--blue-mid);}}
    .nav-cta{{font-family:var(--f-body);font-size:11px;font-weight:500;letter-spacing:0.14em;text-transform:uppercase;color:rgba(245,242,237,0.4);transition:color .3s;}}
    .nav-cta:hover{{color:var(--blue-mid);}}
    .nav-menu-btn{{display:none;flex-direction:column;gap:6px;width:26px;cursor:none;}}
    .nav-menu-btn span{{display:block;width:100%;height:1px;background:var(--offwhite);transition:transform .4s var(--ease),opacity .3s;}}
    .nav-menu-btn.open span:nth-child(1){{transform:translateY(7px) rotate(45deg);}}
    .nav-menu-btn.open span:nth-child(2){{opacity:0;}}
    .nav-menu-btn.open span:nth-child(3){{transform:translateY(-7px) rotate(-45deg);}}
    .m-menu{{position:fixed;inset:0;z-index:190;background:#080f1c;display:grid;grid-template-rows:auto 1fr auto;opacity:0;visibility:hidden;transition:opacity .55s var(--ease),visibility .55s;overflow-y:auto;}}
    .m-menu.open{{opacity:1;visibility:visible;}}
    .m-menu-topbar{{display:flex;align-items:center;justify-content:space-between;padding:22px var(--gap);border-bottom:1px solid rgba(255,255,255,0.05);}}
    .m-menu-body{{padding:32px var(--gap) 24px;}}
    .m-menu-links>li{{border-bottom:1px solid rgba(255,255,255,0.06);}}
    .m-menu-links a,.m-menu-links .m-menu-acc-btn{{font-family:var(--f-head);font-size:clamp(36px,8vw,60px);letter-spacing:0.05em;color:rgba(245,242,237,0.85);display:flex;align-items:center;justify-content:space-between;line-height:1;padding:18px 0;transform:translateY(20px);opacity:0;transition:transform .55s var(--ease),opacity .55s var(--ease),color .25s;background:none;border:none;cursor:none;width:100%;}}
    .m-menu.open .m-menu-links a,.m-menu.open .m-menu-links .m-menu-acc-btn{{transform:translateY(0);opacity:1;}}
    .m-menu-links a:hover,.m-menu-acc-btn.active{{color:var(--blue-mid);}}
    .m-acc-chevron{{width:22px;height:22px;flex-shrink:0;border:1px solid rgba(255,255,255,0.12);display:flex;align-items:center;justify-content:center;transition:transform .35s var(--ease),border-color .3s;}}
    .m-acc-chevron svg{{width:12px;height:12px;color:var(--mist);}}
    .m-menu-acc-btn.active .m-acc-chevron{{transform:rotate(180deg);border-color:var(--blue-mid);}}
    .m-acc-sub{{max-height:0;overflow:hidden;transition:max-height .45s var(--ease);}}
    .m-acc-sub.open{{max-height:600px;}}
    .m-acc-sub-inner{{padding:6px 0 16px;display:grid;grid-template-columns:1fr 1fr;gap:4px;}}
    .m-acc-sub a{{font-family:var(--f-body)!important;font-size:11px!important;font-weight:500;letter-spacing:0.14em;text-transform:uppercase;color:rgba(245,242,237,0.4)!important;padding:12px 14px!important;display:flex!important;align-items:center;gap:8px;transform:none!important;opacity:1!important;border:1px solid rgba(255,255,255,0.05)!important;transition:color .2s,border-color .2s,background .2s!important;}}
    .m-acc-sub a::before{{content:'';width:5px;height:1px;background:currentColor;flex-shrink:0;}}
    .m-acc-sub a:hover,.m-acc-sub a.active{{color:var(--blue-mid)!important;border-color:rgba(54,159,206,0.25)!important;}}
    .m-menu-footer{{padding:20px var(--gap) 32px;border-top:1px solid rgba(255,255,255,0.06);display:flex;flex-direction:column;gap:14px;opacity:0;transform:translateY(10px);transition:opacity .5s var(--ease) .3s,transform .5s var(--ease) .3s;}}
    .m-menu.open .m-menu-footer{{opacity:1;transform:translateY(0);}}
    .m-service-label{{font-family:var(--f-body);font-size:9px;font-weight:600;letter-spacing:0.3em;text-transform:uppercase;color:var(--mist);margin-bottom:6px;}}
    .m-service-pill{{display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border:1px solid rgba(54,159,206,0.2);font-family:var(--f-body);font-size:9px;font-weight:500;letter-spacing:0.14em;text-transform:uppercase;color:var(--blue-mid);}}
    .m-service-pill svg{{width:8px;height:8px;}}
    .m-hq-row{{display:flex;align-items:center;gap:8px;font-family:var(--f-body);font-size:10px;color:rgba(245,242,237,0.35);margin-top:6px;}}
    .m-hq-dot{{width:5px;height:5px;border-radius:50%;background:var(--blue-mid);flex-shrink:0;}}
    .m-contact-row{{display:flex;flex-direction:column;gap:4px;}}
    .m-contact-row a{{font-family:var(--f-body);font-size:12px;color:rgba(245,242,237,0.5);transition:color .25s;transform:none!important;opacity:1!important;}}
    .m-contact-row a:hover{{color:var(--blue-mid);}}
    .hero{{position:relative;height:100svh;min-height:600px;overflow:hidden;display:flex;align-items:flex-end;}}
    .hero-img{{position:absolute;inset:0;z-index:0;}}
    .hero-img img{{width:100%;height:100%;object-fit:cover;transform:scale(1.05);animation:kenBurns 18s ease-in-out infinite alternate;}}
    @keyframes kenBurns{{from{{transform:scale(1.05)}}to{{transform:scale(1.0) translate(-0.8%,0.8%)}}}}
    .hero-overlay{{position:absolute;inset:0;z-index:1;background:linear-gradient(to top,rgba(13,21,32,0.92) 0%,rgba(13,21,32,0.3) 50%,rgba(13,21,32,0.4) 100%);}}
    .hero-content{{position:relative;z-index:2;padding:0 var(--gap) clamp(50px,8vw,100px);width:100%;}}
    .hero-eyebrow{{display:flex;align-items:center;gap:12px;font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:0.35em;text-transform:uppercase;color:var(--blue-mid);margin-bottom:16px;opacity:0;animation:fadeUp .7s var(--ease) .3s forwards;}}
    .hero-eyebrow::before{{content:'';width:20px;height:1px;background:var(--blue-mid);}}
    .hero-h1{{font-family:var(--f-head);font-size:clamp(60px,10vw,140px);letter-spacing:0.06em;line-height:0.9;color:var(--offwhite);text-shadow:0 4px 40px rgba(0,0,0,0.5);opacity:0;animation:fadeUp .8s var(--ease) .5s forwards;}}
    .hero-h1 span{{color:var(--blue-mid);}}
    .hero-meta{{display:flex;align-items:center;gap:32px;margin-top:28px;opacity:0;animation:fadeUp .7s var(--ease) .75s forwards;flex-wrap:wrap;}}
    .hero-meta-item{{display:flex;flex-direction:column;gap:3px;}}
    .meta-label{{font-size:9px;font-weight:600;letter-spacing:0.25em;text-transform:uppercase;color:var(--mist);}}
    .meta-val{{font-size:13px;font-weight:400;color:var(--offwhite);}}
    .hero-meta-div{{width:1px;height:36px;background:rgba(255,255,255,0.12);}}
    .scroll-hint{{position:absolute;bottom:clamp(28px,5vh,50px);right:var(--gap);z-index:2;display:flex;flex-direction:column;align-items:center;gap:8px;opacity:0;animation:fadeIn .8s ease 1.2s forwards;}}
    .scroll-track{{width:1px;height:48px;background:rgba(255,255,255,0.1);position:relative;overflow:hidden;}}
    .scroll-fill{{position:absolute;top:-40%;left:0;right:0;height:40%;background:var(--blue-mid);animation:scrollDrop 2s ease-in-out infinite;}}
    @keyframes scrollDrop{{0%{{top:-40%}}100%{{top:110%}}}}
    .scroll-word{{font-size:9px;letter-spacing:0.22em;text-transform:uppercase;color:rgba(255,255,255,0.3);writing-mode:vertical-rl;}}
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:none}}}}
    @keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
    .rv{{opacity:0;transform:translateY(28px);transition:opacity .9s var(--ease),transform .9s var(--ease);}}
    .rv.vis{{opacity:1;transform:none;}}
    .rv.d1{{transition-delay:.1s}}.rv.d2{{transition-delay:.2s}}.rv.d3{{transition-delay:.3s}}.rv.d4{{transition-delay:.4s}}
    .s-intro{{padding:clamp(70px,10vw,130px) var(--gap) clamp(40px,5vw,70px);max-width:var(--max);margin:0 auto;}}
    .s-tag{{font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:0.3em;text-transform:uppercase;color:var(--blue-mid);display:flex;align-items:center;gap:10px;margin-bottom:14px;}}
    .s-tag::before{{content:'';width:18px;height:1px;background:var(--blue-mid);}}
    .s-intro-grid{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:end;}}
    .s-intro-h{{font-family:var(--f-head);font-size:clamp(48px,5.5vw,80px);letter-spacing:0.05em;line-height:0.92;color:var(--offwhite);}}
    .s-intro-body{{font-size:13px;font-weight:300;line-height:1.9;color:var(--mist);max-width:460px;}}
    .s-intro-body p+p{{margin-top:14px;}}
    
    /* SANKHU STYLE LARGE DYNAMIC SHOWCASE */
    .gallery{{background:var(--ink);}}
    .g-full{{width:100%;height:clamp(380px,68vh,820px);overflow:hidden;position:relative;}}
    .g-half{{display:grid;grid-template-columns:1fr 1fr;gap:4px;}}
    .g-feature{{display:grid;grid-template-columns:2fr 1fr;gap:4px;}}
    .g-feature-rev{{display:grid;grid-template-columns:1fr 2fr;gap:4px;}}
    .g-trio{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;}}
    .g-card{{position:relative;overflow:hidden;background:#080f1c;cursor:none;display:block;}}
    .g-card img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--ease);}}
    .g-card:hover img{{transform:scale(1.06);}}
    .g-card-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(8,14,28,0.75) 0%,transparent 55%);z-index:1;opacity:0;transition:opacity .5s;}}
    .g-card:hover .g-card-overlay{{opacity:1;}}
    .g-card-label{{position:absolute;bottom:0;left:0;right:0;z-index:2;padding:20px 24px;transform:translateY(8px);opacity:0;transition:all .45s var(--ease);}}
    .g-card:hover .g-card-label{{transform:translateY(0);opacity:1;}}
    .g-card-label span{{font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:var(--blue-mid);}}
    .g-card::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--blue-mid);transform:scaleX(0);transform-origin:left;transition:transform .5s var(--ease);z-index:3;}}
    .g-card:hover::after{{transform:scaleX(1);}}
    .ar-wide{{height:clamp(360px,58vh,720px);}}.ar-43{{height:clamp(380px,64vh,780px);}}.ar-32{{height:clamp(360px,60vh,740px);}}.ar-sq{{height:clamp(400px,68vh,820px);}}
    
    /* LIGHTBOX */
    .lb{{position:fixed;inset:0;z-index:9500;background:rgba(8,12,20,0.97);display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:opacity .4s,visibility .4s;}}
    .lb.open{{opacity:1;visibility:visible;}}
    .lb-img-wrap{{position:relative;max-width:92vw;max-height:90vh;}}
    .lb-img-wrap img{{max-width:92vw;max-height:88vh;object-fit:contain;width:auto;height:auto;display:block;}}
    .lb-close{{position:absolute;top:-44px;right:0;width:36px;height:36px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:rgba(255,255,255,0.5);transition:color .3s;}}
    .lb-close:hover{{color:var(--blue-mid);}}
    .lb-close svg{{width:22px;height:22px;}}
    .lb-prev,.lb-next{{position:fixed;top:50%;transform:translateY(-50%);width:52px;height:52px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;cursor:pointer;color:rgba(255,255,255,0.5);transition:all .3s;z-index:9501;}}
    .lb-prev{{left:20px;}}.lb-next{{right:20px;}}
    .lb-prev:hover,.lb-next:hover{{border-color:var(--blue-mid);color:var(--blue-mid);background:rgba(54,159,206,0.1);}}
    .lb-prev svg,.lb-next svg{{width:22px;height:22px;}}
    .lb-counter{{position:fixed;bottom:28px;left:50%;transform:translateX(-50%);font-family:var(--f-body);font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:rgba(255,255,255,0.3);z-index:9501;}}
    
    .cta-strip{{padding:clamp(60px,8vw,110px) var(--gap);text-align:center;max-width:var(--max);margin:0 auto;}}
    .cta-h{{font-family:var(--f-head);font-size:clamp(44px,5vw,76px);letter-spacing:0.05em;color:var(--offwhite);margin-bottom:20px;}}
    .cta-h span{{color:var(--blue-mid);}}
    .cta-p{{font-size:13px;font-weight:300;color:var(--mist);max-width:440px;margin:0 auto 36px;line-height:1.85;}}
    .cta-btns{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}}
    .btn-primary{{display:inline-flex;align-items:center;gap:10px;padding:16px 36px;background:var(--blue-mid);color:#fff;font-family:var(--f-body);font-size:11px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;transition:background .3s;cursor:none;}}
    .btn-primary:hover{{background:var(--blue);}}
    .btn-outline{{display:inline-flex;align-items:center;gap:10px;padding:15px 36px;border:1px solid rgba(255,255,255,0.15);color:var(--offwhite);font-family:var(--f-body);font-size:11px;font-weight:500;letter-spacing:0.18em;text-transform:uppercase;transition:border-color .3s,color .3s;cursor:none;}}
    .btn-outline:hover{{border-color:var(--blue-mid);color:var(--blue-mid);}}
    .footer{{background:#040912;border-top:1px solid rgba(255,255,255,0.04);}}
    .footer-inner{{display:flex;justify-content:space-between;align-items:center;padding:22px var(--gap);flex-wrap:wrap;gap:14px;max-width:var(--max);margin:0 auto;}}
    .footer-logo{{height:28px;display:flex;align-items:center;}}
    .footer-copy{{font-family:var(--f-body);font-size:11px;color:var(--mist);letter-spacing:0.06em;}}
    .footer-socials{{display:flex;gap:18px;}}
    .footer-socials a{{font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:var(--mist);transition:color .3s;}}
    .footer-socials a:hover{{color:var(--blue-mid);}}
    .wa-bubble{{position:fixed;bottom:28px;right:28px;z-index:8000;}}
    .wa-btn{{width:52px;height:52px;border-radius:50%;background:#25d366;box-shadow:0 6px 28px rgba(37,211,102,0.38);display:flex;align-items:center;justify-content:center;cursor:none;transition:transform .3s var(--ease);animation:waPulse 2.8s ease-in-out infinite;}}
    @keyframes waPulse{{0%,100%{{box-shadow:0 6px 28px rgba(37,211,102,0.38),0 0 0 0 rgba(37,211,102,0.32);}}50%{{box-shadow:0 6px 28px rgba(37,211,102,0.38),0 0 0 14px rgba(37,211,102,0);}}}}
    .wa-btn:hover{{transform:scale(1.1);}}
    .wa-btn svg{{width:26px;height:26px;}}
    @media(max-width:900px){{.nav-links,.nav-cta{{display:none;}}.nav-menu-btn{{display:flex;}}.s-intro-grid{{grid-template-columns:1fr;gap:24px;}}.g-feature,.g-feature-rev{{grid-template-columns:1fr;}}.g-trio{{grid-template-columns:1fr 1fr;}}}}
    @media(max-width:1100px){{.ar-wide,.ar-43,.ar-32,.ar-sq{{height:clamp(320px,52vh,620px);}}}}
    @media(max-width:700px){{.g-half,.g-trio{{grid-template-columns:1fr;}}.g-full{{height:clamp(280px,60vw,460px);}}.ar-wide,.ar-43,.ar-32,.ar-sq{{height:clamp(280px,68vw,460px);}}.hero-meta-div{{display:none;}}.wa-bubble{{bottom:16px;right:16px;}}}}
    @media(max-width:480px){{.ar-wide,.ar-43,.ar-32,.ar-sq{{height:clamp(260px,75vw,420px);}}}}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CreativeWork",
        "@id": "https://nextgeninterior.com/{slug}#work",
        "headline": "{title} — NextGen Interiors &amp; Architects",
        "description": "{desc}",
        "url": "https://nextgeninterior.com/{slug}",
        "author": {{
          "@type": "Organization",
          "name": "NextGen Architects and Interiors",
          "url": "https://nextgeninterior.com"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "NextGen Architects and Interiors",
          "logo": {{
            "@type": "ImageObject",
            "url": "https://nextgeninterior.com/logo/favicon.png"
          }}
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://nextgeninterior.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "{category_name}", "item": "https://nextgeninterior.com/{category_slug}" }},
          {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "https://nextgeninterior.com/{slug}" }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>
<div class="cursor-dot" id="cursorDot"></div>
<div class="cursor-ring" id="cursorRing"></div>

<nav class="nav">
  <a href="/" class="nav-logo"><img src="logo/logo.png" class="logo-img" alt="NextGen Interiors" style="height:32px;"/></a>
  <ul class="nav-links">
    <li><a href="architecture">Architecture</a></li>
    <li><a href="interiors">Interiors</a></li>
    <li><a href="dpr-landscaping">DPR &amp; Landscaping</a></li>
    <li>
      <button class="nav-dropdown-trigger">Portfolio<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button>
      <div class="nav-dropdown-wrap"><div class="nav-dropdown">
        <a href="hospitality">Hospitality</a>
        <a href="residential">Residential</a>
        <a href="commercial">Commercial</a>
        <a href="healthcare">Healthcare</a>
        <a href="club-resort">Club or Resort</a>
        <a href="education">Education</a>
        <a href="workplace">Workplace</a>
      </div></div>
    </li>
    <li><a href="blog">Journal</a></li>
    <li><a href="/#contact">Contact</a></li>
    <li><a href="careers">Careers</a></li>
  </ul>
  <a href="tel:+9779849151220" class="nav-cta">+977 9849151220</a>
  <button class="nav-menu-btn" id="menuBtn" aria-label="Menu"><span></span><span></span><span></span></button>
</nav>

<div class="m-menu" id="mMenu">
  <div class="m-menu-topbar">
    <div style="height:30px;display:flex;align-items:center;"><img src="logo/logo.png" class="logo-img" alt="NextGen Interiors" style="height:28px;"/></div>
    <button class="nav-menu-btn open" id="mMenuClose" style="display:flex;"><span></span><span></span><span></span></button>
  </div>
  <div class="m-menu-body"><nav><ul class="m-menu-links">
    <li><a href="architecture">Architecture</a></li>
    <li><a href="interiors">Interiors</a></li>
    <li><a href="dpr-landscaping">DPR &amp; Landscaping</a></li>
    <li>
      <button class="m-menu-acc-btn" id="mPortfolioBtn">Portfolio<span class="m-acc-chevron"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></span></button>
      <div class="m-acc-sub" id="mPortfolioSub"><div class="m-acc-sub-inner">
        <a href="hospitality">Hospitality</a>
        <a href="residential">Residential</a>
        <a href="commercial">Commercial</a>
        <a href="healthcare">Healthcare</a>
        <a href="club-resort">Club or Resort</a>
        <a href="education">Education</a>
        <a href="workplace">Workplace</a>
      </div></div>
    </li>
    <li><a href="blog">Journal</a></li>
    <li><a href="/#contact">Contact</a></li>
    <li><a href="careers">Careers</a></li>
  </ul></nav></div>
  <div class="m-menu-footer">
    <div style="font-size:9px;letter-spacing:0.3em;text-transform:uppercase;color:var(--mist);">Head Office &mdash; Baluwatar, Kathmandu</div>
    <a href="tel:+9779849151220" style="font-size:13px;color:rgba(245,242,237,0.6);">+977 9849151220</a>
    <!--email_off--><a href="mailto:info@nextgeninterior.com" style="font-size:13px;color:rgba(245,242,237,0.6);">info@nextgeninterior.com</a><!--/email_off-->
  </div>
</div>

<section class="hero">
  <div class="hero-img"><img src="{hero_image}" alt="{title}"/></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-eyebrow">{eyebrow}</div>
    <h1 class="hero-h1">{h1_formatted}</h1>
    <div class="hero-meta">
      <div class="hero-meta-item"><span class="meta-label">Location</span><span class="meta-val">{location}</span></div>
      <div class="hero-meta-div"></div>
      <div class="hero-meta-item"><span class="meta-label">Category</span><span class="meta-val">{category_name}</span></div>
      <div class="hero-meta-div"></div>
      <div class="hero-meta-item"><span class="meta-label">Client</span><span class="meta-val">{title}</span></div>
      <div class="hero-meta-div"></div>
      <div class="hero-meta-item"><span class="meta-label">By</span><span class="meta-val">NextGen Interiors</span></div>
    </div>
  </div>
  <div class="scroll-hint"><span class="scroll-word">Scroll</span><div class="scroll-track"><div class="scroll-fill"></div></div></div>
</section>

<div class="s-intro">
  <div class="s-tag rv">Project Overview</div>
  <div class="s-intro-grid">
    <h2 class="s-intro-h rv">{intro_heading}</h2>
    <div class="s-intro-body rv d1">
      {intro_paragraphs}
    </div>
  </div>
</div>

<div class="gallery" id="gallery">
  {showcase_html}
</div>

<div class="lb" id="lb" onclick="closeLbOnBg(event)">
  <div class="lb-img-wrap">
    <div class="lb-close" onclick="closeLb()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
    <img id="lbImg" src="" alt=""/>
  </div>
  <button class="lb-prev" onclick="lbNav(-1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="15 18 9 12 15 6"/></svg></button>
  <button class="lb-next" onclick="lbNav(1)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="9 18 15 12 9 6"/></svg></button>
  <div class="lb-counter" id="lbCounter"></div>
</div>

<div class="cta-strip">
  <h2 class="cta-h">START YOUR<br><span>NEXT PROJECT</span></h2>
  <p class="cta-p">From private homes to hospitality flagships &mdash; let&rsquo;s talk about your space.</p>
  <div class="cta-btns">
    <a href="tel:+9779849151220" class="btn-primary">Call Us Now</a>
    <a href="{category_slug}" class="btn-outline">&larr; Back to {category_name}</a>
  </div>
</div>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-logo"><img src="logo/logo.png" class="logo-img" alt="NextGen Interiors" style="height:28px;"/></div>
    <p class="footer-copy">&copy; 2025 NextGen Interiors &amp; Architects &middot; Baluwatar, Kathmandu</p>
    <div class="footer-socials"><a href="https://www.instagram.com/nextgen_interiors_architects?igsh=OGtuYjZhbmUzamgy" target="_blank" rel="noopener">Instagram</a><a href="https://www.facebook.com/architectsandinteriorshouse" target="_blank" rel="noopener">Facebook</a><a href="https://www.linkedin.com/company/nextgen-interiors-architects-pvt-ltd/?originalSubdomain=np" target="_blank" rel="noopener">LinkedIn</a><a href="https://www.youtube.com/@nextgeninteriors" target="_blank" rel="noopener">YouTube</a></div>
  </div>
</footer>

<div class="wa-bubble">
  <a href="https://wa.me/9779849151220?text=Hello%20NextGen%2C%20I%27d%20like%20to%20discuss%20a%20project." class="wa-btn" target="_blank" rel="noopener" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.115 1.523 5.845L.057 23.427a.5.5 0 0 0 .606.63l5.7-1.494A11.953 11.953 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.953 9.953 0 0 1-5.17-1.447l-.37-.22-3.38.885.9-3.3-.24-.38A9.964 9.964 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
  </a>
</div>

<script>
  const dot=document.getElementById('cursorDot'),ring=document.getElementById('cursorRing');
  let mx=0,my=0,rx=0,ry=0;
  document.addEventListener('mousemove',e=>{{mx=e.clientX;my=e.clientY;dot.style.left=mx+'px';dot.style.top=my+'px';}});
  (function animRing(){{rx+=(mx-rx)*.11;ry+=(my-ry)*.11;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(animRing);}})();
  document.querySelectorAll('a,button,.g-card').forEach(el=>{{el.addEventListener('mouseenter',()=>document.body.classList.add('c-hover'));el.addEventListener('mouseleave',()=>document.body.classList.remove('c-hover'));}});
  const menuBtn=document.getElementById('menuBtn'),mMenu=document.getElementById('mMenu');
  function openMenu(){{menuBtn.classList.add('open');mMenu.classList.add('open');document.body.style.overflow='hidden';}}
  function closeMenu(){{menuBtn.classList.remove('open');mMenu.classList.remove('open');document.body.style.overflow='';}}
  menuBtn.addEventListener('click',()=>{{mMenu.classList.contains('open')?closeMenu():openMenu();}});
  document.getElementById('mMenuClose').addEventListener('click',closeMenu);
  mMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  const mPBtn=document.getElementById('mPortfolioBtn'),mPSub=document.getElementById('mPortfolioSub');
  mPBtn.addEventListener('click',()=>{{const o=mPSub.classList.contains('open');mPSub.classList.toggle('open',!o);mPBtn.classList.toggle('active',!o);}});
  const ro=new IntersectionObserver(entries=>{{entries.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('vis');ro.unobserve(e.target);}}}});}},{{threshold:0.04}});
  document.querySelectorAll('.rv').forEach(el=>ro.observe(el));

  const LB_PHOTOS = {photos_json};
  let lbCurrent = 0;
  const lb = document.getElementById('lb'), lbImg = document.getElementById('lbImg'), lbCounter = document.getElementById('lbCounter');
  function openLb(idx){{lbCurrent = idx; updateLb(); lb.classList.add('open'); document.body.style.overflow='hidden';}}
  function closeLb(){{lb.classList.remove('open'); document.body.style.overflow='';}}
  function closeLbOnBg(e){{if(e.target === lb) closeLb();}}
  function lbNav(dir){{if(!LB_PHOTOS.length) return; lbCurrent = (lbCurrent + dir + LB_PHOTOS.length) % LB_PHOTOS.length; updateLb();}}
  function updateLb(){{if(!LB_PHOTOS.length) return; lbImg.src = LB_PHOTOS[lbCurrent]; lbCounter.textContent = (lbCurrent + 1) + ' / ' + LB_PHOTOS.length;}}
  document.addEventListener('keydown', e => {{
    if(!lb.classList.contains('open')) return;
    if(e.key === 'Escape') closeLb();
    if(e.key === 'ArrowLeft') lbNav(-1);
    if(e.key === 'ArrowRight') lbNav(1);
  }});
</script>
</body>
</html>"""

TITLE_MAX = 60

def build_page_title(title):
    """'<Project> — <brand>' trimmed to what Google actually renders.

    Google cuts a title link at roughly 60 characters, so the brand tail is
    stepped down — full name, short name, then dropped entirely — until the
    whole thing fits. The project name itself is never truncated: it is the
    part someone is searching for."""
    for brand in (' — NextGen Interiors & Architects', ' — NextGen Interiors', ' — NextGen'):
        candidate = title + brand
        if len(candidate) <= TITLE_MAX:
            return candidate
    return title

def build_showcase_layout(gallery):
    if not gallery:
        return ""
        
    html_parts = []
    total = len(gallery)
    i = 0
    
    # 1. First image: Full-width hero showcase
    if i < total:
        html_parts.append(f"""
  <div class="g-full rv" style="position:relative;">
    <div class="g-card" style="position:absolute;inset:0;" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase Hero {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Featured Space</span></div>
    </div>
  </div>""")
        i += 1
        
    # 2. Pair: Two large balanced images
    if i + 1 < total:
        html_parts.append(f"""
  <div class="g-half rv" style="margin-top:4px;">
    <div class="g-card ar-43" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Architectural Perspective</span></div>
    </div>
    <div class="g-card ar-43" onclick="openLb({i+1})">
      <img src="{gallery[i+1]}" alt="Showcase {i+2}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Spatial Detailing</span></div>
    </div>
  </div>""")
        i += 2
    elif i < total:
        html_parts.append(f"""
  <div class="g-full rv" style="margin-top:4px;">
    <div class="g-card ar-43" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Spatial Perspective</span></div>
    </div>
  </div>""")
        i += 1
        
    # 3. Asymmetric 2:1 Focal Split
    if i + 1 < total:
        html_parts.append(f"""
  <div class="g-feature rv" style="margin-top:4px;">
    <div class="g-card ar-32" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Design Focal Point</span></div>
    </div>
    <div class="g-card ar-32" onclick="openLb({i+1})">
      <img src="{gallery[i+1]}" alt="Showcase {i+2}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Material Accent</span></div>
    </div>
  </div>""")
        i += 2
        
    # 4. Asymmetric 1:2 Reverse Focal Split
    if i + 1 < total:
        html_parts.append(f"""
  <div class="g-feature-rev rv" style="margin-top:4px;">
    <div class="g-card ar-32" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Atmosphere &amp; Light</span></div>
    </div>
    <div class="g-card ar-32" onclick="openLb({i+1})">
      <img src="{gallery[i+1]}" alt="Showcase {i+2}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Living Environment</span></div>
    </div>
  </div>""")
        i += 2
        
    # 5. Trio or remaining full-width
    while i < total:
        remaining = total - i
        if remaining >= 3:
            html_parts.append(f"""
  <div class="g-trio rv" style="margin-top:4px;">
    <div class="g-card ar-sq" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Detail Approach</span></div>
    </div>
    <div class="g-card ar-sq" onclick="openLb({i+1})">
      <img src="{gallery[i+1]}" alt="Showcase {i+2}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Joinery &amp; Texture</span></div>
    </div>
    <div class="g-card ar-sq" onclick="openLb({i+2})">
      <img src="{gallery[i+2]}" alt="Showcase {i+3}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Craftsmanship</span></div>
    </div>
  </div>""")
            i += 3
        elif remaining == 2:
            html_parts.append(f"""
  <div class="g-half rv" style="margin-top:4px;">
    <div class="g-card ar-43" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Detail Accent</span></div>
    </div>
    <div class="g-card ar-43" onclick="openLb({i+1})">
      <img src="{gallery[i+1]}" alt="Showcase {i+2}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Complete View</span></div>
    </div>
  </div>""")
            i += 2
        else:
            html_parts.append(f"""
  <div class="g-full rv" style="margin-top:4px;height:clamp(380px,62vh,720px);position:relative;">
    <div class="g-card" style="position:absolute;inset:0;" onclick="openLb({i})">
      <img src="{gallery[i]}" alt="Showcase {i+1}"/>
      <div class="g-card-overlay"></div>
      <div class="g-card-label"><span>Panoramic Perspective</span></div>
    </div>
  </div>""")
            i += 1
            
    return "\n".join(html_parts)

def fetch_sanity_data():
    query = """*[_type == "project"] | order(_createdAt desc) {
        title,
        "slug": slug.current,
        mainCategory,
        subCategory,
        featuredOnHome,
        projectStatus,
        eyebrow,
        location,
        intro_heading,
        intro_text,
        description,
        "thumbnail": coalesce(thumbnail.asset->url, thumbnail.asset.asset->url, galleryImages[0].asset->url, galleryImages[0].asset.asset->url),
        "gallery": galleryImages[]{ "url": coalesce(asset->url, asset.asset->url) }.url
    }"""
    
    url = f"https://{PROJECT_ID}.api.sanity.io/v2021-10-21/data/query/{DATASET}?query={urllib.parse.quote(query)}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        return data.get('result', [])

def fetch_sanity_blogs():
    query = """*[_type == "blog"] | order(publishedAt desc, _createdAt desc) {
        title,
        "slug": slug.current,
        category,
        publishedAt,
        readTime,
        author,
        metaDescription,
        lede,
        "coverImage": coalesce(coverImage.asset->url, coverImage.asset.asset->url),
        content,
        tags
    }"""
    url = f"https://{PROJECT_ID}.api.sanity.io/v2021-10-21/data/query/{DATASET}?query={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            return data.get('result', [])
    except Exception as e:
        print(f"Note on Sanity blogs fetch: {e}")
        return []

def portable_text_to_html(blocks):
    if not blocks:
        return ""
    if isinstance(blocks, str):
        return blocks
        
    html_parts = []
    current_list_type = None
    list_items = []
    
    def flush_list():
        nonlocal current_list_type, list_items
        if list_items:
            tag = "ul" if current_list_type == "bullet" else "ol"
            html_parts.append(f"<{tag}>\n" + "\n".join(list_items) + f"\n</{tag}>")
            list_items = []
            current_list_type = None

    for block in blocks:
        if not isinstance(block, dict):
            continue
        if block.get('_type') != 'block':
            continue
            
        list_item = block.get('listItem')
        style = block.get('style', 'normal')
        children = block.get('children', [])
        mark_defs = {m.get('_key'): m for m in block.get('markDefs', []) if isinstance(m, dict)}
        
        span_texts = []
        for child in children:
            if not isinstance(child, dict):
                continue
            text = child.get('text', '')
            marks = child.get('marks', [])
            
            import html as pyhtml
            formatted = pyhtml.escape(text)
            for mark in marks:
                if mark == 'strong':
                    formatted = f"<strong>{formatted}</strong>"
                elif mark == 'em':
                    formatted = f"<em>{formatted}</em>"
                elif mark in mark_defs:
                    href = mark_defs[mark].get('href', '#')
                    formatted = f'<a href="{href}">{formatted}</a>'
            span_texts.append(formatted)
            
        inner_html = "".join(span_texts).strip()
        if not inner_html:
            continue
            
        if list_item:
            if current_list_type and current_list_type != list_item:
                flush_list()
            current_list_type = list_item
            list_items.append(f"  <li>{inner_html}</li>")
            continue
        else:
            flush_list()
            
        if style == 'h2':
            html_parts.append(f"  <h2>{inner_html}</h2>")
        elif style == 'h3':
            html_parts.append(f"  <h3>{inner_html}</h3>")
        elif style == 'blockquote':
            html_parts.append(f'  <div class="article-pullquote"><p>{inner_html}</p></div>')
        else:
            html_parts.append(f"  <p>{inner_html}</p>")
            
    flush_list()
    return "\n\n".join(html_parts)

BLOG_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <link rel="icon" type="image/png" sizes="32x32" href="/logo/favicon.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/logo/favicon.png" />
  <link rel="shortcut icon" href="/logo/favicon.png" />
  <link rel="apple-touch-icon" href="/logo/favicon.png" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{page_title}</title>
  <meta name="description" content="{desc}"/>
  <link rel="canonical" href="https://nextgeninterior.com/{slug}"/>
  <meta name="robots" content="index, follow, max-image-preview:large"/>
  <meta name="author" content="{author}"/>
  <meta name="theme-color" content="#0d1520"/>
  <meta name="geo.region" content="NP"/>
  <meta name="geo.placename" content="Kathmandu, Nepal"/>
  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="NextGen Architects and Interiors" />
  <meta property="og:locale" content="en_US"/>
  <meta property="og:title" content="{page_title}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:url" content="https://nextgeninterior.com/{slug}"/>
  <meta property="og:image" content="{hero_image}"/>
  <meta property="og:image:alt" content="{title} | NextGen Interiors"/>
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{page_title}"/>
  <meta name="twitter:description" content="{desc}"/>
  <meta name="twitter:image" content="{hero_image}"/>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet">
  <style>
    :root{{--blue-mid:#369fce;--ink:#0d1520;--offwhite:#f5f2ed;--mist:#8a97aa;--f-head:'Bebas Neue',sans-serif;--f-body:'Poppins',sans-serif;--ease:cubic-bezier(0.16,1,0.3,1);--gap:clamp(20px,5vw,80px);--max:1440px;--read:760px;}}
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
    html{{scroll-behavior:smooth;}}
    body{{font-family:var(--f-body);background:var(--ink);color:var(--offwhite);overflow-x:hidden;cursor:none;}}
    img{{display:block;max-width:100%;}}
    .logo-img{{display:block;width:auto!important;height:100%!important;object-fit:contain!important;}}
    a{{text-decoration:none;color:inherit;}}
    button{{border:none;background:none;cursor:none;font:inherit;}}
    ul{{list-style:none;}}
    ::-webkit-scrollbar{{width:3px;}}
    ::-webkit-scrollbar-track{{background:var(--ink);}}
    ::-webkit-scrollbar-thumb{{background:var(--blue-mid);}}
    .cursor-dot{{width:7px;height:7px;border-radius:50%;background:var(--blue-mid);position:fixed;top:0;left:0;transform:translate(-50%,-50%);z-index:9999;pointer-events:none;transition:width .2s,height .2s;mix-blend-mode:screen;}}
    .cursor-ring{{width:36px;height:36px;border-radius:50%;border:1px solid rgba(62,159,201,.35);position:fixed;top:0;left:0;transform:translate(-50%,-50%);z-index:9998;pointer-events:none;transition:width .35s var(--ease),height .35s var(--ease),opacity .3s;}}
    body.c-hover .cursor-dot{{width:52px;height:52px;opacity:.15;}}
    body.c-hover .cursor-ring{{opacity:0;}}
    .nav{{position:fixed;top:0;left:0;right:0;z-index:200;padding:22px var(--gap);display:flex;align-items:center;justify-content:space-between;background:rgba(13,21,32,.96);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,.05);}}
    .nav-logo{{height:34px;display:flex;align-items:center;}}
    .nav-links{{display:flex;gap:32px;align-items:center;}}
    .nav-links>li{{position:relative;}}
    .nav-links a,.nav-dropdown-trigger{{font-family:var(--f-body);font-size:11px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:rgba(245,242,237,.45);transition:color .3s;display:flex;align-items:center;gap:5px;cursor:none;position:relative;}}
    .nav-links a::after{{content:'';position:absolute;bottom:-3px;left:0;width:0;height:1px;background:var(--blue-mid);transition:width .4s var(--ease);}}
    .nav-links a:hover,.nav-links a.active{{color:var(--offwhite);}}
    .nav-links a.active::after,.nav-links a:hover::after{{width:100%;}}
    .nav-dropdown-trigger{{background:none;border:none;padding:0;}}
    .nav-dropdown-trigger svg{{width:10px;height:10px;transition:transform .3s var(--ease);}}
    .nav-links>li:hover .nav-dropdown-trigger{{color:var(--offwhite);}}
    .nav-links>li:hover .nav-dropdown-trigger svg{{transform:rotate(180deg);}}
    .nav-dropdown-wrap{{position:absolute;top:100%;left:50%;transform:translateX(-50%);padding-top:14px;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .28s var(--ease),visibility .28s;z-index:300;}}
    .nav-links>li:hover .nav-dropdown-wrap{{opacity:1;visibility:visible;pointer-events:all;}}
    .nav-dropdown{{background:rgba(8,14,24,.98);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.08);border-top:2px solid var(--blue-mid);min-width:220px;transform:translateY(6px);transition:transform .28s var(--ease);box-shadow:0 20px 60px rgba(0,0,0,.5);}}
    .nav-links>li:hover .nav-dropdown{{transform:translateY(0);}}
    .nav-dropdown a{{display:flex;align-items:center;gap:10px;padding:14px 22px;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:rgba(245,242,237,.45);border-bottom:1px solid rgba(255,255,255,.04);transition:color .22s,background .22s,padding-left .22s;white-space:nowrap;}}
    .nav-dropdown a::before{{content:'';width:0;height:1px;background:var(--blue-mid);transition:width .3s var(--ease);flex-shrink:0;}}
    .nav-dropdown a:last-child{{border-bottom:none;}}
    .nav-dropdown a::after{{display:none!important;}}
    .nav-dropdown a:hover{{color:var(--blue-mid);background:rgba(54,159,206,.05);padding-left:28px;}}
    .nav-dropdown a:hover::before{{width:12px;}}
    .nav-cta {{ display: inline-flex; align-items: center; gap: 8px; font-family: var(--f-body); font-size: 11px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--offwhite); padding: 9px 18px; border: 1px solid rgba(54,159,206,0.5); background: rgba(54,159,206,0.1); white-space: nowrap; transition: background .35s var(--ease), border-color .35s var(--ease), color .35s var(--ease), box-shadow .35s var(--ease), transform .35s var(--ease); }}
    .nav-cta svg {{ width: 13px; height: 13px; flex-shrink: 0; color: var(--blue-mid); transition: color .35s, transform .45s var(--ease); }}
    .nav-cta:hover {{ background: var(--blue-mid); border-color: var(--blue-mid); color: var(--ink); box-shadow: 0 6px 22px rgba(54,159,206,0.32); transform: translateY(-1px); }}
    .nav-cta:hover svg {{ color: var(--ink); transform: rotate(-14deg) scale(1.12); }}
    .nav-cta:active {{ transform: translateY(0); box-shadow: 0 2px 10px rgba(54,159,206,0.22); }}
    .nav-menu-btn{{display:none;flex-direction:column;gap:6px;width:26px;cursor:none;}}
    .nav-menu-btn span{{display:block;width:100%;height:1px;background:var(--offwhite);transition:transform .4s var(--ease),opacity .3s;}}
    .nav-menu-btn.open span:nth-child(1){{transform:translateY(7px) rotate(45deg);}}
    .nav-menu-btn.open span:nth-child(2){{opacity:0;}}
    .nav-menu-btn.open span:nth-child(3){{transform:translateY(-7px) rotate(-45deg);}}
    .m-menu{{position:fixed;inset:0;z-index:190;background:#080f1c;display:grid;grid-template-rows:auto 1fr auto;opacity:0;visibility:hidden;transition:opacity .55s var(--ease),visibility .55s;overflow-y:auto;}}
    .m-menu.open{{opacity:1;visibility:visible;}}
    .m-menu-topbar{{display:flex;align-items:center;justify-content:space-between;padding:22px var(--gap);border-bottom:1px solid rgba(255,255,255,.05);}}
    .m-menu-body{{padding:32px var(--gap) 24px;}}
    .m-menu-links>li{{border-bottom:1px solid rgba(255,255,255,.06);}}
    .m-menu-links a,.m-menu-links .m-menu-acc-btn{{font-family:var(--f-head);font-size:clamp(36px,8vw,60px);letter-spacing:.05em;color:rgba(245,242,237,.85);display:flex;align-items:center;justify-content:space-between;line-height:1;padding:18px 0;transform:translateY(20px);opacity:0;transition:transform .55s var(--ease),opacity .55s var(--ease),color .25s;background:none;border:none;cursor:none;width:100%;}}
    .m-menu.open .m-menu-links a,.m-menu.open .m-menu-links .m-menu-acc-btn{{transform:translateY(0);opacity:1;}}
    .m-menu-links a:hover,.m-menu-acc-btn.active,.m-menu-links a.active{{color:var(--blue-mid);}}
    .m-acc-chevron{{width:22px;height:22px;flex-shrink:0;border:1px solid rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;transition:transform .35s var(--ease),border-color .3s;}}
    .m-acc-chevron svg{{width:12px;height:12px;color:var(--mist);}}
    .m-menu-acc-btn.active .m-acc-chevron{{transform:rotate(180deg);border-color:var(--blue-mid);}}
    .m-acc-sub{{max-height:0;overflow:hidden;transition:max-height .45s var(--ease);}}
    .m-acc-sub.open{{max-height:600px;}}
    .m-acc-sub-inner{{padding:6px 0 16px;display:grid;grid-template-columns:1fr 1fr;gap:4px;}
    .m-acc-sub a{{font-family:var(--f-body)!important;font-size:11px!important;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:rgba(245,242,237,.4)!important;padding:12px 14px!important;display:flex!important;align-items:center;gap:8px;transform:none!important;opacity:1!important;border:1px solid rgba(255,255,255,.05)!important;transition:color .2s,border-color .2s,background .2s!important;}
    .m-acc-sub a::before{{content:'';width:5px;height:1px;background:currentColor;flex-shrink:0;}}
    .m-acc-sub a:hover{{color:var(--blue-mid)!important;border-color:rgba(54,159,206,.25)!important;}
    .m-menu-footer{{padding:20px var(--gap) 32px;border-top:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:14px;opacity:0;transform:translateY(10px);transition:opacity .5s var(--ease) .3s,transform .5s var(--ease) .3s;}
    .m-menu.open .m-menu-footer{{opacity:1;transform:translateY(0);}}
    .m-service-label{{font-family:var(--f-body);font-size:9px;font-weight:600;letter-spacing:.3em;text-transform:uppercase;color:var(--mist);margin-bottom:6px;}}
    .m-service-pill{{display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border:1px solid rgba(54,159,206,.2);font-family:var(--f-body);font-size:9px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--blue-mid);}}
    .m-hq-row{{display:flex;align-items:center;gap:8px;font-family:var(--f-body);font-size:10px;color:rgba(245,242,237,.35);margin-top:6px;}}
    .m-hq-dot{{width:5px;height:5px;border-radius:50%;background:var(--blue-mid);flex-shrink:0;}}
    .m-contact-row{{display:flex;flex-direction:column;gap:4px;}
    .m-contact-row a{{font-family:var(--f-body);font-size:12px;color:rgba(245,242,237,.5);transition:color .25s;transform:none!important;opacity:1!important;}
    .m-contact-row a:hover{{color:var(--blue-mid);}}
    .article-hero{{position:relative;height:70vh;min-height:500px;margin-top:78px;overflow:hidden;}}
    .article-hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}}
    .article-hero-overlay{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(13,21,32,.45) 0%,rgba(13,21,32,.3) 40%,rgba(13,21,32,.95) 100%);z-index:1;}}
    .article-hero-content{{position:absolute;bottom:0;left:0;right:0;z-index:2;padding:0 var(--gap) clamp(40px,5vw,72px);max-width:var(--max);margin:0 auto;}}
    .breadcrumb{{display:flex;align-items:center;gap:10px;font-family:var(--f-body);font-size:10px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:rgba(245,242,237,.6);margin-bottom:22px;}}
    .breadcrumb a{{color:var(--blue-mid);}}
    .breadcrumb svg{{width:10px;height:10px;}}
    .article-category{{display:inline-block;padding:6px 14px;background:var(--blue-mid);color:var(--ink);font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;margin-bottom:20px;}}
    .article-title{{font-family:var(--f-head);font-size:clamp(34px,5vw,72px);letter-spacing:.04em;color:var(--offwhite);line-height:1;max-width:1000px;text-shadow:0 2px 24px rgba(0,0,0,.6);}}
    .article-meta{{display:flex;align-items:center;gap:14px;font-family:var(--f-body);font-size:11px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:var(--mist);margin-top:22px;flex-wrap:wrap;}}
    .article-meta .dot{{width:3px;height:3px;border-radius:50%;background:var(--blue-mid);}}
    .article-meta .by{{color:var(--blue-mid);}}
    .article-body{{max-width:var(--read);margin:0 auto;padding:clamp(48px,6vw,90px) var(--gap);}}
    .article-lede{{font-family:var(--f-body);font-size:clamp(16px,1.4vw,19px);font-weight:300;line-height:1.65;color:var(--offwhite);margin-bottom:36px;padding-left:22px;border-left:2px solid var(--blue-mid);}}
    .article-body h2{{font-family:var(--f-head);font-size:clamp(28px,3vw,40px);letter-spacing:.04em;color:var(--offwhite);line-height:1.1;margin:56px 0 18px;}}
    .article-body h3{{font-family:var(--f-head);font-size:clamp(22px,2.2vw,28px);letter-spacing:.05em;color:var(--blue-mid);margin:36px 0 14px;}}
    .article-body p{{font-family:var(--f-body);font-size:14.5px;font-weight:300;line-height:1.85;color:rgba(245,242,237,.78);margin-bottom:18px;}}
    .article-body p strong{{color:var(--offwhite);font-weight:500;}}
    .article-body p a{{color:var(--blue-mid);text-decoration:underline;text-underline-offset:3px;}}
    .article-body em{{color:rgba(245,242,237,.65);font-style:italic;}}
    .article-body ul,.article-body ol{{margin:16px 0 24px;padding-left:0;}}
    .article-body li{{font-family:var(--f-body);font-size:14px;font-weight:300;line-height:1.8;color:rgba(245,242,237,.78);padding-left:24px;position:relative;margin-bottom:12px;list-style:none;}}
    .article-body li::before{{content:'';position:absolute;left:0;top:12px;width:12px;height:1px;background:var(--blue-mid);}}
    .article-body li strong{{color:var(--offwhite);font-weight:600;}}
    .article-pullquote{{font-family:var(--f-head);font-size:clamp(24px,2.6vw,32px);letter-spacing:.03em;line-height:1.25;color:var(--offwhite);margin:44px 0;padding:28px 30px;background:rgba(54,159,206,.06);border-left:3px solid var(--blue-mid);}}
    .article-pullquote::before{{content:'"';font-size:60px;color:var(--blue-mid);float:left;line-height:.7;margin-right:8px;opacity:.5;}}
    .article-closer{{margin-top:56px;padding-top:36px;border-top:1px solid rgba(255,255,255,.08);font-family:var(--f-body);font-size:13px;font-weight:300;line-height:1.8;color:var(--mist);}}
    .article-closer strong{{color:var(--offwhite);}}
    .article-tags{{max-width:var(--read);margin:0 auto;padding:0 var(--gap) clamp(40px,5vw,64px);display:flex;flex-wrap:wrap;gap:8px;}}
    .tag{{display:inline-flex;align-items:center;padding:7px 14px;border:1px solid rgba(255,255,255,.08);font-family:var(--f-body);font-size:9px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--mist);transition:color .3s,border-color .3s,background .3s;}}
    .tag:hover{{color:var(--blue-mid);border-color:rgba(54,159,206,.3);background:rgba(54,159,206,.04);}}
    .author-strip{{max-width:var(--read);margin:0 auto;padding:clamp(28px,3.5vw,44px) var(--gap);border-top:1px solid rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.06);display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;}}
    .author-info{{display:flex;align-items:center;gap:16px;}}
    .author-avatar{{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--blue-mid),rgba(54,159,206,.4));display:flex;align-items:center;justify-content:center;font-family:var(--f-head);font-size:22px;color:var(--ink);letter-spacing:.04em;flex-shrink:0;}}
    .author-name{{font-family:var(--f-body);font-size:13px;font-weight:500;color:var(--offwhite);letter-spacing:.05em;}
    .author-role{{font-family:var(--f-body);font-size:10px;font-weight:400;color:var(--mist);letter-spacing:.18em;text-transform:uppercase;margin-top:3px;}
    .share-row{{display:flex;align-items:center;gap:10px;}}
    .share-label{{font-family:var(--f-body);font-size:9px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--mist);margin-right:6px;}
    .share-btn{{width:36px;height:36px;border:1px solid rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-family:var(--f-body);font-size:10px;font-weight:600;color:var(--mist);transition:color .3s,border-color .3s,background .3s;}
    .share-btn:hover{{color:var(--blue-mid);border-color:rgba(54,159,206,.4);background:rgba(54,159,206,.05);}}
    .related-wrap{{max-width:var(--max);margin:0 auto;padding:clamp(60px,7vw,96px) var(--gap);}}
    .related-label{{font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:.3em;text-transform:uppercase;color:var(--blue-mid);display:flex;align-items:center;gap:10px;margin-bottom:12px;}
    .related-label::before{{content:'';width:18px;height:1px;background:var(--blue-mid);}}
    .related-title{{font-family:var(--f-head);font-size:clamp(36px,4vw,56px);letter-spacing:.05em;color:var(--offwhite);margin-bottom:36px;}
    .related-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:4px;}
    .blog-card{{display:flex;flex-direction:column;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.04);overflow:hidden;cursor:none;transition:border-color .3s,background .3s,transform .4s var(--ease);}}
    .blog-card:hover{{border-color:rgba(54,159,206,.3);background:rgba(54,159,206,.03);transform:translateY(-4px);}}
    .blog-card-img{{position:relative;overflow:hidden;aspect-ratio:16/9;}
    .blog-card-img img{{width:100%;height:100%;object-fit:cover;transition:transform 1.3s var(--ease),filter 1.3s;filter:brightness(.85);}}
    .blog-card:hover .blog-card-img img{{transform:scale(1.06);filter:brightness(.7);}}
    .blog-card-cat{{position:absolute;top:16px;left:16px;z-index:2;padding:5px 12px;background:rgba(13,21,32,.85);backdrop-filter:blur(8px);border:1px solid rgba(54,159,206,.3);font-family:var(--f-body);font-size:9px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--blue-mid);}}
    .blog-card-body{{padding:24px 26px 28px;}}
    .blog-card-meta{{display:flex;align-items:center;gap:12px;font-family:var(--f-body);font-size:9px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--mist);margin-bottom:12px;}}
    .blog-card-meta .dot{{width:3px;height:3px;border-radius:50%;background:var(--blue-mid);}}
    .blog-card-title{{font-family:var(--f-head);font-size:clamp(20px,2vw,26px);letter-spacing:.04em;color:var(--offwhite);line-height:1.1;transition:color .3s;}
    .blog-card:hover .blog-card-title{{color:var(--blue-mid);}}
    .back-cta-wrap{{max-width:var(--read);margin:0 auto;padding:0 var(--gap) clamp(40px,5vw,64px);display:flex;justify-content:center;}
    .back-cta{{display:inline-flex;align-items:center;gap:10px;padding:14px 30px;border:1px solid var(--blue-mid);color:var(--blue-mid);font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;transition:background .3s,color .3s;}
    .back-cta:hover{{background:var(--blue-mid);color:var(--ink);}}
    .back-cta svg{{width:14px;height:14px;transform:rotate(180deg);}}
    .rv{{opacity:0;transform:translateY(24px);transition:opacity .85s var(--ease),transform .85s var(--ease);}}
    .rv.vis{{opacity:1;transform:none;}}
    .rv.d1{{transition-delay:.07s}}.rv.d2{{transition-delay:.14s}}
    .footer{{background:#040912;border-top:1px solid rgba(255,255,255,.04);}}
    .footer-inner{{display:flex;justify-content:space-between;align-items:center;padding:22px var(--gap);flex-wrap:wrap;gap:14px;max-width:var(--max);margin:0 auto;}}
    .footer-logo{{height:28px;display:flex;align-items:center;}}
    .footer-copy{{font-family:var(--f-body);font-size:11px;color:var(--mist);letter-spacing:.06em;}}
    .footer-socials{{display:flex;gap:18px;}}
    .footer-socials a{{font-family:var(--f-body);font-size:10px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--mist);transition:color .3s;}}
    .footer-socials a:hover{{color:var(--blue-mid);}}
    .wa-bubble{{position:fixed;bottom:28px;right:28px;z-index:8000;}}
    .wa-btn{{width:52px;height:52px;border-radius:50%;background:#25d366;box-shadow:0 6px 28px rgba(37,211,102,.38);display:flex;align-items:center;justify-content:center;cursor:none;transition:transform .3s var(--ease);animation:waPulse 2.8s ease-in-out infinite;}}
    @keyframes waPulse{{0%,100%{{box-shadow:0 6px 28px rgba(37,211,102,.38),0 0 0 0 rgba(37,211,102,.32);}}50%{{box-shadow:0 6px 28px rgba(37,211,102,.38),0 0 0 14px rgba(37,211,102,0);}}}}
    .wa-btn:hover{{transform:scale(1.1);}}
    .wa-btn svg{{width:26px;height:26px;}}
    @media(max-width:900px){{.nav-links,.nav-cta{{display:none;}}.nav-menu-btn{{display:flex;}}.related-grid{{grid-template-columns:1fr;}}}}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{desc}",
    "image": "{hero_image}",
    "author": {{
      "@type": "Organization",
      "name": "NextGen Architects and Interiors",
      "url": "https://nextgeninterior.com"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "NextGen Architects and Interiors",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://nextgeninterior.com/logo/favicon.png"
      }}
    }},
    "datePublished": "{published_at}",
    "dateModified": "{published_at}",
    "url": "https://nextgeninterior.com/{slug}",
    "mainEntityOfPage": "https://nextgeninterior.com/{slug}"
  }}
  </script>
</head>
<body>
  <div class="cursor-dot" id="cursorDot"></div>
  <div class="cursor-ring" id="cursorRing"></div>

  <nav class="nav">
    <a href="/" class="nav-logo">
      <img src="/logo/favicon.png" class="logo-img" alt="NextGen Interiors"/>
    </a>
    <ul class="nav-links">
      <li><a href="/architecture">Architecture</a></li>
      <li><a href="/interiors">Interiors</a></li>
      <li><a href="/dpr-landscaping">DPR &amp; Landscaping</a></li>
      <li>
        <button class="nav-dropdown-trigger">Portfolio
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="nav-dropdown-wrap">
          <div class="nav-dropdown">
            <a href="/hospitality">Hospitality</a>
            <a href="/residential">Residential</a>
            <a href="/commercial">Commercial</a>
            <a href="/healthcare">Healthcare</a>
            <a href="/club-resort">Club or Resort</a>
            <a href="/education">Education</a>
            <a href="/workplace">Workplace</a>
          </div>
        </div>
      </li>
      <li><a href="/blog" class="active">Blog</a></li>
      <li><a href="/#contact">Contact</a></li>
      <li><a href="/careers">Careers</a></li>
    </ul>
    <a href="tel:+9779849151220" class="nav-cta" aria-label="Call NextGen Interiors"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.09 4.18 2 2 0 0 1 4.08 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>+977 9849151220</span></a>
    <button class="nav-menu-btn" id="menuBtn" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <div class="m-menu" id="mMenu">
    <div class="m-menu-topbar">
      <div style="height:30px;display:flex;align-items:center;">
        <img src="/logo/favicon.png" class="logo-img" alt="NextGen Interiors" style="height:28px;"/>
      </div>
      <button class="nav-menu-btn open" id="mMenuClose" style="display:flex;"><span></span><span></span><span></span></button>
    </div>
    <div class="m-menu-body">
      <nav>
        <ul class="m-menu-links">
          <li><a href="/architecture">Architecture</a></li>
          <li><a href="/interiors">Interiors</a></li>
          <li><a href="/dpr-landscaping">DPR &amp; Landscaping</a></li>
          <li>
            <button class="m-menu-acc-btn" id="mPortfolioBtn">Portfolio
              <span class="m-acc-chevron"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></span>
            </button>
            <div class="m-acc-sub" id="mPortfolioSub">
              <div class="m-acc-sub-inner">
                <a href="/hospitality">Hospitality</a>
                <a href="/residential">Residential</a>
                <a href="/commercial">Commercial</a>
                <a href="/healthcare">Healthcare</a>
                <a href="/club-resort">Club or Resort</a>
                <a href="/education">Education</a>
                <a href="/workplace">Workplace</a>
              </div>
            </div>
          </li>
          <li><a href="/blog" class="active">Blog</a></li>
          <li><a href="/#contact">Contact</a></li>
          <li><a href="/careers">Careers</a></li>
        </ul>
      </nav>
    </div>
    <div class="m-menu-footer">
      <div>
        <div class="m-service-label">Services</div>
        <span class="m-service-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:8px;height:8px;"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
          All Over Nepal
        </span>
      </div>
      <div class="m-hq-row">
        <span class="m-hq-dot"></span>
        <span>Head Office &middot; Baluwatar, Kathmandu</span>
      </div>
      <div class="m-contact-row">
        <a href="tel:+9779849151220">+977 9849151220</a>
        <a href="mailto:info@nextgeninterior.com">info@nextgeninterior.com</a>
      </div>
    </div>
  </div>

  <section class="article-hero">
    <img src="{hero_image}" alt="{title}" loading="eager"/>
    <div class="article-hero-overlay"></div>
    <div class="article-hero-content">
      <div class="breadcrumb">
        <a href="/">Home</a>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        <a href="/blog">Blog</a>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        <span style="color:var(--offwhite)">{category}</span>
      </div>
      <div class="article-category">{category}</div>
      <h1 class="article-title">{title}</h1>
      <div class="article-meta">
        <span>{published_at}</span>
        <span class="dot"></span>
        <span>{read_time}</span>
        <span class="dot"></span>
        <span class="by">By {author}</span>
      </div>
    </div>
  </section>

  <article class="article-body">
    {lede_html}
    {body_content}
  </article>

  {tags_html}

  <div class="author-strip">
    <div class="author-info">
      <div class="author-avatar">NG</div>
      <div>
        <div class="author-name">{author}</div>
        <div class="author-role">Architecture &amp; Interior Design Experts</div>
      </div>
    </div>
    <div class="share-row">
      <span class="share-label">Share</span>
      <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fnextgeninterior.com%2F{slug}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on Facebook">FB</a>
      <a href="https://wa.me/?text={title}%20https%3A%2F%2Fnextgeninterior.com%2F{slug}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on WhatsApp">WA</a>
      <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fnextgeninterior.com%2F{slug}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on LinkedIn">IN</a>
    </div>
  </div>

  {related_section_html}

  <div class="back-cta-wrap">
    <a href="/blog" class="back-cta">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
      All Blog Articles
    </a>
  </div>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-logo"><img src="/logo/favicon.png" class="logo-img" alt="NextGen Interiors"/></div>
      <div class="footer-copy">&copy; 2026 NextGen Interiors &amp; Architects. All rights reserved.</div>
      <div class="footer-socials">
        <a href="https://www.instagram.com/nextgen_interiors_architects?igsh=OGtuYjZhbmUzamgy" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.facebook.com/share/1B6DkR2r37/" target="_blank" rel="noopener">Facebook</a>
        <a href="https://www.tiktok.com/@nextgen_interiors?_t=ZS-8u9bK18vW4x&amp;_r=1" target="_blank" rel="noopener">TikTok</a>
      </div>
    </div>
  </footer>

  <div class="wa-bubble">
    <a href="https://wa.me/9779849151220?text=Hello%20NextGen%2C%20I%20read%20your%20blog%20and%20would%20like%20to%20discuss%20a%20project." target="_blank" rel="noopener" class="wa-btn" aria-label="Chat on WhatsApp">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
    </a>
  </div>

  <script>
    const dot = document.getElementById('cursorDot');
    const ring = document.getElementById('cursorRing');
    document.addEventListener('mousemove', (e) => {{
      dot.style.left = e.clientX + 'px';
      dot.style.top = e.clientY + 'px';
      ring.style.left = e.clientX + 'px';
      ring.style.top = e.clientY + 'px';
    }});
    document.querySelectorAll('a, button, input, textarea, select').forEach(el => {{
      el.addEventListener('mouseenter', () => document.body.classList.add('c-hover'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('c-hover'));
    }});
    const menuBtn = document.getElementById('menuBtn');
    const mMenu = document.getElementById('mMenu');
    const mMenuClose = document.getElementById('mMenuClose');
    if (menuBtn && mMenu) {{
      menuBtn.addEventListener('click', () => mMenu.classList.add('open'));
      mMenuClose.addEventListener('click', () => mMenu.classList.remove('open'));
    }}
    const mPortfolioBtn = document.getElementById('mPortfolioBtn');
    const mPortfolioSub = document.getElementById('mPortfolioSub');
    if (mPortfolioBtn && mPortfolioSub) {{
      mPortfolioBtn.addEventListener('click', () => {{
        mPortfolioBtn.classList.toggle('active');
        mPortfolioSub.classList.toggle('open');
      }});
    }}
  </script>
</body>
</html>
"""

def build_blog_pages(blogs, base_dir):
    if not blogs:
        return
    print(f"Generating {len(blogs)} Blog pages from Sanity...")
    
    for idx, b in enumerate(blogs):
        slug = (b.get('slug') or '').strip().replace(' ', '-')
        if not slug:
            continue
            
        title = b.get('title', 'Blog Article').strip()
        category = b.get('category') or 'Interior Design'
        raw_date = b.get('publishedAt') or '2026-08-04'
        read_time = b.get('readTime') or '10 min read'
        author = b.get('author') or 'NextGen Team'
        meta_desc = b.get('metaDescription') or f"{title} — Architecture and interior design insights by NextGen Interiors."
        cover_img = b.get('coverImage') or 'https://nextgeninterior.com/Galleries/GAUTAM%20HOTEL%20interior/5.webp'
        lede = b.get('lede', '').strip()
        lede_html = f'<p class="article-lede">{lede}</p>' if lede else ''
        body_html = portable_text_to_html(b.get('content'))
        
        tags = b.get('tags') or []
        tags_spans = "".join([f'<span class="tag">{t}</span>' for t in tags if t])
        tags_html = f'<div class="article-tags">\n  {tags_spans}\n</div>' if tags_spans else ''
        
        other_blogs = [ob for ob in blogs if (ob.get('slug') or '') != slug]
        related_cards = []
        for rob in other_blogs[:2]:
            r_slug = rob.get('slug')
            r_title = rob.get('title', '')
            r_cat = rob.get('category', 'Architecture')
            r_img = rob.get('coverImage') or cover_img
            r_meta = f"{rob.get('publishedAt', '')} &middot; {rob.get('readTime', '10 min read')}"
            related_cards.append(f'''    <a href="/{r_slug}" class="blog-card rv">
      <div class="blog-card-img"><img src="{r_img}" alt="{r_title}" loading="lazy"/><div class="blog-card-cat">{r_cat}</div></div>
      <div class="blog-card-body"><div class="blog-card-meta">{r_meta}</div><h3 class="blog-card-title">{r_title}</h3></div>
    </a>''')
        
        related_html = ''
        if related_cards:
            related_html = f'''<section class="related-wrap">
  <div class="related-label">Related Articles</div>
  <h2 class="related-title">MORE INSIGHTS &amp; GUIDES</h2>
  <div class="related-grid">
{chr(10).join(related_cards)}
  </div>
</section>'''

        page_title = f"{title} | NextGen Interiors"
        
        page_content = BLOG_PAGE_TEMPLATE.format(
            page_title=page_title,
            desc=meta_desc,
            slug=slug,
            title=title,
            category=category,
            published_at=raw_date,
            read_time=read_time,
            author=author,
            hero_image=cover_img,
            lede_html=lede_html,
            body_content=body_html,
            tags_html=tags_html,
            related_section_html=related_html
        )
        
        root_path = os.path.join(base_dir, f"{slug}.html")
        with open(root_path, "w", encoding="utf-8") as fp:
            fp.write(page_content)
            
        blogs_dir = os.path.join(base_dir, "blogs")
        if os.path.exists(blogs_dir):
            blog_path = os.path.join(blogs_dir, f"{slug}.html")
            with open(blog_path, "w", encoding="utf-8") as fp:
                fp.write(page_content)
                
        print(f"Generated Blog Page: {slug}.html")

def update_blog_index(blogs, base_dir):
    if not blogs:
        return
    blog_index_path = os.path.join(base_dir, "blog.html")
    if not os.path.exists(blog_index_path):
        return
        
    with open(blog_index_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    cards = []
    for b in blogs:
        slug = (b.get('slug') or '').strip().replace(' ', '-')
        if not slug:
            continue
        title = b.get('title', '').strip()
        cat = b.get('category', 'Architecture')
        date_str = b.get('publishedAt', '')
        read_str = b.get('readTime', '10 min read')
        img = b.get('coverImage') or 'https://nextgeninterior.com/Galleries/GAUTAM%20HOTEL%20interior/5.webp'
        lede = b.get('lede') or b.get('metaDescription') or ''
        
        cards.append(f'''    <a href="/{slug}" class="blog-card rv">
      <div class="blog-card-img">
        <img src="{img}" alt="{title}" loading="lazy"/>
        <div class="blog-card-cat">{cat}</div>
      </div>
      <div class="blog-card-body">
        <div class="blog-card-meta"><span>{date_str}</span><span class="dot"></span><span>{read_str}</span></div>
        <h3 class="blog-card-title">{title}</h3>
        <p class="blog-card-excerpt">{lede[:160]}...</p>
        <span class="blog-card-read">Read Article <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
      </div>
    </a>''')
    
    if cards:
        grid_html = '\n' + '\n'.join(cards) + '\n'
        content = re.sub(
            r'(<div class="blog-grid">)[\s\S]*?(</div>\s*</div>\s*(?:<!--\s*NEWSLETTER|<div class="newsletter|<footer|<div class="footer))',
            r'\1' + grid_html + r'  </div>\n</div>\n\n',
            content,
            count=1
        )
        with open(blog_index_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated blog.html with {len(cards)} blog posts from Sanity.")

def build():
    projects = fetch_sanity_data()
    print(f"Fetched {len(projects)} projects from Sanity.")
    
    base_dir = r"D:\nextgen"
    
    for p in projects:
        slug = p.get('slug')
        if not slug:
            continue
            
        title = p.get('title', 'Project')
        sub = p.get('subCategory') or 'residential'
        main_cat = p.get('mainCategory') or 'interiors'
        
        eyebrow = p.get('eyebrow') or f"{sub.capitalize()} &middot; NextGen Showcase"
        location = p.get('location') or 'Kathmandu, Nepal'
        intro_heading = p.get('intro_heading') or f"A REFINED<br>{title.upper()}"
        
        raw_text = p.get('intro_text') or f"{title} is a bespoke project designed by NextGen Interiors, delivering warm layered spaces, curated materials, and timeless architectural form."
        paragraphs = [f"<p>{line.strip()}</p>" for line in raw_text.split('\n') if line.strip()]
        intro_paragraphs = "\n      ".join(paragraphs) if paragraphs else f"<p>{raw_text}</p>"
        
        desc_raw = p.get('description') or f"{title} — interior architecture and bespoke spaces by NextGen Interiors, {location}."
        # Pad a short CMS description towards the length Google renders, but
        # never past it — the old code could only check one suffix and fell back
        # to a second one unconditionally, which is how several project pages
        # ended up at 170 characters and got their snippet rewritten.
        desc_clean = desc_raw.strip().rstrip('.')
        desc = desc_clean + "."
        if len(desc_clean) < 120:
            for suffix in (" NextGen Interiors & Architects delivers premium design and construction in Nepal.",
                           " NextGen provides premium architecture and interiors in Nepal."):
                padded = desc_clean + "." + suffix
                if len(padded) <= 160:
                    desc = padded
                    break
        desc = shorten_description(desc)
        cat_name = sub.capitalize()
        cat_slug = sub
        
        # Split last word for blue accent in H1
        parts = title.split()
        if len(parts) > 1:
            h1_formatted = " ".join(parts[:-1]) + f"<br><span>{parts[-1]}</span>"
        else:
            h1_formatted = f"{title}<br><span>PROJECT</span>"
            
        raw_gallery = p.get('gallery') or []
        gallery = [img for img in raw_gallery if img and str(img) != 'None']
        thumbnail = p.get('thumbnail')
        if not thumbnail and gallery:
            thumbnail = gallery[0]
            
        if not gallery and thumbnail and str(thumbnail) != 'None':
            gallery = [thumbnail]
            
        hero_image = thumbnail if (thumbnail and str(thumbnail) != 'None') else (gallery[0] if gallery else '')
        showcase_html = build_showcase_layout(gallery)
        
        html = PAGE_TEMPLATE.format(
            title=title,
            page_title=build_page_title(title),
            slug=slug,
            desc=desc,
            hero_image=hero_image,
            eyebrow=eyebrow,
            h1_formatted=h1_formatted,
            location=location,
            category_name=cat_name,
            category_slug=cat_slug,
            intro_heading=intro_heading,
            intro_paragraphs=intro_paragraphs,
            showcase_html=showcase_html,
            photos_json=json.dumps(gallery)
        )
        
        filepath = os.path.join(base_dir, f"{slug}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"Generated Sankhu-Style Showcase Page: {slug}.html ({len(gallery)} images)")

    # Pre-render Homepage & Category grids directly into HTML
    update_homepage_and_categories(projects, base_dir)

    # Generate updated dynamic sitemap.xml
    generate_sitemap(projects, base_dir)

def clean_location(loc):
    """Normalise CMS location strings: 'Naikap,kathmandu' / 'PANIPOKHARI , KATHMANDU'
    all collapse to 'Naikap, Kathmandu'. Guards against inconsistent data entry."""
    if not loc:
        return 'Kathmandu, Nepal'
    parts = [seg.strip() for seg in str(loc).split(',') if seg.strip()]
    parts = [seg if seg.isupper() and len(seg) <= 3 else seg.title() for seg in parts]
    return ', '.join(parts) or 'Kathmandu, Nepal'

def category_tag(p):
    """Readable category label for a card, e.g. 'Architecture · Hotel Exterior'."""
    eyebrow = (p.get('eyebrow') or '').strip()
    if eyebrow:
        return eyebrow
    main = (p.get('mainCategory') or '').strip()
    sub = (p.get('subCategory') or '').strip().replace('-', ' ')
    label = ' &middot; '.join([s.title() for s in (main, sub) if s])
    return label or 'Project'

RUNNING_CATEGORIES = {'ongoing-projects', 'running-projects', 'ongoing', 'running'}

def main_category(p):
    return (p.get('mainCategory') or '').lower()

def sub_category(p):
    return (p.get('subCategory') or '').lower()

def is_dpr(p):
    """DPR & Landscaping work. It is its own service line, managed from its own
    section of the dashboard, and it surfaces on dpr-landscaping.html only —
    never on the home page, in Architecture / Interiors, or in a sub-category
    listing. The subCategory check keeps older documents working, which were
    filed under Architecture with a 'dpr-landscaping' sub-category."""
    return main_category(p) == 'dpr-landscaping' or sub_category(p) == 'dpr-landscaping'

def is_running(p):
    """True when the dashboard marks a project as running / ongoing — either via
    the Home Page radio, the Project Status radio, or an 'Ongoing Project' main
    category. A running project belongs to the Running Projects section on the
    home page and nowhere else: not in the Architecture / Interior grids above
    it, and not in the category listing pages."""
    return ((p.get('mainCategory') or '').lower() in RUNNING_CATEGORIES
            or p.get('projectStatus') == 'running'
            or p.get('featuredOnHome') == 'running')

def is_hidden_from_home(p):
    """Only an explicit '❌ NO' hides a project from the home page. The legacy
    boolean False is deliberately ignored — featuredOnHome used to be a checkbox
    with initialValue false, so those values are stale defaults rather than a
    choice, and honouring them would silently empty most of the home grids."""
    return p.get('featuredOnHome') == 'no'

PIN_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>'

def pm_card(p, h_class):
    """One homepage portfolio card. Carries a category tag so visitors can read
    what kind of project it is without opening it (same as the category grids)."""
    cat = p.get('cat') or ''
    cat_html = f'<span class="pm-cat">{cat}</span>' if cat else ''
    return (f'      <a href="{p["slug"]}" class="pm-card {h_class}">'
            f'<img src="{p["thumb"]}?w=1200&amp;auto=format" alt="{p["title"]}" loading="lazy"/>'
            f'<div class="pm-card-overlay"></div>'
            f'{cat_html}'
            f'<span class="pm-name">{p["title"]}</span>'
            f'<span class="pm-loc">{PIN_SVG}{p["loc"]}</span></a>')

def build_micasa_section_rows(project_items, is_interior=False):
    if not project_items:
        return []

    n = len(project_items)
    # Determine row sizes so every row has 2 or 3 items (never an elongated single card)
    if n == 1:
        row_sizes = [1]
    elif n % 3 == 0:
        row_sizes = [3] * (n // 3)
    elif n % 3 == 2:
        row_sizes = [2] + [3] * (n // 3)
    else: # n % 3 == 1 (e.g. 4 -> [2, 2], 7 -> [2, 2, 3], 10 -> [2, 2, 3, 3])
        row_sizes = [2, 2] + [3] * ((n - 4) // 3)

    rows_html = []
    cursor = 0
    two_row_count = 0

    for r_idx, size in enumerate(row_sizes):
        chunk = project_items[cursor : cursor + size]
        cursor += size
        delay_class = f"d{min(r_idx, 3)}" if r_idx > 0 else ""

        if size == 2:
            two_row_count += 1
            if two_row_count % 3 == 1:
                pmr = "pmr-half" if (is_interior and r_idx == 0) else "pmr-small-big"
                h_class = "pm-tall" if (is_interior and r_idx == 0) else "pm-r43"
            elif two_row_count % 3 == 2:
                pmr = "pmr-big-small"
                h_class = "pm-std"
            else:
                pmr = "pmr-half"
                h_class = "pm-r43"

            cards_html = '\n'.join([pm_card(p, h_class) for p in chunk])
            rows_html.append(f'    <div class="port-grid-micasa {pmr} rv vis {delay_class}">\n{cards_html}\n    </div>')

        elif size == 3:
            h_class = "pm-r32" if (not is_interior and r_idx == 1) else "pm-r43"
            cards_html = '\n'.join([pm_card(p, h_class) for p in chunk])
            rows_html.append(f'    <div class="port-grid-micasa pmr-3 rv vis {delay_class}">\n{cards_html}\n    </div>')

        elif size == 1:
            h_class = "pm-r43"
            cards_html = pm_card(chunk[0], h_class)
            rows_html.append(f'    <div class="port-grid-micasa pmr-full rv vis {delay_class}">\n{cards_html}\n    </div>')

    return rows_html

def update_homepage_and_categories(projects, base_dir):
    # 1. Update index.html Home Page with original Micasa editorial layout
    index_path = os.path.join(base_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_html = f.read()

        # Running projects are pulled out first, so they can never also appear in
        # the Architecture / Interior grids above the Running Projects section.
        on_home = lambda p: (p.get('thumbnail') and not is_hidden_from_home(p)
                             and not is_running(p) and not is_dpr(p))

        arch_list = [p for p in projects if on_home(p) and main_category(p) == 'architecture']
        interior_list = [p for p in projects if on_home(p) and main_category(p) != 'architecture']
        running_list = [p for p in projects if is_running(p) and p.get('thumbnail')]

        # Build Architecture Rows
        p_arch = [{'slug': (p.get('slug') or '').strip().replace(' ', '-'), 'title': (clean_text(p.get('title')) or '').upper(), 'loc': clean_location(p.get('location')), 'thumb': p.get('thumbnail'), 'cat': category_tag(p)} for p in arch_list]
        arch_rows = build_micasa_section_rows(p_arch, is_interior=False)

        # Build Interior Rows
        p_int = [{'slug': (p.get('slug') or '').strip().replace(' ', '-'), 'title': (clean_text(p.get('title')) or '').upper(), 'loc': clean_location(p.get('location')), 'thumb': p.get('thumbnail'), 'cat': category_tag(p)} for p in interior_list]
        interior_rows = build_micasa_section_rows(p_int, is_interior=True)

        full_arch_html = '\n'.join(arch_rows)
        full_interior_html = '\n'.join(interior_rows)

        # Build Running / Ongoing Projects Section conditionally (blank if no projects added yet in Sanity dashboard!)
        running_section_html = ""
        if running_list:
            p_run = [{'slug': (p.get('slug') or '').strip().replace(' ', '-'), 'title': (clean_text(p.get('title')) or '').upper(), 'loc': clean_location(p.get('location')), 'thumb': p.get('thumbnail'), 'cat': 'Ongoing &middot; ' + category_tag(p)} for p in running_list]
            running_rows = build_micasa_section_rows(p_run, is_interior=False)
            full_running_html = '\n'.join(running_rows)
            running_section_html = f'''

    <div class="port-cat-strip rv vis" style="padding-top: clamp(24px,4vw,48px);">
      <div class="port-cat-label">03</div>
      <h2 class="port-cat-h">RUNNING PROJECTS</h2>
    </div>
{full_running_html}'''

        full_portfolio_section = f'''  <!-- PORTFOLIO / FEATURED PROJECTS -->
  <section class="portfolio" id="portfolio">
    <div class="port-cat-strip rv vis" style="padding-top: clamp(16px,2.5vw,32px);">
      <div class="port-cat-label">01</div>
      <h2 class="port-cat-h">ARCHITECTURE</h2>
    </div>
{full_arch_html}

    <div class="port-cat-strip rv vis" style="padding-top: clamp(24px,4vw,48px);">
      <div class="port-cat-label">02</div>
      <h2 class="port-cat-h">INTERIOR DESIGN</h2>
    </div>
{full_interior_html}{running_section_html}
  </section>'''

        import re
        # Anchor on the <section> itself, not the marker comment — the comment has
        # been lost before, which silently froze the homepage grid. The optional
        # prefix swallows a stale comment so we never end up with two of them.
        # A lambda replacement keeps backslashes/& in the HTML literal.
        index_html, n_sub = re.subn(
            r'(?:[ \t]*<!-- PORTFOLIO[^>]*-->\s*)?<section class="portfolio" id="portfolio">[\s\S]*?</section>',
            lambda m: full_portfolio_section,
            index_html,
            count=1
        )

        if not n_sub:
            print("WARNING: portfolio section not found in index.html — homepage grid NOT updated.")
        else:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(index_html)
            print(f"Pre-rendered index.html with Micasa layout ({len(arch_rows)} Architecture rows, {len(interior_rows)} Interior rows, {len(running_list)} Running projects).")

    # 2. Update Category Pages
    cat_configs = {
        "architecture.html": lambda p: main_category(p) == 'architecture',
        "interiors.html": lambda p: main_category(p) != 'architecture',
        "residential.html": lambda p: sub_category(p) == 'residential',
        "commercial.html": lambda p: sub_category(p) == 'commercial',
        "hospitality.html": lambda p: sub_category(p) == 'hospitality',
        "healthcare.html": lambda p: sub_category(p) == 'healthcare',
        "education.html": lambda p: sub_category(p) == 'education',
        "workplace.html": lambda p: sub_category(p) == 'workplace',
        "club-resort.html": lambda p: sub_category(p) == 'club-resort',
        "dpr-landscaping.html": is_dpr,
    }

    for fname, filter_fn in cat_configs.items():
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Two page-level invariants, enforced here rather than in each filter:
        # running projects are home-page-only, and DPR work appears on the DPR
        # page and nowhere else.
        dpr_page = (fname == "dpr-landscaping.html")
        cat_projs = [p for p in projects
                     if filter_fn(p) and p.get('thumbnail')
                     and not is_running(p)
                     and is_dpr(p) == dpr_page]
        cards = []
        for idx, p in enumerate(cat_projs):
            slug = (p.get('slug') or '').strip().replace(' ', '-')
            title = p.get('title', '').upper()
            loc = clean_location(p.get('location'))
            thumb = p.get('thumbnail')
            eyebrow = category_tag(p)
            is_span2 = 'span2' if idx == 0 else ''
            num = str(idx + 1).zfill(2)
            cards.append(f'''    <a href="{slug}" class="proj-card rv vis {is_span2}">
      <img src="{thumb}?w=1200&amp;auto=format" alt="{title}" loading="lazy"/>
      <div class="proj-card-overlay"></div>
      <div class="proj-card-cat">{eyebrow}</div>
      <div class="proj-card-info">
        <div class="proj-card-num">{num}</div>
        <div class="proj-card-name">{title}</div>
        <div class="proj-card-loc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>{loc}</div>
      </div>
    </a>''')

        # Visitor-facing empty state — this renders on the live site, so it reads
        # as a note to a client rather than a note to whoever runs the dashboard.
        empty_html = ('\n    <div style="grid-column: 1 / -1; padding: 60px 0; text-align: center; '
                      'color: var(--mist); font-size: 14px; letter-spacing: 0.05em;">'
                      'Selected projects for this service line will be published here shortly.</div>\n')
        grid_html = '\n' + '\n'.join(cards) + '\n' if cards else empty_html

        wrap_html = f'''<div class="projects-wrap">\n  <div class="projects-grid">{grid_html}  </div>\n</div>'''

        import re
        # Stop at whatever comes after the grid on this page. Pages differ — most
        # have an SEO block next, dpr-landscaping.html has the inquiry band — so
        # every known follower is listed here. Miss one and the replacement eats
        # the rest of the page down to the footer.
        content = re.sub(
            r'<div class="projects-wrap">[\s\S]*?'
            r'(?=(?:<!--\s*SEO|<section class="seo|<div class="inquiry-band"'
            r'|<!--\s*=+\s*COMMON TAIL|<section class="contact|<footer|<div class="footer))',
            wrap_html + '\n\n',
            content,
            count=1
        )
        content = re.sub(
            r'(<div class="page-count[^"]*"[^>]*>)[^<]*(</div>)',
            r'\g<1>' + str(len(cat_projs)).zfill(2) + r'\2',
            content
        )
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Pre-rendered {fname} with {len(cat_projs)} projects.")

    # 3. Process Blogs from Sanity
    blogs = fetch_sanity_blogs()
    if blogs:
        print(f"Fetched {len(blogs)} blog articles from Sanity.")
        build_blog_pages(blogs, base_dir)
        update_blog_index(blogs, base_dir)

SITE = "https://nextgeninterior.com"

# Crawl weight for the pages that deserve a considered value. Anything not
# listed falls through to sitemap_meta() below, which is what lets a brand new
# page appear in the sitemap without anyone editing this file.
SITEMAP_PRIORITY = {
    '/': ('1.0', 'weekly'),
    '/architecture': ('0.9', 'weekly'),
    '/interiors': ('0.9', 'weekly'),
    '/dpr-landscaping': ('0.9', 'monthly'),
    '/residential': ('0.8', 'weekly'),
    '/commercial': ('0.8', 'weekly'),
    '/hospitality': ('0.8', 'weekly'),
    '/workplace': ('0.7', 'monthly'),
    '/club-resort': ('0.7', 'monthly'),
    '/healthcare': ('0.7', 'monthly'),
    '/education': ('0.7', 'monthly'),
    '/blog': ('0.8', 'weekly'),
    '/careers': ('0.5', 'monthly'),
}

# Pages that exist but must never be advertised.
SITEMAP_SKIP_SLUGS = {'chapur-hotel'}

_CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
_NOINDEX_RE = re.compile(r'<meta[^>]+name="robots"[^>]+content="[^"]*noindex', re.I)


def page_url(rel_path):
    """Public URL for a file path relative to the site root."""
    rel = rel_path.replace(os.sep, '/')
    if rel == 'index.html':
        return SITE + '/'
    return SITE + '/' + rel[:-len('.html')]


def sitemap_meta(path, project_slugs):
    """(priority, changefreq) for a URL path such as '/blogs/some-post'."""
    if path in SITEMAP_PRIORITY:
        return SITEMAP_PRIORITY[path]
    if path.startswith('/blogs/'):
        return ('0.7', 'monthly')
    if path.startswith('/locations/'):
        return ('0.8', 'monthly')
    if path.lstrip('/') in project_slugs:
        return ('0.7', 'monthly')
    return ('0.8', 'monthly')


def discover_pages(base_dir):
    """Every page that should be in the sitemap, found by walking the site.

    A page is included only when its own canonical points at itself. That single
    rule keeps duplicates out without a maintained exclusion list: the eight SEO
    landing pages that also sit under blogs/, and the five location pages that
    also sit at the root, all canonicalise to one address, so only that address
    is advertised. Pages marked noindex are skipped for the same reason.
    """
    patterns = ['*.html', os.path.join('blogs', '*.html'), os.path.join('locations', '*.html')]
    found = []
    for pattern in patterns:
        for full in sorted(glob.glob(os.path.join(base_dir, pattern))):
            rel = os.path.relpath(full, base_dir)
            try:
                with open(full, encoding='utf-8', errors='ignore') as f:
                    head = f.read(8000)
            except OSError:
                continue
            if _NOINDEX_RE.search(head):
                continue
            match = _CANONICAL_RE.search(head)
            if not match:
                print("  ! %s has no canonical tag — left out of the sitemap." % rel)
                continue
            own = page_url(rel)
            if match.group(1).rstrip('/') != own.rstrip('/'):
                continue  # duplicate; its canonical target is listed instead
            found.append(own)
    return found


def generate_sitemap(projects, base_dir):
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')

    project_slugs = {(p.get('slug') or '').strip().replace(' ', '-')
                     for p in projects if p.get('slug')}

    urls = []
    for url in discover_pages(base_dir):
        path = '/' + url[len(SITE):].lstrip('/')
        if path.lstrip('/') in SITEMAP_SKIP_SLUGS:
            continue
        urls.append((url, path))

    # Home first, then everything else alphabetically, so diffs stay readable.
    urls.sort(key=lambda item: (item[1] != '/', item[1]))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, path in urls:
        prio, freq = sitemap_meta(path, project_slugs)
        lines.append("""  <url>
    <loc>%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>%s</changefreq>
    <priority>%s</priority>
  </url>""" % (url, today, freq, prio))
    lines.append('</urlset>')

    with open(os.path.join(base_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # A generated project page that never made it into the sitemap means the
    # page is missing or its canonical is wrong — worth saying out loud.
    listed = {path.lstrip('/') for _, path in urls}
    orphans = sorted(s for s in project_slugs if s not in listed and s not in SITEMAP_SKIP_SLUGS)
    if orphans:
        print("  ! Project pages missing from sitemap: " + ', '.join(orphans))
    print("Generated sitemap.xml with %d URLs (%d pages discovered on disk)." % (len(urls), len(urls)))


if __name__ == '__main__':
    build()
