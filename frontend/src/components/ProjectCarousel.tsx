import { useEffect, useRef, useState } from 'react'

export interface Project {
  id: string
  title: string
  image?: string
  repo_url: string
  description: string
  demo_url: string
}

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000' : ''

export default function ProjectCarousel() {
  const [projects, setProjects] = useState<Project[]>([])
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetch(`${baseUrl}/api/projects`)
      .then((res) => res.json())
      .then((data) => setProjects(data))
      .catch(() => setProjects([]))
  }, [])

  const scroll = (offset: number) => {
    containerRef.current?.scrollBy({ left: offset, behavior: 'smooth' })
  }

  return (
    <div className="relative">
      <button
        className="absolute left-0 top-1/2 -translate-y-1/2 bg-white bg-opacity-70 rounded-full p-2 shadow"
        onClick={() => scroll(-300)}
      >
        &#8249;
      </button>
      <div
        ref={containerRef}
        className="overflow-x-auto flex space-x-4 py-4 px-8 scroll-smooth"
      >
        {projects.map((p) => {
          const img = p.image ? `${baseUrl}/${p.image}` : undefined
          return (
            <div
              key={p.id}
              onClick={() => (window.location.href = `/project/${p.id}`)}
              className="relative w-64 h-40 flex-shrink-0 rounded shadow cursor-pointer bg-gray-200 bg-cover bg-center"
              style={img ? { backgroundImage: `url(${img})` } : {}}
            >
              <div className="absolute inset-0 bg-black bg-opacity-40 rounded flex items-end p-2">
                <h3 className="text-white text-lg font-semibold">{p.title}</h3>
              </div>
            </div>
          )
        })}
      </div>
      <button
        className="absolute right-0 top-1/2 -translate-y-1/2 bg-white bg-opacity-70 rounded-full p-2 shadow"
        onClick={() => scroll(300)}
      >
        &#8250;
      </button>
    </div>
  )
}
