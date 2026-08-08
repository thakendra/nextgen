const PROJECT_ID = 'gpyk0ky0';
const DATASET = 'production';

async function fetchSanityProjects() {
  const path = window.location.pathname.toLowerCase();
  
  let pageName = 'interiors';
  if (path.includes('architecture')) pageName = 'architecture';
  else if (path.includes('residential')) pageName = 'residential';
  else if (path.includes('commercial')) pageName = 'commercial';
  else if (path.includes('hospitality')) pageName = 'hospitality';
  else if (path.includes('healthcare')) pageName = 'healthcare';
  else if (path.includes('education')) pageName = 'education';
  else if (path.includes('workplace')) pageName = 'workplace';
  else if (path.includes('club-resort')) pageName = 'club-resort';
  else if (path.includes('dpr-landscaping')) pageName = 'dpr-landscaping';

  let filter = '*[_type == "project"]';
  
  if (pageName === 'interiors') {
    // Show projects marked as interiors OR any interior subcategories
    filter = '*[_type == "project" && (mainCategory == "interiors" || subCategory in ["residential","commercial","hospitality","healthcare","education","workplace","club-resort"])]';
  } else if (pageName === 'architecture') {
    // Show projects marked as architecture
    filter = '*[_type == "project" && (mainCategory == "architecture" || subCategory in ["dpr-landscaping"])]';
  } else {
    // Subcategory page (e.g. residential, commercial, hospitality)
    filter = `*[_type == "project" && (subCategory == "${pageName}" || mainCategory == "${pageName}")]`;
  }

  const query = encodeURIComponent(`${filter} | order(_createdAt desc) {
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
    return data.result || [];
  } catch (error) {
    console.error('Error fetching from Sanity:', error);
    return [];
  }
}

async function renderCategoryGrid() {
  const grid = document.querySelector('.projects-grid');
  if (!grid) return;
  
  const projects = await fetchSanityProjects();
  if (!projects || projects.length === 0) return;
  
  // Prepend each project to the top of the grid
  [...projects].reverse().forEach((proj, idx) => {
    if (!proj.thumbnailUrl) return;
    
    const a = document.createElement('a');
    // Clicking the thumbnail opens the dedicated client page
    a.href = `${proj.slug}`; 
    a.className = `proj-card rv vis`;
    
    const catLabel = proj.eyebrow || (proj.subCategory ? proj.subCategory.toUpperCase() : (proj.mainCategory || 'PROJECT').toUpperCase());
    
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
