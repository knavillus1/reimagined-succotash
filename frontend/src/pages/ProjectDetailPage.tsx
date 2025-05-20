import { useEffect, useState } from 'react'
import { debugLog } from '../utils/logger'
import { Project } from '../types'
import { API_BASE_URL } from '../utils/api'
import ProjectDetail from '../components/ProjectDetail'

export default function ProjectDetailPage({ projectId }: { projectId: string }) {
  const [project, setProject] = useState<Project | null>(null)

  useEffect(() => {
    debugLog('Fetching project', projectId)
    fetch(`${API_BASE_URL}/api/projects/${projectId}`)
      .then((res) => res.json())
      .then((data) => setProject(data))
      .catch((err) => debugLog('Failed to load project', err))
  }, [projectId])

  if (!project) {
    return <p>Loading...</p>
  }

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <ProjectDetail project={project} />
    </div>
  )
}
