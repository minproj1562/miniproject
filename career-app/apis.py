# apis.py
import os
import requests
from flask import current_app

class APIService:
    @staticmethod
    def get_linkedin_jobs(title):
        url = "https://api.linkedin.com/v2/job-search"
        headers = {"Authorization": f"Bearer {current_app.config['LINKEDIN_API_KEY']}"}
        params = {
            "keywords": title,
            "count": 5,
            "sort": "DATE_POSTED_DESC"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('elements', [])

class ONetAPI:
    BASE_URL = "https://services.onetcenter.org/ws/"
    
    def get_career_details(self, soc_code):
        url = f"{self.BASE_URL}/mnm/careers/{soc_code}/summary"
        response = requests.get(url, auth=(os.getenv('ONET_USER'), os.getenv('ONET_PWD')))
        return response.json()

class PlagiarismChecker:
    @staticmethod
    def verify_content(text):
        response = requests.post(
            "https://api.copyleaks.com/v3/detector",
            json={"text": text},
            headers={"Authorization": f"Bearer {os.getenv('COPYLEAKS_KEY')}"}
        )
        return response.json().get('score', 0)
