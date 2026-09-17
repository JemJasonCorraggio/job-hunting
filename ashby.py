import requests
import json
import re
import time


def fetch_jobs(url):
    response = requests.get(url)
    response.raise_for_status()

    return response.text


def fetch_job(job_id, organization):
    url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting"

    query = """
    query ApiJobPosting(
        $organizationHostedJobsPageName: String!
        $jobPostingId: String!
    ) {
        jobPosting(
            organizationHostedJobsPageName: $organizationHostedJobsPageName
            jobPostingId: $jobPostingId
        ) {
            id
            title
            locationName
            workplaceType
            descriptionHtml
        }
    }
    """

    response = requests.post(
        url,
        json={
            "query": query,
            "variables": {
                "organizationHostedJobsPageName": organization,
                "jobPostingId": job_id,
            },
        },
    )

    response.raise_for_status()

    return response.json()["data"]["jobPosting"]

def fetch_selected_jobs(postings, organization):
    jobs = []

    for i, posting in enumerate(postings):
        print(f"Fetching {i + 1}/{len(postings)}: {posting['title']}")

        job = fetch_job(posting["id"], organization)
        jobs.append(job)

        time.sleep(1)

    return jobs