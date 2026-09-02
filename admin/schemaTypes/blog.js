export const blog = {
  name: 'blog',
  title: 'Blog / Article',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Article / Blog Title',
      type: 'string',
      description: 'e.g. "Hotel Interior Design in Nepal" or "Affordable International Style House"',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'slug',
      title: 'Page URL Slug',
      type: 'slug',
      description: 'e.g. "hotel-interior-design-nepal"',
      options: {
        source: 'title',
        maxLength: 96,
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'category',
      title: 'Category',
      type: 'string',
      options: {
        list: [
          { title: 'Interior Design', value: 'Interior Design' },
          { title: 'Architecture', value: 'Architecture' },
          { title: 'Hospitality', value: 'Hospitality' },
          { title: 'Commercial', value: 'Commercial' },
          { title: 'Residential', value: 'Residential' },
          { title: 'Design Guide', value: 'Design Guide' },
          { title: 'Construction', value: 'Construction' },
        ],
      },
      initialValue: 'Interior Design',
    },
    {
      name: 'publishedAt',
      title: 'Published Date',
      type: 'date',
      options: {
        dateFormat: 'YYYY-MM-DD',
      },
      initialValue: () => new Date().toISOString().split('T')[0],
    },
    {
      name: 'readTime',
      title: 'Read Time',
      type: 'string',
      description: 'e.g. "12 min read"',
      initialValue: '10 min read',
    },
    {
      name: 'author',
      title: 'Author',
      type: 'string',
      initialValue: 'NextGen Team',
    },
    {
      name: 'coverImage',
      title: 'Cover / Hero Image',
      type: 'image',
      options: {
        hotspot: true,
      },
    },
    {
      name: 'metaDescription',
      title: 'SEO Meta Description',
      type: 'text',
      rows: 3,
      description: 'Search engine description (120 - 165 characters recommended)',
    },
    {
      name: 'lede',
      title: 'Opening Highlight / Lede Paragraph',
      type: 'text',
      rows: 3,
      description: 'Prominent introductory text displayed at the top of the article',
    },
    {
      name: 'content',
      title: 'Article Content (Text & Headings)',
      type: 'array',
      of: [
        {
          type: 'block',
          styles: [
            { title: 'Normal Paragraph', value: 'normal' },
            { title: 'Heading 2 (Major Section)', value: 'h2' },
            { title: 'Heading 3 (Subsection)', value: 'h3' },
            { title: 'Pullquote / Highlight', value: 'blockquote' },
          ],
          lists: [
            { title: 'Bullet List', value: 'bullet' },
            { title: 'Numbered List', value: 'number' },
          ],
          marks: {
            decorators: [
              { title: 'Bold', value: 'strong' },
              { title: 'Italic', value: 'em' },
            ],
            annotations: [
              {
                name: 'link',
                type: 'object',
                title: 'Link URL',
                fields: [
                  {
                    name: 'href',
                    type: 'url',
                    title: 'URL (Internal link e.g. /hospitality or external https://)',
                    validation: (Rule) =>
                      Rule.uri({
                        allowRelative: true,
                        scheme: ['https', 'http', 'mailto', 'tel'],
                      }),
                  },
                ],
              },
            ],
          },
        },
      ],
      description: 'Write or edit your article text here. You can add Headings (H2/H3), bullet lists, quotes, bold text, and links.',
    },
    {
      name: 'tags',
      title: 'Keywords / Tags',
      type: 'array',
      of: [{ type: 'string' }],
      options: {
        layout: 'tags',
      },
    },
  ],
  preview: {
    select: {
      title: 'title',
      subtitle: 'category',
      media: 'coverImage',
    },
  },
}
