import os
from dotenv import load_dotenv
from config.settings import settings
from src.search import SearchTool

# Force reload real dotfiles just for testing this script directly
load_dotenv(".env", override=True)

def main():
    print("Testing Tavily Search Tool...\n")
    searcher = SearchTool()
    
    product_query = "PlayStation 5 Pro"
    print(f"Querying for: {product_query}")
    
    results = searcher.find_product_urls(product_query, max_results=3)
    
    if not results:
        print("No results found. (Maybe using a missing or test API key?)")
    else:
        for idx, res in enumerate(results, 1):
            print(f"{idx}. {res['competitor']}")
            print(f"   Title: {res.get('title', 'N/A')}")
            print(f"   URL: {res['url']}\n")

if __name__ == "__main__":
    main()