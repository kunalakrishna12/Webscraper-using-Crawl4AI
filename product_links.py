import asyncio
from crawl4ai import AsyncWebCrawler

async def fetch_indiamart_links(inside_url, tradeindia_base_url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(inside_url)
        if result.success:
            internal_links = result.links.get("internal", [])
            print(f"Found {len(internal_links)} internal links.")
            
            # Extract 'href' values before filtering
            links = [link['href'] for link in internal_links if 'href' in link and link['href'].startswith(tradeindia_base_url)]
            
            # Check if tradeindia_base_url is present in links and pop if it is there
            if tradeindia_base_url in links:
                links.remove(tradeindia_base_url)
            
            return links
        else:
            print("Crawl failed:", result.error_message)
            return []


if __name__ == "__main__":
    inside_url = "https://dir.indiamart.com/impcat/hdpe-drums.html"
    tradeindia_base_url = "https://dir.indiamart.com/impcat"
    links = asyncio.run(fetch_indiamart_links(inside_url, tradeindia_base_url))
    for i in links:
        print(i)