import { ParticleHero } from "@/components/ui/particle-hero";

export default function Home() {
  return (
    <main>
      <ParticleHero
        name="[Your Name]"
        title="Founder & CEO — Nava AI"
        tagline="Building the future with Artificial Intelligence"
        imageSrc="/founder.jpg"
        services={[
          "AI Automation",
          "AI Counselling",
          "Agentic AI",
          "AI Integration",
          "Custom Chatbot Building",
        ]}
      />
    </main>
  );
}
