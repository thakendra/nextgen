const PROJECT_ID = 'gpyk0ky0';
const DATASET = 'production';

const RUNNING_CATEGORIES = ['ongoing-projects', 'running-projects', 'ongoing', 'running'];

// Running / ongoing projects live only in the Running Projects section of the
// home page — never in a category listing. Mirrors is_running() in build_from_sanity.py.
const isRunningProject = p =>
  RUNNING_CATEGORIES.includes((p.mainCategory || '').toLowerCase()) ||
  p.projectStatus === 'running' ||
  p.featuredOnHome === 'running';

// DPR & Landscaping is its own service line: it belongs on dpr-landscaping.html
// and nowhere else. Mirrors is_dpr() in build_from_sanity.py.
const isDprProject = p =>
  (p.mainCategory || '').toLowerCase() === 'dpr-landscaping' ||
  (p.subCategory || '').toLowerCase() === 'dpr-landscaping';

async function fetchSanityProjects() {
  const query = encodeURIComponent(`*[_type == "project"] | order(_createdAt desc) {
    title, 
    "slug": slug.current, 
    location,
    eyebrow,
    mainCategory,
    subCategory,
    featuredOnHome,
    projectStatus,
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

  // Category pages are pre-rendered by build_from_sanity.py — skip to avoid duplicates
  if (grid.querySelectorAll('.proj-card').length > 0) return;
  
  const path = window.location.pathname.toLowerCase();
  const allProjects = await fetchSanityProjects();
  
  // Clean filtering logic matching main and subcategories
  const filtered = allProjects.filter(p => {
    if (!p.thumbnailUrl || p.thumbnailUrl === 'None') return false;
    if (isRunningProject(p)) return false;

    const main = (p.mainCategory || '').toLowerCase();
    const sub = (p.subCategory || '').toLowerCase();

    // DPR first: its page takes only DPR work, and every other page takes none.
    if (path.includes('dpr-landscaping')) return isDprProject(p);
    if (isDprProject(p)) return false;

    if (path.includes('architecture')) {
      return main === 'architecture' || sub.includes('exterior');
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
    if (path.includes('interiors') || path === '/' || path.endsWith('/index.html')) {
      return main === 'interiors' || ['residential','commercial','hospitality','healthcare','education','workplace','club-resort'].includes(sub) || !main;
    }
    return true;
  });

  // Clear static old fallback
  grid.innerHTML = '';

  if (filtered.length === 0) {
    // Same visitor-facing wording as the pre-rendered empty state in
    // build_from_sanity.py — this text is public, so it reads as a note to a
    // client rather than to whoever runs the dashboard.
    grid.innerHTML = `<div style="grid-column: 1 / -1; padding: 60px 0; text-align: center; color: var(--mist); font-size: 14px; letter-spacing: 0.05em;">Selected projects for this service line will be published here shortly.</div>`;
    return;
  }

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
}

async function renderHomePageFeatured() {
  // Home page is pre-rendered by build_from_sanity.py — skip to avoid duplicates
  if (document.querySelectorAll('.pm-card').length > 0) return;
  const archContainer = document.getElementById('homeArchGrid');
  const interiorContainer = document.getElementById('homeInteriorGrid');
  if (!archContainer && !interiorContainer) return;

  const allProjects = await fetchSanityProjects();
  if (!allProjects || allProjects.length === 0) return;

  // Support both YES/NO radio selection and legacy booleans
  const isFeatured = p => (p.featuredOnHome === 'yes' || p.featuredOnHome === true) && p.thumbnailUrl && p.thumbnailUrl !== 'None' && !isRunningProject(p) && !isDprProject(p);
  const isExcluded = p => (p.featuredOnHome === 'no' || p.featuredOnHome === false) || isRunningProject(p) || isDprProject(p);

  const featuredArch = allProjects.filter(p => isFeatured(p) && (p.mainCategory || '').toLowerCase() === 'architecture');
  const featuredInterior = allProjects.filter(p => isFeatured(p) && (p.mainCategory || '').toLowerCase() !== 'architecture');

  // If specific projects are chosen with YES, show them; otherwise show active projects that are not excluded with NO
  const archList = featuredArch.length > 0 ? featuredArch : allProjects.filter(p => !isExcluded(p) && (p.mainCategory || '').toLowerCase() === 'architecture' && p.thumbnailUrl).slice(0, 4);
  const interiorList = featuredInterior.length > 0 ? featuredInterior : allProjects.filter(p => !isExcluded(p) && (p.mainCategory || '').toLowerCase() !== 'architecture' && p.thumbnailUrl).slice(0, 4);

  if (archContainer) {
    archContainer.innerHTML = '';
    archList.forEach((proj, idx) => {
      if (!proj.thumbnailUrl) return;
      const a = document.createElement('a');
      a.href = proj.slug || '#';
      a.className = 'pm-card pm-r43';
      const catTag = proj.eyebrow || (proj.subCategory ? proj.subCategory.replace(/-/g, ' ') : '');
      a.innerHTML = `
        <img src="${proj.thumbnailUrl}?w=1200&auto=format" alt="${proj.title}" loading="lazy"/>
        <div class="pm-card-overlay"></div>
        ${catTag ? `<span class="pm-cat">${catTag}</span>` : ''}
        <span class="pm-name">${proj.title.toUpperCase()}</span>
        <span class="pm-loc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>${proj.location || 'Kathmandu, Nepal'}</span>
      `;
      archContainer.appendChild(a);
    });
  }

  if (interiorContainer) {
    interiorContainer.innerHTML = '';
    interiorList.forEach((proj, idx) => {
      if (!proj.thumbnailUrl) return;
      const a = document.createElement('a');
      a.href = proj.slug || '#';
      a.className = 'pm-card pm-tall';
      const catTag = proj.eyebrow || (proj.subCategory ? proj.subCategory.replace(/-/g, ' ') : '');
      a.innerHTML = `
        <img src="${proj.thumbnailUrl}?w=1200&auto=format" alt="${proj.title}" loading="lazy"/>
        <div class="pm-card-overlay"></div>
        ${catTag ? `<span class="pm-cat">${catTag}</span>` : ''}
        <span class="pm-name">${proj.title.toUpperCase()}</span>
        <span class="pm-loc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>${proj.location || 'Kathmandu, Nepal'}</span>
      `;
      interiorContainer.appendChild(a);
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderCategoryGrid();
  renderHomePageFeatured();
});
