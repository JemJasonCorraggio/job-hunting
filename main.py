from ashby import fetch_job


def main():
    job = fetch_job("85e808ab-ee45-4944-bedc-832bf933d0b6")

    print(job["title"])
    print(job["locationName"])
    print(job["workplaceType"])
    print(job["descriptionHtml"][:500])


if __name__ == "__main__":
    main()