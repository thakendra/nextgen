import { getCliClient } from 'sanity/cli'

async function deleteChapur() {
  const client = getCliClient({ apiVersion: '2023-01-01' })
  const docs = await client.fetch(`*[slug.current == "chapur-hotel" || title match "*Chapur*"]`)
  console.log(`Found ${docs.length} Chapur documents to delete.`)
  for (const doc of docs) {
    console.log(`Deleting ${doc._id} (${doc.title})...`)
    await client.delete(doc._id)
  }
  console.log('Chapur Hotel deleted from Sanity completely!')
}

deleteChapur().catch(console.error)
