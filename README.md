# Multidomain Article Discovery

AI-powered platform for semantic search and article recommendations across multiple scientific domains.

## Features

- Fetches articles from arXiv and PubMed
- Stores metadata and embeddings in PostgreSQL + pgvector
- Semantic search using BGE-M3
- Reranking using BGE reranker
- Interest-based article recommendations
- FastAPI backend
- Scheduled article ingestion

## Tech Stack

Python, FastAPI, PostgreSQL, pgvector, SQLAlchemy, Sentence Transformers, BGE-M3

## Current Status

Backend and recommendation system are implemented. Frontend and cloud deployment are in progress.