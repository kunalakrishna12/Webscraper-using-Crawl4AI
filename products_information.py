# import asyncio
# import json
# import pandas as pd
# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# product_url = "https://www.indiamart.com/proddetail/60l-un-approved-hdpe-open-top-drum-2853043798833.html"

# async def extract_product_info(url):
#     """Extracts product details using Crawl4AI with magic mode enabled."""
#     schema = {
#         "name": "Example Items",
#         "baseSelector": "div.sfirst.wful.dsf.tmpm1",
#         "fields": [
#             {"name": "product_name", "selector": "h1.bo.center-heading.centerHeadHeight", "type": "text"},
#             {"name": "price", "selector": "span.bo.price-unit", "type": "text"},
#             {"name": "description", "selector": "div.isq-container", "type": "text"},
#             {"name": "owner", "selector": "div.cbg1.pd10.pd_tal.brde2.cmpnewUi", "type": "text"},
#         ]
#     }

#     crawler_config = CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS,  # ✅ Ensures fresh data is fetched
#         extraction_strategy=JsonCssExtractionStrategy(schema),
#     )

#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(url=url, config=crawler_config, magic=True)  # ✅ Enable magic mode
#         if result.success:
#             extracted_data = json.loads(result.extracted_content)
            
#             if isinstance(extracted_data, list) and extracted_data:
#                 product_info = extracted_data[0]  # ✅ Extract first product (assuming one result)
#                 product_info['product_url'] = url
#                 return product_info
#             else:
#                 print("Unexpected data format:", extracted_data)
#                 return None
#         else:
#             print(f"Failed to retrieve the page: {result.error_message}")
#             return None

# def run_scraper(product_url):
#     """Runs the scraper in an asyncio event loop and stores the data in an Excel file."""
#     try:
#         product_details = asyncio.run(extract_product_info(product_url))  # ✅ Run async function in main thread
#         if product_details:
#             print("\n✅ Extracted Product Information:")
#             for key, value in product_details.items():
#                 print(f"{key}: {value}")
            
#             # Store the extracted data in an Excel file
#             df = pd.DataFrame([product_details])
#             df.to_excel("extracted_product_info.xlsx", index=False)
#             print("\n✅ Data has been saved to 'extracted_product_info.xlsx'.")
#         else:
#             print("\n❌ No product details extracted.")
#     except RuntimeError as e:
#         print(f"Error running event loop: {e}")

# # if __name__ == "__main__":
# #     run_scraper()

import asyncio
import os
import json
import random
import pandas as pd
import time
import re
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# Constants
CONCURRENCY_LIMIT = 2  

# Random User-Agents (Helps avoid detection)
USER_AGENTS = [
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/537.36",
]

def clean_text(text):
    """Removes illegal characters that can't be used in Excel"""
    if isinstance(text, str):
        return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
    return text

async def auto_scroll(page):
    """Scrolls multiple times in a human-like way."""
    for _ in range(random.randint(5, 10)):
        await page.evaluate("window.scrollBy(0, window.innerHeight * Math.random())")
        await asyncio.sleep(random.uniform(3, 7))

async def extract_product_info(url):
    """Extracts product details with auto-scroll and Crawl4AI."""
    schema = {
        "name": "Product Details",
        "baseSelector": "body",
        "fields": [
            {"name": "product_title", "selector": "h1.bo.center-heading.centerHeadHeight", "type": "text"},
            {"name": "price", "selector": "span.bo.price-unit", "type": "text"},
            {"name": "product_specifications", "selector": "table.spec-table", "type": "table"},
            {"name": "product_overview", "selector": "div.fs14.color.tabledesc", "type": "text"},
            {"name": "company_details", "selector": "div#aboutUs.aboutus.fs16.lh28.mt30", "type": "text"},
            {"name": "business_details", "selector": "div.business-details", "type": "text"},
            {"name": "seller_details", "selector": "div.rdsp", "type": "text"},
            {"name": "vendor_name", "selector": "a.color6.pd_txu.bo", "type": "text"},
        ]
    }
    
    browser_config = BrowserConfig(headless=False)
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema),
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        await asyncio.sleep(random.uniform(5, 15))  
        result = await crawler.arun(url=url, config=crawler_config, magic=True)
        
        if result.success:
            extracted_data = json.loads(result.extracted_content)
            if isinstance(extracted_data, list) and extracted_data:
                product_info = extracted_data[0]
                product_info['product_url'] = url
                print(f"\n✅ Extracted product details from: {url}")
                print(json.dumps(product_info, indent=4))
                return product_info
        else:
            print(f"❌ Failed to extract data from {url}: {result.error_message}")
            return None

async def process_in_batches(product_links, batch_size=10):
    """Processes product links in batches."""
    product_details = []
    for i in range(0, len(product_links), batch_size):
        batch = product_links[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}: {len(batch)} links")
        batch_details = await asyncio.gather(*[extract_product_info(link) for link in batch])
        product_details.extend(batch_details)
        await asyncio.sleep(random.uniform(5, 10))  
    return product_details

async def main_cat(product_links):
    """Main function to process product links in batches."""
    start_time = time.time()
    print(f"\n📦 Extracting product details from {len(product_links)} links...")
    product_details = await process_in_batches(product_links, batch_size=10)
    
    filtered_details = [p for p in product_details if p is not None]
    print(f"\n✅ Extracted {len(filtered_details)} product details.")
    
    if filtered_details:
        df = pd.DataFrame(filtered_details).drop_duplicates(subset=['product_title'])
        
        # Clean text fields to remove illegal characters
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].apply(clean_text)
        
        os.makedirs("data", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = f"data/indiamart_products_{timestamp}.xlsx"
        df.to_excel(file_path, index=False)
        print(f"✅ Data saved as '{file_path}'")
    
    print(f"\n⏳ Total Execution Time: {time.time() - start_time:.2f} seconds")

# Example usage:
# asyncio.run(main_cat(["https://www.indiamart.com/proddetail/product1", "https://www.indiamart.com/proddetail/product2"]))
