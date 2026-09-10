from google import genai


client = genai.Client()


MODEL = "gemini-3.6-flash"


CANDIDATE_PROFILE = """
Senior backend software engineer and engineering lead.

Strong experience with:
- Go
- Scala and Java
- Python
- REST APIs and distributed systems
- AWS and GCP
- Terraform and cloud infrastructure
- PostgreSQL, MongoDB, Elasticsearch
- Observability, reliability, and production operations
- Developer tooling and SDKs
- Security-sensitive enterprise systems
- Technical leadership and mentoring

Experience includes owning production APIs and services, leading engineering teams,
working cross-functionally, and being responsible for on-call and reliability.

Interested in backend, platform, infrastructure, reliability, developer experience,
and production AI/agentic systems.

US citizen eligible for a CUSMA Professional (TN) work permit for qualifying
Canadian roles.
"""


def evaluate_job(job):
    prompt = f"""
You are helping a software engineer decide which jobs are worth applying to.

Candidate:
{CANDIDATE_PROFILE}

Job:
Title: {job["title"]}
Location: {job["locationName"]}
Workplace: {job["workplaceType"]}

Description:
{job["descriptionHtml"]}

Evaluate this job for the candidate.

Return:
1. Match score from 1-10
2. Whether the candidate should seriously consider applying
3. The strongest matches
4. The biggest gaps
5. A brief explanation

Be honest. Do not assume the candidate has experience that is not supported
by the candidate profile.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response.text

if __name__ == "__main__":
    chat = client.chats.create(model=MODEL)

    response = chat.send_message(
        "Respond with exactly: Gemini is working."
    )

    print(response.text)