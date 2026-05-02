import json
import logging
import argparse
from datetime import datetime
from config.settings import settings
from src.agent import Agent
from src.storage import save_results

logging.basicConfig(level=settings.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="PriceScout AI CLI")
    parser.add_argument("--product", type=str, required=True, help="Product name to search for (e.g., 'Sony WH-1000XM5')")
    parser.add_argument("--urls", type=str, required=False, help="Comma-separated format of competitor:url -> e.g. 'Amazon:http...,Target:http...'. If omitted, agent searches autonomously.")
    parser.add_argument("--max-results", type=int, default=3, help="Max results to fetch if doing autonomous search")
    
    args = parser.parse_args()
    
    print(f"Starting PriceScout MVP for '{args.product}'")
    agent = Agent()
    
    if args.urls:
        urls_input = args.urls.split(',')
        urls_to_process = []
        
        for u in urls_input:
            parts = u.split(':', 1)
            if len(parts) == 2:
                urls_to_process.append({"competitor": parts[0].strip(), "url": parts[1].strip()})
            else:
                print(f"Skipping invalid URL format: {u}. Please use Competitor:https://url")
                
        if not urls_to_process:
            print("No valid URLs provided. Exiting.")
            return
            
        results = agent.run_multi_url_search(args.product, urls_to_process)
    else:
        # Fully autonomous execution
        print("Autonomous mode: Searching web for best links...")
        results = agent.run_autonomous_search(args.product, max_results=args.max_results)
    
    if results:
        timestamp = datetime.now().strftime("%Y%md_%H%M%S")
        filename = f"price_results_{timestamp}.json"
        save_results(results, filename)
        print(f"\nSuccessfully processed {len(results)} URLs! Results saved to {filename}")
        
        for r in results:
            print(f"\n- {r.competitor}: {r.price} {r.currency} ({r.status})")
    else:
        print("\nNo results could be extracted.")

if __name__ == "__main__":
    main()