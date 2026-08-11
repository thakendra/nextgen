import { getCliClient } from 'sanity/cli'

async function checkSanity() {
  const client = getCliClient({ apiVersion: '2023-01-01' })
  const docs = await client.fetch(`*[
    title match "*Campus Block*" ||
    title match "*Reading Lounge*" ||
    title match "*Training Studio*" ||
    title match "*Sankhu Hillside*" ||
    title match "*Lemon Tree Retreat*" ||
    title match "*Navya Club*" ||
    title match "*Sankhu Wellness*" ||
    title match "*Wellness Reception*" ||
    title match "*Consultation Suite*" ||
    title match "*Clinic Foyer*" ||
    title match "*Lemon Tree Cafe*"
  ]`)
  console.log(`Found ${docs.length} matching documents in Sanity.`)
  for (const doc of docs) {
    console.log(`Deleting ${doc._id} (${doc.title})...`)
    await client.delete(doc._id)
  }
}

checkSanity().catch(console.error)
