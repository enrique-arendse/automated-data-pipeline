
import logging
from pathlib import Path

from extract import extract_posts
from transform import transform_posts
from load import load_posts


# Create the logs directory if it does not exist.
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

# Send log messages to both the terminal and a log file.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        ),
    ],
    force=True,
)

logger = logging.getLogger(__name__)


def run_pipeline():
    """Execute the complete data pipeline."""

    logger.info("Pipeline started")

    try:
        raw_posts = extract_posts()
        logger.info("Extracted %s records", len(raw_posts))

        valid_posts, rejected_posts = transform_posts(raw_posts)

        logger.info("Valid records: %s", len(valid_posts))
        logger.info("Rejected records: %s", len(rejected_posts))

        if rejected_posts:
            logger.warning("Some records failed validation.")

            for rejected in rejected_posts[:5]:
                logger.warning(
                    "Rejected record: %s",
                    rejected["reason"],
                )

        loaded_count = load_posts(valid_posts)

        logger.info(
            "Loaded %s records into PostgreSQL",
            loaded_count,
        )

        logger.info("Pipeline finished successfully")

        return {
            "extracted": len(raw_posts),
            "valid": len(valid_posts),
            "rejected": len(rejected_posts),
            "loaded": loaded_count,
        }

    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()
