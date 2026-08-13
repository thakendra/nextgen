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
  },
})
