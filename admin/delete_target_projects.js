import { getCliClient } from 'sanity/cli'

async function deleteTargets() {
  const client = getCliClient({ apiVersion: '2023-01-01' })
  const docs = await client.fetch(`*[
    slug.current in ["restro-office", "executive-suites", "breakout-lounge", "chapur-boardroom", "chapur-hotel"] ||
    title match "*Restro Office*" ||
    title match "*Executive Suit*" ||
    title match "*Breakout Lounge*" ||
    title match "*Chapur Boardroom*"
  ]`)
  
  console.log(`Found ${docs.length} target documents to delete in Sanity.`)
  for (const doc of docs) {
    console.log(`Deleting: ${doc._id} (${doc.title})...`)
    await client.delete(doc._id)
  }
  console.log('All target documents deleted from Sanity completely!')
}

deleteTargets().catch(console.error)
