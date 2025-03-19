import asyncio
import os
import pandas as pd
import re
import time
import subprocess
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import random
from main import main_cat

CONCURRENCY_LIMIT = 5

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
]

async def limited_arun(crawler, url, semaphore):
    """Limits the number of concurrent web scraping requests."""
    async with semaphore:
        return await crawler.arun(url)

async def filter_category_links(search_links):
    """Filters out category pages from the search links."""
    return [link for link in search_links if "impcat" in link]

async def get_google_search_links(product: str, location: str = " ", num_pages: int = 10):
    """Scrapes Google search results and filters only TradeIndia vendor links."""
    base_google_url = "https://www.google.com/search?q=site:indiamart.com +{}+{}&start={}"
    formatted_product = "+".join(product.split())
    formatted_location = "+".join(location.split())
    search_links = []
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    # Randomly choose a User-Agent for each request
    def get_random_user_agent():
        return random.choice(USER_AGENTS)

    # Configure the browser with the proxy and headers
    async with AsyncWebCrawler(config=BrowserConfig(headers={"User-Agent": get_random_user_agent()})) as crawler:
        tasks = [
            limited_arun(crawler, base_google_url.format(formatted_product, formatted_location, page * 10), semaphore)
            for page in range(num_pages)
        ]
        results = await asyncio.gather(*tasks)
        for result in results:
            if result.success:
                search_results = result.links.get("external", [])
                search_links.extend(
                    link["href"] for link in search_results if isinstance(link, dict) and "href" in link
                )
            else:
                print(f":x: Failed to scrape Google: {result.error_message}")
            await asyncio.sleep(random.uniform(2, 5))  # Prevent IP bans
    return search_links

if __name__ == "__main__":
    # Get the search links
    search_links = asyncio.run(get_google_search_links("Stainless Steel 316 Round Bar", num_pages=5))
    print(f":mag: Found {len(search_links)} search links.")
    category_links = asyncio.run(filter_category_links(search_links))
    print(f":mag: Found {len(category_links)} category links.")
    print(category_links)
    for i in category_links:
        # main_cat(i)
        asyncio.run(main_cat(i))
        time.sleep(5)
    print("Done")
