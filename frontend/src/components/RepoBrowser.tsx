import { useEffect, useState, useRef, type ReactNode, useMemo } from 'react'
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

export default function RepoBrowser({
  repoUrl,
  effectiveExcludePaths,
}: {
  repoUrl: string
  effectiveExcludePaths?: string[]
}) {
  const fsRef = useRef<LightningFS | null>(null)
  const [entries, setEntries] = useState<Entry[]>([])
  const [currentPath, setCurrentPath] = useState('/')
  const [content, setContent] = useState<ReactNode | string>('')
  const [loading, setLoading] = useState(true)
  const [selectedFile, setSelectedFile] = useState<string | null>(null)

  const allExcludes = useMemo(
    () => (effectiveExcludePaths || []).map((p) => p.replace(/^\/+/g, '')),
    [effectiveExcludePaths]
  )

  function isExcluded(path: string) {
    const normalized = path.replace(/^\/+/g, '')
    return allExcludes.some(
      (ex) => normalized === ex || normalized.startsWith(`${ex}/`)
    )
  }

  const dir = '/repo'

  useEffect(() => {
    async function cloneRepo() {
      // Use a unique FS name per repoUrl to avoid cached conflicts
      const fsName = `repo-fs-${btoa(repoUrl)}`
      const fs = new LightningFS(fsName)
      fsRef.current = fs
      const pfs = fs.promises
      // Wipe the repo directory if it exists
      try {
        await pfs.rmdir(dir, { recursive: true })
      } catch (_) {}
      try {
        await pfs.mkdir(dir)
      } catch (_) {}

      // Remove .git if it exists to avoid conflicts
      try {
        await pfs.rmdir(`${dir}/.git`, { recursive: true })
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
      await openDir('/')

      // Automatically open README if present
      const readmeNames = ['README.md', 'readme.md', 'README', 'readme']
      for (const name of readmeNames) {
        try {
          await pfs.stat(`${dir}/${name}`)
          await openFile(`/${name}`)
          break
        } catch (_) {
          // ignore missing file
        }
      }
    }

    cloneRepo().catch((err) => console.error(err))
  }, [repoUrl])

  async function openDir(path: string) {
    if (!fsRef.current) return
    const pfs = fsRef.current.promises
    const names = await pfs.readdir(dir + path)
    const ents: Entry[] = []
    for (const name of names) {
      const normalized = path.endsWith('/') ? path.slice(0, -1) : path
      const fullPath = `${normalized}/${name}`
      if (isExcluded(fullPath)) continue
      const stat = await pfs.stat(`${dir}${fullPath}`)
      ents.push({ name, path: fullPath, isDir: stat.isDirectory() })
    }
    setEntries(ents)
    setCurrentPath(path)
    setContent('')
    setSelectedFile(null)
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
    setSelectedFile(path)
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
    <div className="flex border-2 border-primary rounded-xl w-full max-w-full md:max-w-screen-lg bg-white">
      <div className="w-1/3 border-r-2 border-primary p-4 bg-light-bg text-sm">
        {parentPath && (
          <div className="cursor-pointer px-2 py-1 rounded hover:bg-primary hover:text-white transition" onClick={() => openDir(parentPath)}>
            ../
          </div>
        )}
        {entries.map((e) => (
          <div
            key={e.path}
            className={`cursor-pointer px-2 py-1 rounded transition ${
              selectedFile === e.path
                ? 'bg-secondary text-white'
                : 'hover:bg-primary hover:text-white'
            }`}
            onClick={() => (e.isDir ? openDir(e.path) : openFile(e.path))}
          >
            {e.isDir ? e.name + '/' : e.name}
          </div>
        ))}
      </div>
      <div className="w-2/3 overflow-x-auto p-6 bg-light-bg font-mono text-gray-800 text-xs">
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
