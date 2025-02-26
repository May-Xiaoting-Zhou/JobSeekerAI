from typing import List, Dict, Optional
import requests
import json
import os
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JobSearchAPI:
    def __init__(self):
        # Initialize API keys from environment variables
        self.jsearch_key = os.getenv("JSEARCH_API_KEY")
        self.jooble_key = os.getenv("JOOBLE_API_KEY")
        self.adzuna_id = os.getenv("ADZUNA_APP_ID")
        self.adzuna_key = os.getenv("ADZUNA_API_KEY")

        # Define patterns for extracting job information
        self.patterns = {
            'title': r'(job|position|role|looking for|hiring)\s+(?:a\s+)?([^,\.]+)',
            'location': r'(in|at|near|around)\s+([^,\.]+)',
            'salary': r'(\$[\d,]+(?:\s*-\s*\$[\d,]+)?|\d+k(?:\s*-\s*\d+k)?)',
            'experience': r'(\d+(?:\+|\s*-\s*\d+)?\s*(?:years?|yrs?)(?:\s+of)?\s+experience)',
            'type': r'(full[- ]time|part[- ]time|contract|permanent|remote|hybrid)'
        }

    async def search_jsearch(self, query: str, location: str = "Remote") -> List[Dict]:
        """Search jobs using JSearch API"""
        try:
            url = "https://jsearch.p.rapidapi.com/search"
            querystring = {"query": f"{query}, {location}", "num_pages": "1"}
            headers = {
                "X-RapidAPI-Key": self.jsearch_key,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
            
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            # Standardize the response format
            return [{
                "title": job["job_title"],
                "company": job["employer_name"],
                "location": job["job_city"],
                "description": job.get("job_description", ""),
                "url": job.get("job_apply_link", ""),
                "salary": job.get("job_salary", "Not specified"),
                "source": "JSearch",
                "posted_date": job.get("job_posted_at_datetime", ""),
                "job_type": job.get("job_employment_type", "Not specified")
            } for job in data.get("data", [])]
            
        except Exception as e:
            print(f"JSearch API error: {e}")
            return []

    async def search_remotive(self, query: str) -> List[Dict]:
        """Search remote jobs using Remotive API"""
        try:
            url = f"https://remotive.io/api/remote-jobs?search={query}&category=software-dev"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            return [{
                "title": job["title"],
                "company": job["company_name"],
                "location": job["candidate_required_location"],
                "description": job.get("description", ""),
                "url": job.get("url", ""),
                "salary": "Not specified",
                "source": "Remotive",
                "posted_date": job.get("publication_date", ""),
                "job_type": "Remote"
            } for job in data.get("jobs", [])]
            
        except Exception as e:
            print(f"Remotive API error: {e}")
            return []

    def extract_job_params(self, conversation_history: List[Dict]) -> Dict:
        """Extract job search parameters from conversation history"""
        # Combine all user messages
        full_text = ' '.join([
            msg['text'].lower() 
            for msg in conversation_history 
            if msg['sender'] == 'user'
        ])
        
        params = {
            'title': None,
            'location': 'Remote',  # default
            'salary': None,
            'experience': None,
            'type': None
        }
        
        # Extract parameters using regex patterns
        for param, pattern in self.patterns.items():
            match = re.search(pattern, full_text)
            if match:
                params[param] = match.group(2) if param == 'title' else match.group(1)
        
        return params

    async def search_all(self, query: str, location: str = "Remote", params: Dict = None) -> Dict:
        """Enhanced search with additional parameters"""
        try:
            # Build search query incorporating all parameters
            search_query = query
            if params:
                if params.get('title'):
                    search_query = f"{params['title']} {search_query}"
                if params.get('type'):
                    search_query = f"{search_query} {params['type']}"
                if params.get('experience'):
                    search_query = f"{search_query} {params['experience']}"
                if params.get('salary'):
                    search_query = f"{search_query} {params['salary']}"
                
            # Use provided location or extracted location
            search_location = params.get('location', location) if params else location
            
            # Get results from different APIs
            jsearch_results = await self.search_jsearch(search_query, search_location)
            remotive_results = await self.search_remotive(search_query)
            
            # Combine and filter results
            all_jobs = jsearch_results + remotive_results
            
            # Filter results if we have specific parameters
            if params:
                filtered_jobs = []
                for job in all_jobs:
                    matches = True
                    if params.get('salary'):
                        if not self._matches_salary(job['salary'], params['salary']):
                            matches = False
                    if params.get('type'):
                        if params['type'].lower() not in job['job_type'].lower():
                            matches = False
                    if matches:
                        filtered_jobs.append(job)
                all_jobs = filtered_jobs
            
            # Sort by posted date
            all_jobs.sort(
                key=lambda x: datetime.fromisoformat(x["posted_date"].replace('Z', '+00:00'))
                if x["posted_date"]
                else datetime.min,
                reverse=True
            )
            
            return {
                "status": "success",
                "total_jobs": len(all_jobs),
                "jobs": all_jobs,
                "search_params": params,
                "metadata": {
                    "query": search_query,
                    "location": search_location,
                    "sources": ["JSearch", "Remotive"],
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "jobs": [],
                "search_params": params,
                "metadata": {
                    "query": query,
                    "location": location,
                    "timestamp": datetime.now().isoformat()
                }
            }

    def _matches_salary(self, job_salary: str, target_salary: str) -> bool:
        """Helper method to match salary ranges"""
        try:
            # Extract numbers from salary strings
            job_nums = re.findall(r'\d+', job_salary)
            target_nums = re.findall(r'\d+', target_salary)
            
            if not job_nums or not target_nums:
                return True  # If we can't parse either salary, don't filter it out
                
            job_min = min(int(n) for n in job_nums)
            job_max = max(int(n) for n in job_nums)
            target_min = min(int(n) for n in target_nums)
            target_max = max(int(n) for n in target_nums)
            
            # Check if salary ranges overlap
            return not (job_max < target_min or job_min > target_max)
        except:
            return True  # If there's any error in parsing, don't filter out the job

    def format_job_for_chat(self, job: Dict) -> str:
        """Format a job listing for chat display"""
        return f"""
🔍 {job['title']}
🏢 {job['company']}
📍 {job['location']}
💰 {job['salary']}
🔗 {job['url']}
📅 Posted: {job['posted_date']}
🏷️ Type: {job['job_type']}
""" 