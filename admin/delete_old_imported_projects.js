import { getCliClient } from 'sanity/cli'

async function deleteOldImported() {
  const client = getCliClient({ apiVersion: '2023-01-01' })
  const allDocs = await client.fetch(`*[_type == "project"]{_id, title}`)
  const oldDocs = allDocs.filter(d => d._id.startsWith('project-') || d._id.startsWith('drafts.project-'))
  
  console.log(`Found ${oldDocs.length} old imported projects to delete in Sanity.`)
  
  for (const doc of oldDocs) {
    console.log(`Deleting: ${doc._id} (${doc.title})...`)
    await client.delete(doc._id)
  }
  
  console.log('All old imported projects deleted from Sanity successfully!')
}

deleteOldImported().catch(console.error)
