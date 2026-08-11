const PROJECT_ID = 'gpyk0ky0';
const DATASET = 'production';

async function fetchSanityProjects() {
  const query = encodeURIComponent(`*[_type == "project"] | order(_createdAt desc) {
    title, 
    "slug": slug.current, 
    location,
    eyebrow,
    mainCategory,
    subCategory,
    featuredOnHome,
    "thumbnailUrl": coalesce(thumbnail.asset->url, thumbnail.asset.asset->url, galleryImages[0].asset.asset->url, galleryImages[0].asset->url)
  }`);
  
  const url = `https://${PROJECT_ID}.api.sanity.io/v2021-10-21/data/query/${DATASET}?query=${query}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data.result || [];
  } catch (error) {
    console.error('[Sanity] Fetch Error:', error);
    return [];
  }
}

async function renderCategoryGrid() {
  const grid = document.querySelector('.projects-grid');
  if (!grid) return;
  
  const path = window.location.pathname.toLowerCase();
  const allProjects = await fetchSanityProjects();
  if (!allProjects || allProjects.length === 0) return;
  
  // Clean filtering logic matching main and subcategories
  const filtered = allProjects.filter(p => {
    if (!p.thumbnailUrl || p.thumbnailUrl === 'None') return false;
    
    const main = (p.mainCategory || '').toLowerCase();
    const sub = (p.subCategory || '').toLowerCase();
    
    if (path.includes('architecture')) {
      return main === 'architecture' || sub === 'dpr-landscaping' || sub.includes('exterior');
    }
    if (path.includes('residential')) {
      return sub === 'residential';
    }
    if (path.includes('commercial')) {
      return sub === 'commercial';
    }
    if (path.includes('hospitality')) {
      return sub === 'hospitality';
    }
    if (path.includes('healthcare')) {
      return sub === 'healthcare';
    }
    if (path.includes('education')) {
      return sub === 'education';
    }
    if (path.includes('workplace')) {
      return sub === 'workplace';
    }
    if (path.includes('club-resort')) {
      return sub === 'club-resort';
    }
    if (path.includes('dpr-landscaping')) {
      return sub === 'dpr-landscaping';
    }
    if (path.includes('interiors') || path === '/' || path.endsWith('/index.html')) {
      return main === 'interiors' || ['residential','commercial','hospitality','healthcare','education','workplace','club-resort'].includes(sub) || !main;
    }
    return true;
  });

  if (filtered.length === 0) {
    const pageCount = document.querySelector('.page-count');
    if (pageCount) pageCount.textContent = '00';
    return;
  }

  // Clear static old fallback and render pure live Sanity projects
  grid.innerHTML = '';

  filtered.forEach((proj, idx) => {
    const a = document.createElement('a');
    const linkSlug = proj.slug || proj.title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    a.href = linkSlug;
    
    const isFirst = idx === 0;
    a.className = `proj-card rv vis ${isFirst ? 'span2' : ''}`;
    
    const catLabel = proj.eyebrow || (proj.subCategory ? proj.subCategory.toUpperCase() : 'PROJECT');
    
    a.innerHTML = `
      <img src="${proj.thumbnailUrl}?w=1200&auto=format" alt="${proj.title}" loading="lazy"/>
      <div class="proj-card-overlay"></div>
      <div class="proj-card-cat">${catLabel}</div>
      <div class="proj-card-info">
        <div class="proj-card-num">${String(idx + 1).padStart(2, '0')}</div>
        <div class="proj-card-name">${proj.title.toUpperCase()}</div>
        <div class="proj-card-loc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>${proj.location || 'Kathmandu, Nepal'}</div>
      </div>
    `;
    
    grid.appendChild(a);
  });
  
  const pageCount = document.querySelector('.page-count');
  if (pageCount) {
    pageCount.textContent = String(filtered.length).padStart(2, '0');
  }
}

async function renderHomePageFeatured() {
  const archContainer = document.getElementById('homeArchGrid');
  const interiorContainer = document.getElementById('homeInteriorGrid');
  if (!archContainer && !interiorContainer) return;

  const allProjects = await fetchSanityProjects();
  const featured = allProjects.filter(p => p.featuredOnHome === true && p.thumbnailUrl && p.thumbnailUrl !== 'None');
  
  const archProjects = (featured.length > 0 ? featured : allProjects).filter(p => (p.mainCategory || '').toLowerCase() === 'architecture');
  const interiorProjects = (featured.length > 0 ? featured : allProjects).filter(p => (p.mainCategory || '').toLowerCase() !== 'architecture');

  if (archContainer && archProjects.length > 0) {
    archContainer.innerHTML = '';
    archProjects.forEach(proj => {
      if (!proj.thumbnailUrl) return;
      const a = document.createElement('a');
      a.href = proj.slug || '#';
      a.className = 'pm-card pm-r43';
      a.innerHTML = `
        <img src="${proj.thumbnailUrl}?w=1200&auto=format" alt="${proj.title}"/>
        <div class="pm-card-overlay"></div>
        <span class="pm-name">${proj.title.toUpperCase()}</span>
        <span class="pm-loc">&#128205; ${proj.location || 'Kathmandu, Nepal'}</span>
      `;
      archContainer.appendChild(a);
    });
  }

  if (interiorContainer && interiorProjects.length > 0) {
    interiorContainer.innerHTML = '';
    interiorProjects.forEach(proj => {
      if (!proj.thumbnailUrl) return;
      const a = document.createElement('a');
      a.href = proj.slug || '#';
      a.className = 'pm-card pm-tall';
      a.innerHTML = `
        <img src="${proj.thumbnailUrl}?w=1200&auto=format" alt="${proj.title}"/>
        <div class="pm-card-overlay"></div>
        <span class="pm-name">${proj.title.toUpperCase()}</span>
        <span class="pm-loc">&#128205; ${proj.location || 'Kathmandu, Nepal'}</span>
      `;
      interiorContainer.appendChild(a);
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderCategoryGrid();
  renderHomePageFeatured();
});
