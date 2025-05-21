import { Project } from '../types'
import { API_BASE_URL } from '../utils/api'
import RepoBrowser from './RepoBrowser'

export default function ProjectDetail({ project }: { project: Project }) {
  const imageUrl = project.image ? `${API_BASE_URL}/${project.image}` : undefined

  return (
    <>
    <article className="bg-white rounded-xl shadow-lg overflow-hidden">
      {imageUrl && (
        <div
          className="h-48 md:h-64 bg-cover bg-center"
          style={{ backgroundImage: `url(${imageUrl})` }}
        />
      )}
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-4 text-dark-accent">{project.title}</h1>
        <p className="mb-4 text-gray-700">{project.description}</p>
        <div className="space-x-4">
          <a
            className="text-primary hover:text-secondary underline"
            href={project.demo_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Live Demo
          </a>
        </div>
      </div>
    </article>
    <div className="mt-6 w-full">
      <RepoBrowser repoUrl={project.repo_url} />
    </div>
    </>
  )
}
