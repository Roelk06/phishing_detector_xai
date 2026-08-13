import requests
import pandas as pd
import random
import os

class DataPipeline:
    def __init__(self):
        self.phishing_url = "https://openphish.com/feed.txt"

    def fetch_phishing_urls(self, max_urls = 500):
        try:
            response = requests.get(self.phishing_url)
            urls = response.text.splitlines()

            random.shuffle(urls)
            selected_urls = urls[:max_urls]
            return selected_urls
        
        except Exception as e:
            return []

    def fetch_safe_urls(self, max_urls = 500):
        trusted_domains = ["github.com", "wikipedia.org", "tilburguniversity.edu", "google.com", "microsoft.com", "apple.com", "nos.nl", "linkedin.com", "stackoverflow.com", "spotify.com"]
        common_paths = ["/login", "/about", "/contact", "/user/settings", "/update", ""]

        safe_urls = []

        for _ in range(max_urls):
                domain = random.choice(trusted_domains)
                path = random.choice(common_paths)
                protocol = random.choice(["http://", "https://"])
                safe_urls.append(f"{protocol}{domain}{path}")
        return safe_urls

    def build_dataset(self):
        phishing_urls = self.fetch_phishing_urls(max_urls=200)
        safe_urls = self.fetch_safe_urls(max_urls=200)

        data = []
        for url in phishing_urls:
            data.append({"url": url, "label": 1})
        for url in safe_urls:
            data.append({"url": url, "label": 0})

        df = pd.DataFrame(data)
        df = df.sample(frac=1).reset_index(drop=True)  

        save_path = "data/url_dataset.csv"
        df.to_csv(save_path, index=False)

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.build_dataset()

