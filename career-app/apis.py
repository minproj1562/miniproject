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
    def __init__(self):
        self.BASE_URL = "https://services.onetcenter.org/ws/"

    def get_career_details(self, soc_code):
        url = f"{self.BASE_URL}mnm/careers/{soc_code}/summary"
        response = requests.get(url, auth=(os.getenv('ONET_USER'), os.getenv('ONET_PWD')))
        print(f"ONet API Status: {response.status_code}")
        print(f"ONet API Response: {response.text}")
        if response.status_code != 200:
            raise Exception(f"ONet API failed with status {response.status_code}")
        data = response.json()
        return {
            'title': data.get('title', 'N/A'),
            'wages': {'median': data.get('wages', {}).get('national', {}).get('median', 'N/A')},
            'outlook': {'growth_rate': data.get('bright_outlook', {}).get('growth_rate', 'N/A')}
        }

class PlagiarismChecker:
    @staticmethod
    def verify_content(text):
        response = requests.post(
            "https://api.copyleaks.com/v3/detector",
            json={"text": text},
            headers={"Authorization": f"Bearer {os.getenv('COPYLEAKS_KEY')}"}
        )
        return response.json().get('score', 0)
