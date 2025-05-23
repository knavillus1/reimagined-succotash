import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { debugLog } from '../utils/logger'
import { Project } from '../types'
import { API_BASE_URL } from '../utils/api'

export default function ProjectCarousel() {
  const [projects, setProjects] = useState<Project[]>([])
  const containerRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()

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

  const scroll = (offset: number) => {
    containerRef.current?.scrollBy({ left: offset, behavior: 'smooth' })
  }

  return (
    <div className="relative">
      <button
        className="absolute left-0 top-1/2 -translate-y-1/2 bg-primary text-white rounded-full p-3 shadow-lg hover:bg-secondary transition"
        onClick={() => scroll(-300)}
      >
        &#8249;
      </button>
      <div
        ref={containerRef}
        className="overflow-x-auto flex space-x-6 py-6 px-8 scroll-smooth"
      >
        {projects.map((p) => {
          const img = p.image ? `${API_BASE_URL}/${p.image}` : undefined
          return (
            <div
              key={p.id}
              onClick={() => navigate(`/project/${p.id}`)}
              className="relative w-64 h-40 flex-shrink-0 rounded-xl overflow-hidden shadow-lg cursor-pointer transform hover:scale-105 transition bg-gray-200 bg-cover bg-center"
              style={img ? { backgroundImage: `url(${img})` } : {}}
            >
              <div className="absolute inset-0 bg-dark-accent bg-opacity-50 flex items-end p-3">
                <h3 className="text-white text-lg font-semibold">{p.title}</h3>
              </div>
            </div>
          )
        })}
      </div>
      <button
        className="absolute right-0 top-1/2 -translate-y-1/2 bg-primary text-white rounded-full p-3 shadow-lg hover:bg-secondary transition"
        onClick={() => scroll(300)}
      >
        &#8250;
      </button>
    </div>
  )
}
