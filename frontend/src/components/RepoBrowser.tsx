import { useEffect, useState, useRef, type ReactNode } from 'react'
import git from 'isomorphic-git'
import http from 'isomorphic-git/http/web'
import LightningFS from '@isomorphic-git/lightning-fs'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import MarkdownRenderer from './MarkdownRenderer'

interface Entry {
  name: string
  path: string
  isDir: boolean
}

export default function RepoBrowser({ repoUrl }: { repoUrl: string }) {
  const fsRef = useRef<LightningFS | null>(null)
  const [entries, setEntries] = useState<Entry[]>([])
  const [currentPath, setCurrentPath] = useState('/')
  const [content, setContent] = useState<ReactNode | string>('')
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
    const lower = path.toLowerCase()
    if (lower.endsWith('.md')) {
      setContent(<MarkdownRenderer markdown={data} />)
    } else if (lower.endsWith('.json')) {
      try {
        const obj = JSON.parse(data)
        setContent(wrapCode(JSON.stringify(obj, null, 2), 'json'))
      } catch {
        setContent(wrapCode(data, 'json'))
      }
    } else {
      setContent(wrapCode(data))
    }
  }

  function wrapCode(code: string, language?: string) {
    const highlighted = language
      ? hljs.highlight(code, { language }).value
      : hljs.highlightAuto(code).value
    const lines = highlighted.split('\n')
    const numbered = lines
      .map(
        (line, i) =>
          `<span class="block"><span class="text-gray-500 select-none mr-2">${
            i + 1
          }</span>${line}</span>`
      )
      .join('')
    return `<pre class="hljs">${numbered}</pre>`
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
        {content ? (
          typeof content === 'string' ? (
            <div dangerouslySetInnerHTML={{ __html: content }} />
          ) : (
            content
          )
        ) : (
          <p>Select a file</p>
        )}
      </div>
    </div>
  )
}
