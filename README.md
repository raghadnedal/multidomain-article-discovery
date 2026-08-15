# Multidomain Article Discovery

AI-powered platform for semantic scientific article discovery and personalized recommendations across multiple domains.

## Features

- Semantic search using BGE-M3 embeddings
- Cross-encoder reranking
- Personalized article recommendations
- PostgreSQL + pgvector vector search
- arXiv and PubMed ingestion
- FastAPI backend
- React + TypeScript frontend
- Dockerized backend
- Scheduled ingestion pipeline

## Architecture

arXiv / PubMed
→ ingestion
→ normalization + deduplication
→ embeddings
→ PostgreSQL + pgvector
→ semantic retrieval
→ reranking
→ FastAPI
→ React frontend

## Tech Stack

Backend:
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector

AI:
- BGE-M3
- BGE reranker
- Sentence Transformers
- PyTorch

Frontend:
- React
- TypeScript
- Vite

Infrastructure:
- Docker

## Current Status

MVP implementation completed locally.

Cloud deployment and scheduled ingestion are in progress.