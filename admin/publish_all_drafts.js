import { getCliClient } from 'sanity/cli'

async function publishDrafts() {
  const client = getCliClient({ apiVersion: '2023-01-01' })
  
  const drafts = await client.fetch(`*[_id in path("drafts.**")]`)
  console.log(`Found ${drafts.length} drafts in Sanity dataset.`)
  
  for (const draft of drafts) {
    const publishedId = draft._id.replace(/^drafts\./, '')
    const { _id, _rev, _createdAt, _updatedAt, ...doc } = draft
    
    console.log(`Publishing: ${draft.title || publishedId}...`)
    
    const transaction = client.transaction()
    transaction.createOrReplace({
      ...doc,
      _id: publishedId,
    })
    transaction.delete(draft._id)
    await transaction.commit()
  }
  
  console.log('All drafts successfully published!')
}

publishDrafts().catch((err) => {
  console.error('Publish error:', err)
  process.exit(1)
})
