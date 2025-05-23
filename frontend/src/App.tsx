import LandingPage from './pages/LandingPage'
import MainLayout from './layouts/MainLayout'
import ProjectDetailPage from './pages/ProjectDetailPage'
import { Routes, Route, useParams } from 'react-router-dom'

function ProjectDetailWrapper() {
  const { projectId } = useParams()
  return <ProjectDetailPage projectId={projectId || ''} />
}

export default function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/project/:projectId" element={<ProjectDetailWrapper />} />
      </Routes>
    </MainLayout>
  )
}
