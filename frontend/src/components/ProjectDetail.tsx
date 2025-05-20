import { Project } from '../types'
import { API_BASE_URL } from '../utils/api'
import RepoBrowser from './RepoBrowser'

export default function ProjectDetail({ project }: { project: Project }) {
  const imageUrl = project.image ? `${API_BASE_URL}/${project.image}` : undefined

  return (
    <>
    <article className="bg-white shadow rounded overflow-hidden">
      {imageUrl && (
        <div
          className="h-48 md:h-64 bg-cover bg-center"
          style={{ backgroundImage: `url(${imageUrl})` }}
        />
      )}
      <div className="p-4">
        <h1 className="text-3xl font-bold mb-4">{project.title}</h1>
        <p className="mb-4">{project.description}</p>
        <div className="space-x-4">
          <a
            className="text-blue-600 underline"
            href={project.demo_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Live Demo
          </a>
          <a
            className="text-blue-600 underline"
            href={project.repo_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub Repo
          </a>
        </div>
      </div>
    </article>
    <div className="mt-4">
      <RepoBrowser repoUrl={project.repo_url} />
    </div>
    </>
  )
}
