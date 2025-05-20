import { useEffect, useState } from 'react'
import { debugLog } from '../utils/logger'
import { Project } from '../types'
import { API_BASE_URL } from '../utils/api'

export default function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    debugLog('Fetching projects from', `${API_BASE_URL}/api/projects`)
    fetch(`${API_BASE_URL}/api/projects`)
      .then((res) => {
        debugLog('Received response', res.status)
        return res.json()
      })
      .then((data) => {
        debugLog('Project data', data)
        setProjects(data)
      })
      .catch((err) => {
        debugLog('Failed to load projects', err)
        setProjects([])
      })
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
