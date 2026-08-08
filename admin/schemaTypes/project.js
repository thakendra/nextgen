export const project = {
  name: 'project',
  title: 'Project / Portfolio',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Project Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96,
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'client',
      title: 'Client',
      type: 'reference',
      to: [{ type: 'client' }],
      description: 'Which client is this project for?',
    },
    {
      name: 'category',
      title: 'Category',
      type: 'reference',
      to: [{ type: 'category' }],
      description: 'Which category does this project belong to (e.g. Residential, Commercial, Hospitality)?',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'eyebrow',
      title: 'Eyebrow Tag',
      type: 'string',
      description: 'e.g. "Residential · Private Home" or "Architecture · Exterior"',
    },
    {
      name: 'location',
      title: 'Location',
      type: 'string',
      description: 'e.g. "Tokha, Kathmandu" or "Bharatpur, Chitwan"',
    },
    {
      name: 'intro_heading',
      title: 'Intro Heading (Showcase)',
      type: 'string',
      description: 'e.g. "A REFINED CHITWAN RESIDENCE"',
    },
    {
      name: 'intro_text',
      title: 'Intro Description',
      type: 'text',
      description: 'A brief 2-3 sentence overview of this project.',
    },
    {
      name: 'thumbnail',
      title: 'Thumbnail Image (For Category Grid)',
      type: 'image',
      description: 'This is the cover image shown on the main listing page before opening the project.',
      options: {
        hotspot: true,
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'galleryImages',
      title: 'Gallery Photos',
      description: 'Add multiple photos for this project.',
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
              title: 'Alternative Text',
              description: 'Important for SEO (e.g. "Hotel Lobby View").',
            },
          ],
        },
      ],
    },
    {
      name: 'description',
      title: 'Project Description',
      type: 'text',
    },
  ],
}
