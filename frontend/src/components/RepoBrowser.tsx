import { useEffect, useState, useRef } from 'react'
import git from 'isomorphic-git'
import http from 'isomorphic-git/http/web'
import LightningFS from '@isomorphic-git/lightning-fs'
import { marked } from 'marked'

interface Entry {
  name: string
  path: string
  isDir: boolean
}

export default function RepoBrowser({ repoUrl }: { repoUrl: string }) {
  const fsRef = useRef<LightningFS | null>(null)
  const [entries, setEntries] = useState<Entry[]>([])
  const [currentPath, setCurrentPath] = useState('/')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)

  const dir = '/repo'

  useEffect(() => {
    async function cloneRepo() {
      const fs = new LightningFS('repo-fs')
      fsRef.current = fs
      const pfs = fs.promises
      try {
        await pfs.mkdir(dir)
      } catch (_) {}

      await git.clone({
        fs: pfs,
        http,
        dir,
        url: repoUrl,
        ref: 'main',
        singleBranch: true,
        depth: 1,
        corsProxy: 'https://cors.isomorphic-git.org',
      })

      setLoading(false)
      openDir('/')
    }

    cloneRepo().catch((err) => console.error(err))
  }, [repoUrl])

  async function openDir(path: string) {
    if (!fsRef.current) return
    const pfs = fsRef.current.promises
    const names = await pfs.readdir(dir + path)
    const ents: Entry[] = []
    for (const name of names) {
      const stat = await pfs.stat(`${dir}${path}/${name}`)
      ents.push({ name, path: `${path}/${name}`, isDir: stat.isDirectory() })
    }
    setEntries(ents)
    setCurrentPath(path)
    setContent('')
  }

  async function openFile(path: string) {
    if (!fsRef.current) return
    const pfs = fsRef.current.promises
    const data = await pfs.readFile(dir + path, 'utf8')
    if (path.toLowerCase().endsWith('.md')) {
      setContent(marked.parse(data))
    } else {
      setContent(`<pre>${escapeHtml(data)}</pre>`)
    }
  }

  function escapeHtml(str: string) {
    return str.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c] || c))
  }

  const parentPath =
    currentPath === '/' ? null : currentPath.split('/').slice(0, -1).join('/') || '/'

  if (loading) {
    return <p>Loading repository...</p>
  }

  return (
    <div className="flex border rounded h-96 overflow-hidden text-sm">
      <div className="w-1/3 overflow-y-auto border-r p-2">
        {parentPath && (
          <div className="cursor-pointer" onClick={() => openDir(parentPath)}>
            ../
          </div>
        )}
        {entries.map((e) => (
          <div
            key={e.path}
            className="cursor-pointer"
            onClick={() => (e.isDir ? openDir(e.path) : openFile(e.path))}
          >
            {e.isDir ? e.name + '/' : e.name}
          </div>
        ))}
      </div>
      <div className="w-2/3 overflow-y-auto p-2">
        {content ? <div dangerouslySetInnerHTML={{ __html: content }} /> : <p>Select a file</p>}
      </div>
    </div>
  )
}
