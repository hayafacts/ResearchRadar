from services.serpapi_service import search_google_scholar

results = search_google_scholar("artificial intelligence in education")

papers = results.get("organic_results", [])

for i, paper in enumerate(papers, start=1):
    print(f"\nPaper {i}")
    print("Title:", paper.get("title"))
    print("Authors:", paper.get("publication_info", {}).get("summary"))
    print("Link:", paper.get("link"))