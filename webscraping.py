import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configure headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# List of 3 distinct URLs
URLS = [
    "https://www.reddit.com/search/?q=nvidia&type=posts&sort=top&t=all&cId=f8226b7e-d987-4fde-9d56-8106fb98b11f&iId=8368e59a-b36f-47a5-b241-acca8bf444f8",
    "https://www.reddit.com/search/?q=nvidia&type=posts&sort=top&t=month&cId=f8226b7e-d987-4fde-9d56-8106fb98b11f&iId=31f94a34-bc5b-4a2d-a19b-ec19e4d593db",
    "https://www.reddit.com/search/?q=nvidia&type=posts&sort=top&t=all&cId=f8226b7e-d987-4fde-9d56-8106fb98b11f&iId=623f0123-ecfd-4e6a-af0c-024f314cf67b"
]

def scrape_reddit():
    data = []
    
    for url in URLS:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("a", attrs={"class": "absolute inset-0"})
            
        for post in posts:
                try:
                    # Extract comment text
                    aria_label = post.get("aria-label")  
                    comment_text = aria_label if aria_label else "No text"                   
                    # Extract subreddit from URL
                    href = post.get("href", "")
                    subreddit = href.split("/")[2] if "/r/" in href else "Unknown"
                    
                    data.append({
                        "profile_name": subreddit,
                        "comment": comment_text
                    })
                    
                        
                except Exception as e:
                    print(f"Error processing post: {str(e)}...")
            
    return pd.DataFrame(data)

def main():
    print("Starting Reddit scraper...")
    df = scrape_reddit()
    
    if not df.empty:
        df.to_csv("nvidia_comments.csv", index=True)
        print(f"Success! Saved {len(df)} comments.")
        print(df.head(10))
    else:
        print("Failed to collect data. Potential issues:")
        print("- Reddit's anti-bot measures (add proxy rotation)")
        print("- Changed HTML structure (verify selectors)")

if __name__ == "__main__":
    main()
