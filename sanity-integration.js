const PROJECT_ID = 'gpyk0ky0';
const DATASET = 'production';

async function fetchSanityProjectsForCurrentCategory() {
  // Determine current category from the URL
  // e.g. /interiors.html or /architecture.html or /hospitality.html
  const path = window.location.pathname.toLowerCase();
  let categorySlug = '';
  
  if (path.includes('interiors')) categorySlug = 'interiors';
  else if (path.includes('architecture')) categorySlug = 'architecture';
  else if (path.includes('residential')) categorySlug = 'residential';
  else if (path.includes('commercial')) categorySlug = 'commercial';
  else if (path.includes('hospitality')) categorySlug = 'hospitality';
  else if (path.includes('healthcare')) categorySlug = 'healthcare';
  else if (path.includes('education')) categorySlug = 'education';
  else if (path.includes('workplace')) categorySlug = 'workplace';
  else if (path.includes('club-resort')) categorySlug = 'club-resort';

  let filter = '*[_type == "project"]';
  if (categorySlug) {
    // If on a specific category page, only fetch projects matching that category
    // or fetch all if it's general interiors
    if (categorySlug === 'interiors') {
      filter = '*[_type == "project"]';
    } else {
      filter = `*[_type == "project" && category->slug.current == "${categorySlug}"]`;
    }
  }

  const query = encodeURIComponent(`${filter} | order(_createdAt desc) {
    title, 
    "slug": slug.current, 
    location,
    "thumbnailUrl": thumbnail.asset->url, 
    "categoryName": category->title,
    "categorySlug": category->slug.current
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
  
  const projects = await fetchSanityProjectsForCurrentCategory();
  if (!projects || projects.length === 0) return;
  
  // Prepend each project so it appears in the grid, matching the exact old style
  [...projects].reverse().forEach((proj, idx) => {
    const a = document.createElement('a');
    // Clicking the thumbnail opens the dedicated client page!
    a.href = `${proj.slug}`; 
    a.className = `proj-card rv vis`;
    
    a.innerHTML = `
      <img src="${proj.thumbnailUrl}?w=1200&auto=format" alt="${proj.title}"/>
      <div class="proj-card-overlay"></div>
      <div class="proj-card-cat">${proj.categoryName || 'Project'}</div>
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
