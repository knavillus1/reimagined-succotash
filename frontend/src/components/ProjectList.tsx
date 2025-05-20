import { useEffect, useState } from 'react'

export interface Project {
  id: string
  title: string
  image?: string
  repo_url: string
  description: string
  demo_url: string
}

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000' : ''

export default function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    fetch(`${baseUrl}/api/projects`)
      .then((res) => res.json())
      .then((data) => setProjects(data))
      .catch(() => setProjects([]))
  }, [])

  return (
    <div className="overflow-x-auto whitespace-nowrap space-x-4 flex py-4">
      {projects.map((p) => (
        <div key={p.id} className="inline-block w-64 bg-white shadow rounded p-4">
          <h3 className="text-lg font-semibold mb-2">{p.title}</h3>
          <p className="text-sm mb-2">{p.description.slice(0, 80)}...</p>
          <a className="text-blue-500" href={`/project/${p.id}`}>View Project</a>
        </div>
      ))}
    </div>
  )
}
