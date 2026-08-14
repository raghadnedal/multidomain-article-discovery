import './App.css'
import { useEffect, useState, type FormEvent, type ReactNode } from 'react'
import ArticleCard from './components/ArticleCard'
import type { Article } from './types/article'

function Icon({ children }: { children: ReactNode }) {
  return <span className="icon" aria-hidden="true">{children}</span>
}

function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const savedTheme = localStorage.getItem('article-discovery-theme')
    if (savedTheme === 'light' || savedTheme === 'dark') return savedTheme
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  })
  const [query, setQuery] = useState('')
  const [domain, setDomain] = useState('')
  const [results, setResults] = useState<Article[]>([])
  const [interests, setInterests] = useState('')
  const [recommendations, setRecommendations] = useState<Article[]>([])
  const [searchLoading, setSearchLoading] = useState(false)
  const [recommendLoading, setRecommendLoading] = useState(false)
  const [searchError, setSearchError] = useState('')
  const [recommendError, setRecommendError] = useState('')

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('article-discovery-theme', theme)
  }, [theme])

  async function handleSearch(event?: FormEvent) {
    event?.preventDefault()
    try {
      setSearchLoading(true)
      setSearchError('')
      const params = new URLSearchParams({ query })
      if (domain) params.append('domain', domain)

      const response = await fetch(`http://127.0.0.1:8000/search?${params.toString()}`)
      if (!response.ok) throw new Error('Search request failed')
      setResults(await response.json())
    } catch {
      setSearchError('Something went wrong while searching.')
    } finally {
      setSearchLoading(false)
    }
  }

  async function handleRecommend(event?: FormEvent) {
    event?.preventDefault()
    try {
      setRecommendLoading(true)
      setRecommendError('')
      const interestList = interests.split(',').map((interest) => interest.trim()).filter(Boolean)
      if (interestList.length === 0) {
        setRecommendError('Please enter at least one interest.')
        return
      }

      const response = await fetch('http://127.0.0.1:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ interests: interestList }),
      })
      if (!response.ok) throw new Error('Recommendation request failed')
      setRecommendations(await response.json())
    } catch {
      setRecommendError('Something went wrong while generating recommendations.')
    } finally {
      setRecommendLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="header">
        <a className="brand" href="#top" aria-label="Article Discovery home">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="4"/><ellipse cx="16" cy="16" rx="13" ry="6"/><ellipse cx="16" cy="16" rx="6" ry="13" transform="rotate(42 16 16)"/></svg>
          </span>
          <span><strong>Article Discovery</strong><small>AI Research Platform</small></span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#search">Search</a>
          <a href="#recommendations">Recommendations</a>
          <button
            className="theme-toggle"
            type="button"
            onClick={() => setTheme((current) => current === 'light' ? 'dark' : 'light')}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            <span className="theme-icon" aria-hidden="true">{theme === 'light' ? '☾' : '☀'}</span>
          </button>
          <a href="#search" className="nav-button">Explore articles <span>→</span></a>
        </nav>
      </header>

      <main id="top">
        <section className="hero">
          <div className="eyebrow"><span className="status-dot" /> AI-powered scientific discovery</div>
          <h1>Discover research across<br/><span>multiple domains</span></h1>
          <p>Search, discover, and get AI-powered research recommendations across medicine and artificial intelligence.</p>
          <div className="hero-tags" aria-label="Supported capabilities"><span>Semantic search</span><span>Cross-domain</span><span>AI recommendations</span></div>
        </section>

        <section id="search" className="panel">
          <div className="section-heading">
            <div>
              <span className="kicker">01 · Search</span>
              <h2>Article Search</h2>
              <p>Find relevant work using natural language and refine by domain.</p>
            </div>
            <Icon>⌕</Icon>
          </div>

          <form className="search-form" onSubmit={handleSearch}>
            <label className="field search-field">
              <span>Search query</span>
              <span className="input-wrap"><b aria-hidden="true">⌕</b><input type="search" placeholder="Try ‘machine learning in clinical diagnostics’" value={query} onChange={(event) => setQuery(event.target.value)} /></span>
            </label>
            <label className="field domain-field">
              <span>Domain</span>
              <select value={domain} onChange={(event) => setDomain(event.target.value)}>
                <option value="">All domains</option>
                <option value="medicine">Medicine</option>
                <option value="artificial_intelligence">Artificial Intelligence</option>
              </select>
            </label>
            <button className="primary-button" type="submit" disabled={searchLoading}>
              {searchLoading ? <span className="spinner" /> : <span aria-hidden="true">✦</span>}
              {searchLoading ? 'Searching…' : 'Search research'}
            </button>
          </form>

          {searchError && <div className="error" role="alert"><span>!</span>{searchError}</div>}

          <div className="results-header">
            <div><h3>Search results</h3><span>{results.length} {results.length === 1 ? 'article' : 'articles'}</span></div>
            {results.length > 0 && <p>Ranked by semantic relevance</p>}
          </div>
          {results.length === 0 ? (
            <div className="empty-state"><span className="empty-illustration" aria-hidden="true">⌕</span><h3>Your research journey starts here</h3><p>Enter a topic above to surface the most relevant articles from our interdisciplinary library.</p></div>
          ) : <div className="results">{results.map((article) => <ArticleCard key={article.external_id} article={article} />)}</div>}
        </section>

        <section id="recommendations" className="panel recommendation-panel">
          <div className="section-heading">
            <div>
              <span className="kicker">02 · Recommendations</span>
              <h2>Recommended for You</h2>
              <p>Enter your interests to discover relevant research.</p>
            </div>
            <Icon>✦</Icon>
          </div>
          <form className="recommend-form" onSubmit={handleRecommend}>
            <label className="field">
              <span>Your interests <em>Separate topics with commas</em></span>
              <span className="input-wrap"><b aria-hidden="true">＋</b><input type="text" placeholder="AI safety, robotics, medical imaging…" value={interests} onChange={(event) => setInterests(event.target.value)} /></span>
            </label>
            <button className="primary-button" type="submit" disabled={recommendLoading}>
              {recommendLoading ? <span className="spinner" /> : <span aria-hidden="true">✦</span>}
              {recommendLoading ? 'Curating…' : 'Curate my reading list'}
            </button>
          </form>
          {recommendError && <div className="error" role="alert"><span>!</span>{recommendError}</div>}
          {recommendations.length === 0 ? (
            <div className="recommend-empty"><span>Thoughtful recommendations begin with the subjects you care about.</span></div>
          ) : <div className="results recommendation-results">{recommendations.map((article) => <ArticleCard key={article.external_id} article={article} />)}</div>}
        </section>
      </main>

      <footer id="about" className="technical-footer">
        <div className="footer-intro"><strong>Article Discovery</strong><p>AI-powered multi-domain scientific research discovery.</p></div>
        <div className="footer-stack"><strong>Built with:</strong><span>FastAPI · PostgreSQL · pgvector · BGE-M3 · React</span></div>
        <div className="footer-stack"><strong>Data sources:</strong><span>arXiv · PubMed</span></div>
        <a href="https://github.com/raghadnedal/multidomain-article-discovery" target="_blank" rel="noreferrer">GitHub ↗</a>
      </footer>
    </div>
  )
}

export default App
