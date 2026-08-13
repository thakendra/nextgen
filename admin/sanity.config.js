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
            // Its own upload / update area, same fields and same flow as any
            // other project. "Create new" here pre-fills the DPR category, and
            // these documents render on dpr-landscaping.html only.
            S.listItem()
              .title('🌿 DPR & Landscaping Projects')
              .child(
                S.documentTypeList('project')
                  .title('DPR & Landscaping Projects')
                  .filter('_type == "project" && (mainCategory == "dpr-landscaping" || subCategory == "dpr-landscaping")')
                  .initialValueTemplates([S.initialValueTemplateItem('project-dpr')])
              ),
            S.listItem()
              .title('🚧 Ongoing Projects (Running)')
              .child(
                S.documentList()
                  .title('Ongoing / Running Projects')
                  .filter('_type == "project" && (mainCategory == "ongoing-projects" || projectStatus == "running" || featuredOnHome == "running")')
              ),
            S.listItem()
              .title('🏛️ Architecture Projects')
              .child(
                S.documentList()
                  .title('Architecture Projects')
                  .filter('_type == "project" && mainCategory == "architecture"')
              ),
            S.listItem()
              .title('🛋️ Interior Design Projects')
              .child(
                S.documentList()
                  .title('Interior Design Projects')
                  .filter('_type == "project" && mainCategory == "interiors"')
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
