from celery import Celery
from app import create_app

celery = Celery(__name__, broker=os.getenv('REDIS_URL'))
celery.conf.update(include=['apis'])

@celery.task
def update_job_market_data():
    with create_app().app_context():
        # Update job market data nightly
        careers = CAREER_MAPPING.keys()
        for career in careers:
            data = APIService.get_linkedin_jobs(career)
            # Store in database