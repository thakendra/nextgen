export const project = {
  name: 'project',
  title: 'Project / Showcase',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Project / Client Name',
      type: 'string',
      description: 'e.g. "Sankhu Residence" or "Maya Cafe" or "Bhattrai Home"',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'slug',
      title: 'Page URL Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96,
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'featuredOnHome',
      title: '🌟 Do you want to show this project on Home Page?',
      type: 'string',
      options: {
        list: [
          { title: '✅ YES — Show in Architecture / Interior Showcase', value: 'yes' },
          { title: '🚧 RUNNING — Show in Running Projects Section', value: 'running' },
          { title: '❌ NO — Hide from Home Page Showcase', value: 'no' },
        ],
        layout: 'radio',
      },
      initialValue: 'yes',
      description: 'Select YES for Architecture/Interior grid, RUNNING for Running Projects section, or NO to hide from Home Page.',
    },
    {
      name: 'projectStatus',
      title: '🏗️ Project Status (Completed vs Running/Ongoing)',
      type: 'string',
      options: {
        list: [
          { title: '✅ Completed Project', value: 'completed' },
          { title: '🚧 Running / Ongoing Project (Under Construction)', value: 'running' },
        ],
        layout: 'radio',
      },
      initialValue: 'completed',
      description: 'Mark as "Running / Ongoing Project" to showcase in the Running Projects section on the Home Page.',
    },
    {
      name: 'mainCategory',
      title: '1. Main Category',
      type: 'string',
      options: {
        list: [
          { title: 'Architecture', value: 'architecture' },
          { title: 'Interior Design', value: 'interiors' },
          { title: '🌿 DPR & Landscaping', value: 'dpr-landscaping' },
          { title: 'Ongoing Project', value: 'ongoing-projects' },
        ],
        layout: 'radio',
      },
      validation: (Rule) => Rule.required(),
      description: 'Select whether this is an Interior or Architecture project. DPR & Landscaping projects appear on the DPR & Landscaping page only — not on the Home Page or the other category pages.',
    },
    {
      name: 'subCategory',
      title: '2. Sub Category',
      type: 'string',
      options: {
        list: [
          { title: 'Residential', value: 'residential' },
          { title: 'Commercial', value: 'commercial' },
          { title: 'Hospitality', value: 'hospitality' },
          { title: 'Healthcare', value: 'healthcare' },
          { title: 'Education', value: 'education' },
          { title: 'Workplace', value: 'workplace' },
          { title: 'Club or Resort', value: 'club-resort' },
          { title: 'DPR & Landscaping', value: 'dpr-landscaping' },
        ],
      },
      validation: (Rule) => Rule.required(),
      description: 'Select the specific sub-category (will show on both Main and Subcategory pages).',
    },
    {
      name: 'thumbnail',
      title: 'Thumbnail Image (Listing Cover)',
      type: 'image',
      description: 'WebP format only (< 500KB). The cover image shown in the category listing grid.',
      options: {
        hotspot: true,
        accept: 'image/webp',
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'eyebrow',
      title: 'Eyebrow Tag',
      type: 'string',
      description: 'e.g. "Residential · Private Home" or "Hospitality · Hotel" or "Residential · Heritage Architecture"',
    },
    {
      name: 'location',
      title: 'Location',
      type: 'string',
      description: 'e.g. "Kathmandu, Nepal" or "Sankhu, Kathmandu Valley"',
    },
    {
      name: 'intro_heading',
      title: 'Showcase Intro Heading',
      type: 'string',
      description: 'e.g. "HERITAGE MEETS MODERN LIVING" or "A REFINED KATHMANDU RESIDENCE"',
    },
    {
      name: 'intro_text',
      title: 'Showcase Description (2 Paragraphs recommended)',
      type: 'text',
      rows: 4,
      description: 'Detailed overview of the project design, materials, and concept.',
    },
    {
      name: 'galleryImages',
      title: 'Inner Gallery Showcase Photos (Max 10, WebP recommended)',
      description: 'Upload between 1 and 10 high-resolution images. You can select multiple images at once (Ctrl+Click) or drag & drop up to 10 files directly into this box!',
      type: 'array',
      options: {
        layout: 'grid',
      },
      validation: (Rule) =>
        Rule.max(10)
          .error('Maximum 10 inner gallery photos allowed for optimal loading speed.'),
      of: [
        {
          type: 'image',
          options: {
            hotspot: true,
            accept: 'image/webp',
          },
          fields: [
            {
              name: 'caption',
              type: 'string',
              title: 'Showcase Label / Caption',
              description: 'e.g. "Front Elevation", "Garden Approach", "Detail & Brickwork"',
            },
            {
              name: 'alt',
              type: 'string',
              title: 'Alt Text for SEO',
            },
          ],
        },
      ],
    },
    {
      name: 'description',
      title: 'SEO Meta Description',
      type: 'text',
      rows: 2,
      description: 'Search engine description for Google (~140-155 characters).',
    },
  ],
}
