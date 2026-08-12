from apscheduler.schedulers.blocking import BlockingScheduler
from article_discovery.jobs.ingest_arxiv import run_arxiv_ingestion


def start_scheduler() -> None:
    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_arxiv_ingestion,
        trigger="interval",
        hours=6,
    )

    print("Scheduler started. arXiv ingestion will run every 6 hours.")

    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
