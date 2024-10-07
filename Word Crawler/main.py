import requests

class GoogleSearchCrawler:
    def __init__(self, api_key, cse_id, search_term, total_results=20, page_size=10):
        self.api_key = api_key
        self.cse_id = cse_id
        self.search_term = search_term
        self.total_results = total_results  # Total number of results to fetch
        self.page_size = page_size  # Maximum results per request (up to 10)
        self.search_url = "https://www.googleapis.com/customsearch/v1"
        self.found_urls = []

    def search(self):
        for start in range(1, self.total_results, self.page_size):
            params = {
                "key": self.api_key,
                "cx": self.cse_id,
                "q": self.search_term,
                "num": self.page_size,
                "start": start
            }
            try:
                response = requests.get(self.search_url, params=params)
                response.raise_for_status()
                search_results = response.json()

                for result in search_results.get("items", []):
                    url = result.get("link")
                    title = result.get("title")
                    snippet = result.get("snippet")
                    self.found_urls.append({"title": title, "url": url, "snippet": snippet})

            except requests.RequestException as e:
                print(f"Error while searching: {e}")
                break  # Stop searching if there's an error

    def display_results(self):
        results = {}
        if self.found_urls:
            print(f"\nResults for '{self.search_term}':\n")
            for index, result in enumerate(self.found_urls, start=1):
                print(f"{index}. {result['title']}")
                print(f"   URL: {result['url']}")
                print(f"   Snippet: {result['snippet']}\n")
                results[index] = {"title": result['title'], "URL": result['url'], "Snippet": result['snippet']}
            return results
        else:
            print(f"No results found for '{self.search_term}'.")

if __name__ == "__main__":
    api_key = "AIzaSyC-zwSnNzttyfIuDN7O825ovOgY0L8iXKI"
    cse_id = "80e65eac15a724f7c"
    search_term = input("Enter the keyword or subject to search for: ")
    max_results = int(input("Enter the number of results to retrieve (e.g., 10): "))

    crawler = GoogleSearchCrawler(api_key, cse_id, search_term, max_results)
    crawler.search()
    results = crawler.display_results()
    try:
        if results:
            with open("result.txt", "w") as f:
                for k, v in results.items():
                    f.writelines(f"{k}. ")
                    for n, c in v.items():
                        f.writelines(f"{n}: {c}\n")
        else:
            print("There is nothing to save!")
    except Exception as e:
        print(e)
