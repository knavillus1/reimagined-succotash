import ProjectCarousel from '../components/ProjectCarousel'

export default function LandingPage() {
  return (
    <section className="max-w-screen-lg mx-auto bg-white rounded-xl shadow-lg p-8">
      <h1 className="text-4xl font-bold text-dark-accent mb-6">My Portfolio</h1>
      <ProjectCarousel />
    </section>
  )
}
