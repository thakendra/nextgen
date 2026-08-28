import {defineCliConfig} from 'sanity/cli'

export default defineCliConfig({
  api: {
    projectId: 'gpyk0ky0',
    dataset: 'production'
  },
  studioHost: 'nextgen-interiors',
  deployment: {
    appId: 'c9eplzj0p9sq61ighv3nync6',
    /**
     * Enable auto-updates for studios.
     * Learn more at https://www.sanity.io/docs/studio/latest-version-of-sanity#k47faf43faf56
     */
    autoUpdates: true,
  },
})
