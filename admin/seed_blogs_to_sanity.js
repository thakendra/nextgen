import { getCliClient } from 'sanity/cli'
import fs from 'fs'
import path from 'path'

async function seedBlogs() {
  const client = getCliClient({ apiVersion: '2023-01-01' })
  
  const jsonPath = 'C:/Users/LOQ/.gemini/antigravity/brain/a0f7c821-4155-4659-a0bb-a4eeee91a00a/scratch/sanity_seed_blogs.json'
  const blogs = JSON.parse(fs.readFileSync(jsonPath, 'utf8'))
  
  console.log(`Starting migration of ${blogs.length} blogs to Sanity...`)
  
  for (const b of blogs) {
    console.log(`Uploading blog: ${b.title} (${b.slug.current})...`)
    const transaction = client.transaction()
    transaction.createOrReplace(b)
    await transaction.commit()
  }
  
  console.log('All 16 blogs successfully uploaded to Sanity!')
}

seedBlogs().catch((err) => {
  console.error('Migration error:', err)
  process.exit(1)
})
