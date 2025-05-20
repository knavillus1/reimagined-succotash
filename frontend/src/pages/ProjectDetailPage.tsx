import { useEffect, useState } from 'react'
import { debugLog } from '../utils/logger'

export interface Project {
  id: string
  title: string
  image?: string
  repo_url: string
  description: string
  demo_url: string
}

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000' : ''

export default function ProjectDetailPage({ projectId }: { projectId: string }) {
  const [project, setProject] = useState<Project | null>(null)

  useEffect(() => {
    debugLog('Fetching project', projectId)
    fetch(`${baseUrl}/api/projects/${projectId}`)
      .then((res) => res.json())
      .then((data) => setProject(data))
      .catch((err) => debugLog('Failed to load project', err))
  }, [projectId])

  if (!project) {
    return <p>Loading...</p>
  }

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">{project.title}</h1>
      <p className="mb-4">{project.description}</p>
      <p className="mb-2">
        <a className="text-blue-500" href={project.repo_url}>
          GitHub Repo
        </a>
      </p>
      <p>
        <a className="text-blue-500" href={project.demo_url}>
          Live Demo
        </a>
      </p>
    </div>
  )
}
