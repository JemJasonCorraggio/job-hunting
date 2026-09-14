from google import genai


client = genai.Client()


MODEL = "gemini-3.6-flash"


CANDIDATE_PROFILE = """
Summary
Senior Backend Software Engineer and Engineering Lead candidate skilled in planning and leading development in new products or enhancements, writing and reviewing clean, testable code, and determining the appropriate scope and timeline for deliverables. Experienced with Scala, Akka, Play, Java, Go, Python, C++, VB, React, jQuery, Node.js including API architecture, SDKs, and alerting systems. Excited to pick up the new technologies and methods to meet the needs of the project. 
As a U.S. citizen, eligible for a CUSMA Professional (TN) work permit - no LMIA required.
Skills and Languages
Engineering: Go, Java, Scala, Akka, Play, REST APIs, Terraform, AWS, GCP, PostgreSQL, MongoDB, Elasticsearch, Grafana, DataDog, Splunk, Honeycomb, TDD, Swagger, Jira, OOP and FP, JavaScript, React, jQuery, Node.js, HTML, CSS, C++, VB, Git, GitHub
AI Development Tools: Experience incorporating AI tools into software design, coding, debugging, and documentation workflows
Leadership: Team leadership, project planning, mentoring, incident response, on-call management, cross-functional communication
Languages: English - Fluent, French - B1
Actively preparing for certification to be eligible for the Francophone Mobility program - no LMIA required.
Experience
GreyNoise Intelligence	Remote from Philadelphia, PA
Lead Software Engineer / Oncall Lead	05/23-05/25
Oversaw 2 teams (4 direct reports) including planning projects, mentoring engineers through 1:1s and reviewing code
Owned, iterated on, and maintained an API using Go, Terraform, and Gin, and querying large data from Elasticsearch
Designed and implemented multiple additional services in a monorepo to deliver alerts, reports, and real-time feed events to customers (Go, Terraform, S3, Google Storage, Protobuf, lambdas, webhooks)
Maintained an SDK for integrations with the API using Python
Implemented the transition from PagerDuty / StatusPage to Incident.io,  saving money and improving the oncall experience
Managed the oncall shifts for the entire company, including implementing Terraform based alerts in Grafana and Honeycomb
Capital One	Remote from Philadelphia, PA
Senior Software Engineer	01/22-04/23
Initiated an investigation into a cross-functional DEI related code change that would affect 1500+ systems, including meeting with technical and non-technical stakeholders.
Developed endpoints in Scala using ZIO for a new Docker microservice.
Wrote unit tests and service tests utilizing Wiremock 
Learned Go in order to write canary tests that run every 10 minutes
TrueAccord	Remote from Philadelphia, PA
Tech Lead of the Multiple Account Project / Oncall Admin of the Recover Team	03/21-12/21
Designed and implemented a technical solution using to allow communication and logging to occur at the consumer level for consumers with multiple accounts (Scala, Postgres, jsonb,  Akka, Play)
Directed, code reviewed, and assisted other engineers working on the project
Represented the team and the interests of the project at meetings with external engineering teams and the product team
Managed the on call shifts and alerts for the team acted as the first point of escalation (DataDog / Splunk)
Wingspan Technology, an IQVIA Company	Blue Bell, PA
Engineering Lead of the Technical Services Team	05/18 – 03/21
Led a globally distributed team to deliver solutions for client-specific problems or requests, including a Scala API built to migrate 10k documents in a single run while tracking over 60 pieces of metadata, among other features.
Designed and oversaw the analysis, development, maintenance and testing of multiple software solutions, including an on-going cross-team project for handling time-sensitive client requests for data corrections (Scala/Java)	
Learned Scala and familiarized myself with a large and complex code base using primarily Java and Scala.
Wyzant Tutoring, 21st Century Cyber Charter School	Greater Philadelphia Area, PA
Math and Science Tutor/Math Teacher	08/09 – 05/18
Built an online Statistics course (HTML / CSS).
Built a scheduling program (C++ then VB).
Education
Rensselaer Polytechnic Institute	BS, Mathematics	
12 Comp Sci credits including 8 in  C++, Emily Roebling Scholarship for Mathematics

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

Prioritize strong matches for backend, platform, infrastructure, reliability,
developer experience, distributed systems, APIs, cloud infrastructure, and
technical leadership.

Treat frontend-heavy roles and roles requiring substantial experience that the
candidate does not have as weaker matches.

Score potential jobs from the point of view of the employer - the candidate can
decide if s/he wants the job. S/he needs to know the likelyhood of getting an
interview.

Be honest. Do not assume the candidate has experience that is not supported
by the candidate profile.

Return your response as JSON with exactly these fields:

{{
  "score": <number from 1 to 10>,
  "apply": <true or false>,
  "strongest_matches": [
    "<strongest reason this job matches the candidate>",
    "<another strong match>"
  ],
  "biggest_gaps": [
    "<most important missing experience or qualification>",
    "<another significant gap>"
  ],
  "summary": "<brief explanation of the overall fit>"
}}

Field definitions:
- "score": Overall match from 1 to 10, where 1 is a very poor fit and 10 is an exceptional fit.
- "apply": Whether the candidate should seriously consider spending time applying to this role.
- "strongest_matches": The 2-4 most important ways the candidate's experience aligns with the role.
- "biggest_gaps": The 1-3 most important weaknesses, missing experience, or qualifications.
- "summary": A concise explanation of why the role is or is not a strong opportunity for this candidate.

Return only valid JSON. Do not include markdown formatting or any text outside the JSON object.

"""

    chat = client.chats.create(model=MODEL)

    response = chat.send_message(prompt)

    return response.text

def rank_jobs_by_title(jobs):
    jobs_text = "\n\n".join(
        f"""JOB {i + 1}
Title: {job["title"]}
ID: {job["id"]}
Location: {job["locationName"]}
Workplace: {job["workplaceType"]}"""
        for i, job in enumerate(jobs)
    )

    prompt = f"""
You are helping a software engineer prioritize jobs to investigate further.

Candidate profile:
{CANDIDATE_PROFILE}

Below is a list of jobs that have already passed a basic filter for
department/team and Canadian location eligibility.

Your task is NOT to decide whether the candidate should ultimately apply.
Instead, rank the jobs by which ones are most worth retrieving and reading
the full job description for.

Prioritize titles suggesting:
- backend software engineering
- platform or infrastructure engineering
- distributed systems
- APIs
- cloud infrastructure
- reliability / SRE
- developer experience / developer tooling
- security engineering
- agentic or AI engineering where the role also appears to involve substantial software engineering
- technical leadership / engineering management where the candidate's leadership experience is relevant

Deprioritize titles that strongly suggest:
- frontend-heavy work
- mobile development
- data science
- data annotation
- TPM/project management
- roles requiring a specialized background not evident from the candidate profile

Be especially careful not to assume that a title containing "AI" is
automatically a strong match.

Do not de-prioritize jobs based on primary location, all jobs on this list should
have Canada as a location, but it may be a secondary location.

Rank ALL jobs from most to least likely for the candidate to get an interview 
based only on the information available from the title and metadata.

IMPORTANT:

At this stage you only have the job title and basic metadata. Do not assume
which programming languages, frameworks, cloud providers, databases, tools,
or other technologies the job uses unless they are explicitly stated in the
job title or metadata.

You may use the candidate's experience to judge whether a title appears
promising. For example, an "Infrastructure" role is potentially relevant
because the candidate has infrastructure experience. However, do not claim
that the role uses Go, Terraform, AWS, GCP, Elasticsearch, etc. unless that
information is actually present.

The purpose of this ranking is to decide which jobs deserve retrieval of the
full job description. It is acceptable for a job with a promising title to
rank highly even if there are important unknowns that can only be resolved
from the full description.

The score should represent "promise based on the title and metadata", not
final candidate-job fit.

Return ONLY valid JSON in this exact format:

{{
  "ranked_jobs": [
    {{
      "title": <title>,
      "id": <id>,
      "score": <number from 1 to 10>,
      "reason": "<Briefly explain why the TITLE makes it worth investigating based on
the candidate's background. Explicitly distinguish known information from
unknowns. Do not describe technologies or requirements that are not visible
in the title or metadata."
    }}
  ]
}}

Use the exact job ID and exact job title provided for each job.
Do not modify, abbreviate, or invent either value.

Jobs:

{jobs_text}
"""

    chat = client.chats.create(model=MODEL)
    response = chat.send_message(prompt)

    text = response.text.strip()

    if text.startswith("```"):
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        
    return text

if __name__ == "__main__":
    chat = client.chats.create(model=MODEL)

    response = chat.send_message(
        "Respond with exactly: Gemini is working."
    )

    print(response.text)