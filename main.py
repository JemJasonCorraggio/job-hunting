from ashby import fetch_jobs
from ashby import fetch_selected_jobs
from agent import evaluate_job
from agent import rank_jobs_by_title
import re
import json
import sys

JOB_BOARDS = {
    "cohere": {
        "company": "Cohere",
        "organization": "cohere",
        "url": "https://jobs.ashbyhq.com/cohere",
        "team_id": "68960387-27ac-4599-81a6-0b61399ef7eb"
    },
}


def get_postings(url):
    page = fetch_jobs(url)

    match = re.search(r"window\.__appData\s*=\s*(\{.*?\});", page)

    if not match:
        raise ValueError("Could not find Ashby app data")

    data = json.loads(match.group(1))

    return data["jobBoard"]["jobPostings"], data["jobBoard"]["teams"]


ENGINEERING_INFRA_TEAM_ID = "68960387-27ac-4599-81a6-0b61399ef7eb"


def is_candidate_job(job, teams, team_id):
    # Find the Engineering & Infra team and its direct children
    engineering_team_ids = {
        team["id"]
        for team in teams
        if (
            team["id"] == team_id
            or team["parentTeamId"] == team_id
        )
    }

    # Check whether Canada is one of the job's locations
    locations = [job.get("locationName", "")]

    locations.extend(
        location["locationName"]
        for location in job.get("secondaryLocations", [])
    )

    locations = [location.lower() for location in locations]

    canada = any(
        "canada" in location
        or "toronto" in location
        or "ottawa" in location
        or "montreal" in location
        or "vancouver" in location
        for location in locations
    )

    # Check whether the job belongs to Engineering & Infra
    engineering = job.get("teamId") in engineering_team_ids

    return canada and engineering


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <job_board>")
        print(f"Available job boards: {', '.join(JOB_BOARDS)}")
        sys.exit(1)

    board_name = sys.argv[1].lower()

    if board_name not in JOB_BOARDS:
        print(f"Unknown job board: {board_name}")
        print(f"Available job boards: {', '.join(JOB_BOARDS)}")
        sys.exit(1)

    board = JOB_BOARDS[board_name]

    print(f"=== {board['company']} ===")
    print()

    postings, teams = get_postings(board["url"])

    candidates = [
        posting
        for posting in postings
        if is_candidate_job(posting, teams, board["team_id"])
    ]

    print(f"Found {len(postings)} total jobs")
    print(f"Found {len(candidates)} candidate jobs")
    print()

    title_ranking = rank_jobs_by_title(candidates)

    top_five = json.loads(title_ranking)["ranked_jobs"][:5]

    jobs = fetch_selected_jobs(
        top_five,
        organization=board["organization"],
    )

    print()
    print(f"Fetched {len(jobs)} full job descriptions")
    print()

    results = []

    for i, job in enumerate(jobs):
        print(f"=== Analyzing {i + 1}/{len(jobs)}: {job['title']} ===")

        try:
            result = evaluate_job(job)
            analysis = json.loads(result)

            results.append({
                "title": job["title"],
                "location": job["locationName"],
                "workplace": job["workplaceType"],
                **analysis,
            })

            print(f"Score: {analysis['score']}/10")
            print()

        except Exception as e:
            print(f"AI analysis failed: {e}")
            print()

    results.sort(key=lambda job: job["score"], reverse=True)

    print()
    print("=== RANKING ===")

    for i, result in enumerate(results):
        print(
            f"{i + 1}. {result['title']} "
            f"({result['score']}/10) "
            f"- apply: {result['apply']}\n"
            f"Reasoning: {result['summary']}"
        )

if __name__ == "__main__":
    main()