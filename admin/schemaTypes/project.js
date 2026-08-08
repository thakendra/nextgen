export const project = {
  name: 'project',
  title: 'Project / Showcase',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Project / Client Name',
      type: 'string',
      description: 'e.g. "Bhattrai Home" or "Maya Cafe" or "Chapur Hotel"',
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
      description: 'The photo shown in the grid before clicking to open the dedicated page.',
      options: {
        hotspot: true,
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'eyebrow',
      title: 'Eyebrow Tag',
      type: 'string',
      description: 'e.g. "Residential · Private Home" or "Hospitality · Hotel"',
    },
    {
      name: 'location',
      title: 'Location',
      type: 'string',
      description: 'e.g. "Kathmandu, Nepal" or "Bharatpur, Chitwan"',
    },
    {
      name: 'intro_heading',
      title: 'Showcase Intro Heading',
      type: 'string',
      description: 'e.g. "A REFINED KATHMANDU RESIDENCE"',
    },
    {
      name: 'intro_text',
      title: 'Showcase Description',
      type: 'text',
      description: 'A 2-3 sentence overview of this project for the dedicated page.',
    },
    {
      name: 'galleryImages',
      title: 'Inner Gallery Photos',
      description: 'Upload all photos for this project (will display in the grid with lightbox).',
      type: 'array',
      of: [
        {
          type: 'image',
          options: {
            hotspot: true,
          },
          fields: [
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
      description: 'Search engine description for Google.',
    },
  ],
}
