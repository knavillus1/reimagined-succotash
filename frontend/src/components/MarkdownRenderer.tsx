import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark.css';

type Props = { markdown: string };

export default function MarkdownRenderer({ markdown }: Props) {
  return (
    <article className="prose prose-slate dark:prose-invert max-w-none">
      <ReactMarkdown
        children={markdown}
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          a: ({ node, ...props }) => (
            <a {...props} className="text-blue-600 underline hover:text-blue-800" />
          ),
          img: ({ node, ...props }) => (
            <img {...props} className="rounded-lg shadow mx-auto" loading="lazy" />
          ),
        }}
      />
    </article>
  );
}
