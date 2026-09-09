from ashby import fetch_jobs


def main():
    url = "https://jobs.ashbyhq.com/cohere?departmentId=68960387-27ac-4599-81a6-0b61399ef7eb&embed=js&locationId=40d7466c-5909-4da1-aabc-5029d77b5a9b&utm_source=chatgpt.com"

    page = fetch_jobs(url)

    with open("ashby_response.html", "w", encoding="utf-8") as f:
        f.write(page)

    print(f"Saved {len(page)} characters to ashby_response.html")


if __name__ == "__main__":
    main()