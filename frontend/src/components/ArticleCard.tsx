import type { Article } from '../types/article'

type ArticleCardProps = { article: Article }

function ArticleCard({ article }: ArticleCardProps) {
  const relevance = Math.max(0, Math.min(100, Math.round(article.score * 100)))

  return (
    <article className="article-card">
      <div className="card-meta"><span>Research article</span><span className="score"><i><span style={{ width: `${relevance}%` }} /></i>{article.score.toFixed(3)} relevance</span></div>
      <h3>{article.title}</h3>
      <p className="abstract">{article.abstract}</p>
      <a href={article.url} target="_blank" rel="noreferrer">Read full article <span aria-hidden="true">↗</span></a>
    </article>
  )
}

export default ArticleCard
