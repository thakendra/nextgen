// gallery-page.js — shared script for all client gallery pages

const menuBtn=document.getElementById('menuBtn'),mMenu=document.getElementById('mMenu');
function openMenu(){menuBtn.classList.add('open');mMenu.classList.add('open');document.body.style.overflow='hidden';}
function closeMenu(){menuBtn.classList.remove('open');mMenu.classList.remove('open');document.body.style.overflow='';}
menuBtn.addEventListener('click',()=>mMenu.classList.contains('open')?closeMenu():openMenu());
document.getElementById('mMenuClose').addEventListener('click',closeMenu);
mMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
const mPBtn=document.getElementById('mPortfolioBtn'),mPSub=document.getElementById('mPortfolioSub');
mPBtn.addEventListener('click',()=>{const o=mPSub.classList.contains('open');mPSub.classList.toggle('open',!o);mPBtn.classList.toggle('active',!o);});

let LB_PHOTOS=[],LB_FOLDER='',LB_PROJECT='',lbCurrent=0;
const lb=document.getElementById('lb'),lbImg=document.getElementById('lbImg'),lbCounter=document.getElementById('lbCounter');

function initGallery(folder,photos,project){
  LB_FOLDER=folder;LB_PHOTOS=photos;LB_PROJECT=project;
  const heroImg=document.getElementById('heroImg');
  if(heroImg) heroImg.src=encodeURI(folder+photos[0]);
  const grid=document.getElementById('gallery');
  photos.forEach((f,i)=>{
    const a=document.createElement('a');a.className='g-card';a.href='javascript:void(0)';a.onclick=()=>openLb(i);
    a.innerHTML=`<img src="${encodeURI(folder+f)}" alt="${project} ${i+1}" loading="lazy"/><div class="g-card-overlay"></div><div class="g-card-num">${String(i+1).padStart(2,'0')}</div><div class="g-card-zoom"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>`;
    grid.appendChild(a);
  });
}

function openLb(idx){lbCurrent=idx;updateLb();lb.classList.add('open');document.body.style.overflow='hidden';}
function closeLb(){lb.classList.remove('open');document.body.style.overflow='';}
function closeLbOnBg(e){if(e.target===lb)closeLb();}
function lbNav(dir){lbCurrent=(lbCurrent+dir+LB_PHOTOS.length)%LB_PHOTOS.length;updateLb();}
function updateLb(){lbImg.src=encodeURI(LB_FOLDER+LB_PHOTOS[lbCurrent]);lbImg.alt=LB_PROJECT+' '+(lbCurrent+1);lbCounter.textContent=(lbCurrent+1)+' / '+LB_PHOTOS.length;}
document.addEventListener('keydown',e=>{if(!lb.classList.contains('open'))return;if(e.key==='Escape')closeLb();if(e.key==='ArrowLeft')lbNav(-1);if(e.key==='ArrowRight')lbNav(1);});

