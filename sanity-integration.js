const PROJECT_ID = 'gpyk0ky0';
const DATASET = 'production';

async function fetchSanityProjects() {
  // Query all projects with resolved thumbnail url
  const query = encodeURIComponent(`*[_type == "project"] | order(_createdAt desc) {
    title, 
    "slug": slug.current, 
    location,
    eyebrow,
    mainCategory,
    subCategory,
    "thumbnailUrl": thumbnail.asset->url
  }`);
  
  const url = `https://${PROJECT_ID}.api.sanity.io/v2021-10-21/data/query/${DATASET}?query=${query}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    console.log('[Sanity] Fetched projects:', data.result);
    return data.result || [];
  } catch (error) {
    console.error('[Sanity] Error fetching:', error);
    return [];
  }
}

async function renderCategoryGrid() {
  const grid = document.querySelector('.projects-grid');
  if (!grid) return;
  
  const path = window.location.pathname.toLowerCase();
  const allProjects = await fetchSanityProjects();
  if (!allProjects || allProjects.length === 0) return;
  
  // Filter projects for the current page
  const filtered = allProjects.filter(p => {
    if (!p.thumbnailUrl) return false;
    
    const main = (p.mainCategory || '').toLowerCase();
    const sub = (p.subCategory || '').toLowerCase();
    
    if (path.includes('architecture')) {
      return main === 'architecture' || sub.includes('architecture') || sub === 'dpr-landscaping';
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
      // Show all interior projects or any project with an interior subcategory
      return main === 'interiors' || ['residential','commercial','hospitality','healthcare','education','workplace','club-resort'].includes(sub) || !main;
    }
    return true;
  });

  console.log('[Sanity] Filtered for this page (' + path + '):', filtered);

  // Prepend each project to the top of the grid
  filtered.reverse().forEach((proj, idx) => {
    const a = document.createElement('a');
    // Ensure slug is used
    const linkSlug = proj.slug || proj.title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    a.href = linkSlug;
    a.className = 'proj-card rv vis';
    
    const catLabel = proj.eyebrow || (proj.subCategory ? proj.subCategory.toUpperCase() : 'INTERIOR');
    
    a.innerHTML = `
      <img src="${proj.thumbnailUrl}?w=1200&auto=format" alt="${proj.title}"/>
      <div class="proj-card-overlay"></div>
      <div class="proj-card-cat">${catLabel}</div>
      <div class="proj-card-info">
        <div class="proj-card-num">${String(idx + 1).padStart(2, '0')}</div>
        <div class="proj-card-name">${proj.title}</div>
        <div class="proj-card-loc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>${proj.location || 'Kathmandu, Nepal'}</div>
      </div>
    `;
    
    grid.prepend(a);
  });
}

document.addEventListener('DOMContentLoaded', renderCategoryGrid);
