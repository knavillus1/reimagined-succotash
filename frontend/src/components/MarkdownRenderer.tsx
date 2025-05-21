import React, { Component, ErrorInfo } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark.css';

type Props = { markdown: string };

class ErrorBoundary extends Component<{ children: React.ReactNode }, { hasError: boolean }> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(_: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught in MarkdownRenderer:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <p>Something went wrong while rendering the markdown.</p>;
    }

    return this.props.children;
  }
}

// Temporarily remove remark-gfm for testing
const remarkPlugins = [];
const rehypePlugins = [rehypeHighlight];

export default function MarkdownRenderer({ markdown }: Props) {
  return (
    <ErrorBoundary>
      <article className="prose prose-slate dark:prose-invert max-w-none">
        <ReactMarkdown
          children={markdown}
          remarkPlugins={remarkPlugins}
          rehypePlugins={rehypePlugins}
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
    </ErrorBoundary>
  );
}
