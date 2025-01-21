from job_scraper import get_job_listings
from job_matcher import match_jobs

def main():
    print("Welcome to JobSeekerAI: Your Personalized Job Hunt Partner")
    
    # Input user's resume
    resume_text = input("Please enter your resume text: ")

    # Input user's top preferred cities
    top_cities = input("Please enter your top 5 preferred cities (comma-separated): ").split(',')

    # Fetch job listings
    job_listings = get_job_listings()

    # Match jobs based on user's resume and top cities
    matched_jobs = match_jobs(resume_text, job_listings, top_cities)

    # Display matched jobs
    if matched_jobs:
        print("Matched Job Listings:")
        for job in matched_jobs:
            print(f"Title: {job['title']}, City: {job['city']}, Date Posted: {job['date_posted']}, Similarity: {job['similarity']:.2f}")
            print(f"Key Words: {', '.join(job['key_words'])}")
            print()
    else:
        print("No matching job listings found.")

if __name__ == "__main__":
    main()
