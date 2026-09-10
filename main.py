from ashby import fetch_jobs
from ashby import fetch_selected_jobs
import re
import json


def get_postings(url):
    page = fetch_jobs(url)

    match = re.search(r"window\.__appData\s*=\s*(\{.*?\});", page)

    if not match:
        raise ValueError("Could not find Ashby app data")

    data = json.loads(match.group(1))

    return data["jobBoard"]["jobPostings"]


def is_candidate_job(job):
    title = job["title"].lower()
    location = (job.get("locationName") or "").lower()
    workplace = (job.get("workplaceType") or "").lower()

    # Canada / Canadian location
    canada = (
        "canada" in location
        or "toronto" in location
        or "ottawa" in location
        or "montreal" in location
        or "vancouver" in location
    )

    # Engineering-ish roles
    engineering = any(
        word in title
        for word in [
            "engineer",
            "developer",
            "software",
            "technical",
            "site reliability",
            "data",
        ]
    )

    # Exclude obvious non-target roles
    excluded = any(
        word in title
        for word in [
            "intern",
            "internship",
            "account executive",
            "sales",
            "marketing",
            "recruit",
            "finance",
            "tax",
            "legal",
            "counsel",
            "policy",
            "communications",
            "customer success",
        ]
    )

    return canada and engineering and not excluded


def main():
    url = "https://jobs.ashbyhq.com/cohere"

    postings = get_postings(url)

    candidates = [
        posting for posting in postings
        if is_candidate_job(posting)
    ]

    print(f"Found {len(postings)} total jobs")
    print(f"Found {len(candidates)} candidate jobs")
    print()

    jobs = fetch_selected_jobs(candidates)

    print()
    print(f"Fetched {len(jobs)} full job descriptions")


if __name__ == "__main__":
    main()