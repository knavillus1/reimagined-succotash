export interface Project {
  id: string
  title: string
  image?: string
  repo_url: string
  description: string
  demo_url: string
  exclude_paths?: string[]
  effective_exclude_paths?: string[]
}
