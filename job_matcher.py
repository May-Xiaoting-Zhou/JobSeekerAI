import spacy
import datetime

# Load spaCy model for NLP
nlp = spacy.load('en_core_web_sm')

def match_jobs(resume_text, job_listings, top_cities):
    resume_doc = nlp(resume_text)
    matched_jobs = []

    for job in job_listings:
        if job["city"] in top_cities:
            job_doc = nlp(job["description"])
            similarity = resume_doc.similarity(job_doc)
            if similarity > 0.7:
                job['similarity'] = similarity
                job['key_words'] = [token.text for token in resume_doc if token.text in job_doc.text]
                matched_jobs.append(job)

    matched_jobs.sort(key=lambda x: datetime.datetime.strptime(x["date_posted"], "%Y-%m-%d"), reverse=True)
    return matched_jobs

# Example usage
if __name__ == "__main__":
    job_listings = [
        {"title": "Data Scientist", "description": "Experienced in Python, machine learning.", "date_posted": "2025-01-20", "city": "San Francisco"},
        {"title": "Software Engineer", "description": "Proficient in JavaScript and web development.", "date_posted": "2025-01-19", "city": "New York"}
    ]
    resume_text = "Experienced in Python, machine learning, data analysis."
    top_cities = ["San Francisco", "New York"]

    matched_jobs = match_jobs(resume_text, job_listings, top_cities)
    for job in matched_jobs:
        print(f"Title: {job['title']}, City: {job['city']}, Date Posted: {job['date_posted']}, Similarity: {job['similarity']:.2f}")
        print(f"Key Words: {', '.join(job['key_words'])}")
        print()
