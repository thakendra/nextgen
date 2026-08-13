import {defineConfig} from 'sanity'
import {structureTool} from 'sanity/structure'
import {visionTool} from '@sanity/vision'
import {schemaTypes} from './schemaTypes'

export default defineConfig({
  name: 'default',
  title: 'NextGen Interiors',

  projectId: 'gpyk0ky0',
  dataset: 'production',

  plugins: [
    structureTool({
      structure: (S) =>
        S.list()
          .title('Content')
          .items([
            S.listItem()
              .title('📂 All Projects / Showcase')
              .child(S.documentTypeList('project').title('All Projects')),
            S.listItem()
              .title('🌿 DPR & Landscaping Projects')
              .child(
                S.documentTypeList('project')
                  .title('DPR & Landscaping Projects')
                  .filter('_type == "project" && (mainCategory == "dpr-landscaping" || subCategory == "dpr-landscaping")')
              ),
          ]),
    }),
    visionTool(),
  ],

  schema: {
    types: schemaTypes,
    // Backs the "Create new" button inside the DPR & Landscaping list, so a new
    // document lands in the right category without anyone having to remember to
    // set it. featuredOnHome is pinned to 'no' because DPR work is not part of
    // the Home Page showcase.
    templates: (prev) => [
      ...prev,
      {
        id: 'project-dpr',
        title: '🌿 DPR & Landscaping Project',
        schemaType: 'project',
        value: {
          mainCategory: 'dpr-landscaping',
          subCategory: 'dpr-landscaping',
          featuredOnHome: 'no',
          projectStatus: 'completed',
        },
      },
    ],
  },
})
