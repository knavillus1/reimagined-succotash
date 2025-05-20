import { useEffect, useState } from 'react'
import LandingPage from './pages/LandingPage'
import MainLayout from './layouts/MainLayout'
import ProjectDetailPage from './pages/ProjectDetailPage'

export default function App() {
  const [path, setPath] = useState(window.location.pathname)

  useEffect(() => {
    const onPop = () => setPath(window.location.pathname)
    window.addEventListener('popstate', onPop)
    return () => window.removeEventListener('popstate', onPop)
  }, [])

  let content
  if (path.startsWith('/project/')) {
    const projectId = path.replace('/project/', '')
    content = <ProjectDetailPage projectId={projectId} />
  } else {
    content = <LandingPage />
  }

  return <MainLayout>{content}</MainLayout>
}
