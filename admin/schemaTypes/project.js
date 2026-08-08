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
      name: 'mainCategory',
      title: '1. Main Category',
      type: 'string',
      options: {
        list: [
          { title: 'Interiors', value: 'interiors' },
          { title: 'Architecture', value: 'architecture' },
        ],
        layout: 'radio',
      },
      validation: (Rule) => Rule.required(),
      description: 'Select whether this is an Interior or Architecture project.',
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
      validation: (Rule) =>
        Rule.required().custom((value) => {
          if (!value?.asset?._ref) return true;
          if (!value.asset._ref.endsWith('-webp')) {
            return 'Only WebP (.webp) format is allowed for high performance.';
          }
          return true;
        }),
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
      title: 'Inner Gallery Showcase Photos (Max 10, WebP only, <500KB)',
      description: 'Upload between 1 and 10 high-resolution WebP images. You can select multiple images at once (Ctrl+Click) or drag & drop up to 10 files directly into this box!',
      type: 'array',
      options: {
        layout: 'grid',
      },
      validation: (Rule) =>
        Rule.max(10)
          .error('Maximum 10 inner gallery photos allowed for optimal loading speed.')
          .custom((images) => {
            if (!images || !Array.isArray(images)) return true;
            for (let i = 0; i < images.length; i++) {
              const img = images[i];
              if (img?.asset?._ref && !img.asset._ref.endsWith('-webp')) {
                return `Image #${i + 1} must be in WebP (.webp) format.`;
              }
            }
            return true;
          }),
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
