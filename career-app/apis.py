import os
import requests
from requests.auth import HTTPBasicAuth

class ONetAPI:
    def __init__(self):
        # Load O*NET credentials from environment variables
        self.user = os.getenv('ONET_USER')
        self.pwd = os.getenv('ONET_PWD')
        self.base_url = "https://services.onetcenter.org/ws/"

        # Validate that credentials are available
        if not self.user or not self.pwd:
            raise ValueError("O*NET API credentials (ONET_USER and ONET_PWD) must be set in environment variables.")

    def _make_request(self, endpoint):
        """
        Helper method to make an API request to O*NET with authentication.
        
        Args:
            endpoint (str): The API endpoint to query (e.g., "mnm/careers/15-1132.00").
            
        Returns:
            dict: The JSON response from the API, or None if the request fails.
        """
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                auth=HTTPBasicAuth(self.user, self.pwd),
                headers={'Accept': 'application/json'}
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to O*NET API: {e}")
            return None

    def get_career_details(self, soc_code):
        """
        Fetch career details for a given SOC code from O*NET.
        
        Args:
            soc_code (str): The Standard Occupational Classification (SOC) code (e.g., "15-1132.00").
            
        Returns:
            dict: A dictionary containing career details such as job title, wages, and job outlook.
                  Returns a fallback dictionary with 'N/A' values if the request fails.
        """
        # Construct the endpoint for career details
        endpoint = f"mnm/careers/{soc_code}"

        # Make the API request
        data = self._make_request(endpoint)
        if not data:
            # Return fallback data if the request fails
            return {
                "title": "N/A",
                "wages": {"median": "N/A"},
                "outlook": {"growth_rate": "N/A"}
            }

        # Extract relevant information from the response
        career_data = {
            "title": data.get("career", {}).get("title", "N/A"),
            "wages": {
                "median": data.get("career", {}).get("wages", {}).get("median", "N/A")
            },
            "outlook": {
                "growth_rate": data.get("career", {}).get("outlook", {}).get("growth_rate", "N/A")
            }
        }

        return career_data

    def get_occupation_list(self, keyword=None, start=1, end=10):
        """
        Fetch a list of occupations from O*NET, optionally filtered by a keyword.
        
        Args:
            keyword (str, optional): A keyword to filter occupations (e.g., "software").
            start (int): The starting index for pagination (default: 1).
            end (int): The ending index for pagination (default: 10).
            
        Returns:
            list: A list of occupations, or an empty list if the request fails.
        """
        # Construct the endpoint for the occupation list
        endpoint = f"online/occupations?start={start}&end={end}"
        if keyword:
            endpoint += f"&keyword={keyword}"

        # Make the API request
        data = self._make_request(endpoint)
        if not data or "occupation" not in data:
            return []

        # Extract the list of occupations
        occupations = data.get("occupation", [])
        return occupations

    def get_skills_for_occupation(self, soc_code):
        """
        Fetch skills associated with a given SOC code.
        
        Args:
            soc_code (str): The SOC code (e.g., "15-1132.00").
            
        Returns:
            list: A list of skills, or an empty list if the request fails.
        """
        # Construct the endpoint for skills
        endpoint = f"online/occupations/{soc_code}/details/skills"

        # Make the API request
        data = self._make_request(endpoint)
        if not data or "element" not in data:
            return []

        # Extract the list of skills
        skills = data.get("element", [])
        return skills

    def get_education_for_occupation(self, soc_code):
        """
        Fetch education requirements for a given SOC code.
        
        Args:
            soc_code (str): The SOC code (e.g., "15-1132.00").
            
        Returns:
            dict: A dictionary of education requirements, or an empty dict if the request fails.
        """
        # Construct the endpoint for education
        endpoint = f"mnm/careers/{soc_code}/education"

        # Make the API request
        data = self._make_request(endpoint)
        if not data:
            return {}

        # Extract education requirements
        education = {
            "typical_level": data.get("typical_level", "N/A"),
            "required_level": data.get("required_level", "N/A")
        }
        return education