# # import asyncio
# # import os
# # import json
# # import random
# # import pandas as pd
# # import time
# # import requests
# # from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
# # from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
# # from playwright.async_api import async_playwright

# # # ✅ Constants
# # CONCURRENCY_LIMIT =   2# 🔥 Lower concurrency to reduce detection
# # # CATEGORY_URL = "https://dir.indiamart.com/impcat/hdpe-drums.html"
# # USE_CAPTCHA_SOLVER = True  # 🔥 Set to True to enable 2Captcha solving

# # # ✅ CAPTCHA Solver API Key (2Captcha)
# # API_KEY = "e4d8886140d521e8a2ba1031f3ffc908"

# # # ✅ Random User-Agents (Helps avoid detection)
# # USER_AGENTS = [
# #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
# #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
# #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# # ]

# # async def auto_scroll(page):
# #     """Scrolls multiple times in a human-like way."""
# #     for _ in range(random.randint(5, 10)):  
# #         await page.evaluate("window.scrollBy(0, window.innerHeight * Math.random())")
# #         await asyncio.sleep(random.uniform(3, 7))  # 🔥 Increased delay for realism

# # async def simulate_human_interaction(page):
# #     """Simulates random mouse movements and interactions to bypass bot detection."""
# #     for _ in range(random.randint(3, 7)):
# #         x, y = random.randint(100, 900), random.randint(100, 600)
# #         await page.mouse.move(x, y, steps=random.randint(5, 15))
# #         await asyncio.sleep(random.uniform(1, 3))

# # async def solve_recaptcha(page):
# #     """Solves reCAPTCHA using 2Captcha API."""
# #     site_key = await page.evaluate("document.querySelector('iframe[title=\"reCAPTCHA\"]').dataset.sitekey")
# #     page_url = page.url

# #     print("⚠️ CAPTCHA detected! Trying to solve...")

# #     response = requests.get(f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={site_key}&pageurl={page_url}")
# #     if "OK" not in response.text:
# #         print("❌ Failed to submit CAPTCHA request!")
# #         return False
    
# #     captcha_id = response.text.split('|')[1]
# #     await asyncio.sleep(20)  # 🔥 Wait for CAPTCHA to be solved

# #     for _ in range(10):  # 🔥 Retry fetching solution
# #         solution_response = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}")
# #         if "OK" in solution_response.text:
# #             captcha_solution = solution_response.text.split('|')[1]
# #             await page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_solution}";')
# #             await page.locator("button[type='submit']").click()
# #             print("✅ CAPTCHA solved successfully!")
# #             return True
# #         await asyncio.sleep(5)

# #     print("❌ CAPTCHA solution failed!")
# #     return False

# # async def fetch_product_links(category_url):
# #     """Fetches product links using Playwright with anti-detection features."""
# #     user_agent = random.choice(USER_AGENTS)

# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(
# #             headless=False,  # 🔥 Use a real browser instead of headless
# #             args=["--disable-blink-features=AutomationControlled"]  # 🔥 Stealth mode
# #         )
# #         context = await browser.new_context(
# #             user_agent=user_agent,
# #             ignore_https_errors=True,
# #             viewport={"width": random.randint(900, 1200), "height": random.randint(600, 900)}
# #         )
# #         page = await context.new_page()

# #         # 🔥 Load `stealth.min.js` to prevent detection
# #         await page.add_init_script("""() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); }""")

# #         print(f"\n🔍 Navigating to {category_url} with User-Agent: {user_agent}")
# #         try:
# #             await page.goto(category_url, timeout=240000, wait_until="networkidle")  
# #             await auto_scroll(page)  
# #             await simulate_human_interaction(page)  

# #             # 🔥 Check if CAPTCHA appears
# #             if await page.locator('iframe[title="reCAPTCHA"]').count() > 0:
# #                 if USE_CAPTCHA_SOLVER:
# #                     solved = await solve_recaptcha(page)
# #                     if not solved:
# #                         print("❌ Exiting due to CAPTCHA failure.")
# #                         await browser.close()
# #                         return []
# #                 else:
# #                     print("❌ CAPTCHA detected! Try reducing speed or using a proxy.")
# #                     await browser.close()
# #                     return []

# #             product_link_selector = "a[href*='/proddetail/']"
# #             await page.wait_for_selector(product_link_selector, timeout=90000)  

# #             links = await page.locator(product_link_selector).evaluate_all(
# #                 "elements => elements.map(el => el.href)"
# #             )

# #             await browser.close()

# #             print(f"✅ Extracted {len(links)} product links:")
# #             for link in links:
# #                 print(f"🔗 {link}")

# #             return list(set(links))  

# #         except Exception as e:
# #             print(f"❌ Failed to load {category_url}: {e}")
# #             await browser.close()
# #             return []

# # async def extract_product_info(url):
# #     """Extracts product details from IndiaMART using Crawl4AI."""
# #     schema = {
# #         "name": "Product Data",
# #         "baseSelector": "body",
# #         "fields": [
# #             {"name": "product_name", "selector": "h1.bo.center-heading.centerHeadHeight", "type": "text"},
# #             {"name": "price", "selector": "span.bo.price-unit", "type": "text"},
# #             {"name": "product_specifications", "selector": "table.spec-table", "type": "table"},
# #             {"name": "product_overview", "selector": "div.fs14.color.tabledesc", "type": "text"},
# #             {"name": "company_details", "selector": "div#aboutUs.aboutus.fs16.lh28.mt30", "type": "text"},
# #             {"name": "business_details", "selector": "div.business-details", "type": "text"},
# #             {"name": "seller_details", "selector": "div.rdsp", "type": "text"},
# #             {"name": "vendor_name", "selector": "a.color6.pd_txu.bo", "type": "text"},
# #         ]
# #     }

# #     crawler_config = CrawlerRunConfig(
# #         cache_mode=CacheMode.BYPASS,  
# #         extraction_strategy=JsonCssExtractionStrategy(schema),
# #     )

# #     async with AsyncWebCrawler() as crawler:  
# #         await asyncio.sleep(random.uniform(5, 15))  
# #         result = await crawler.arun(url=url, config=crawler_config, magic=True)
# #         if result.success:
# #             extracted_data = json.loads(result.extracted_content)
# #             if isinstance(extracted_data, list) and extracted_data:
# #                 product_info = extracted_data[0]
# #                 product_info['product_url'] = url
# #                 print(f"\n✅ Extracted product details from: {url}")
# #                 print(json.dumps(product_info, indent=4))  
# #                 return product_info
# #         else:
# #             print(f"❌ Failed to extract data from {url}: {result.error_message}")
# #             return None

# # async def main_cat(CATEGORY_URL):
# #     """Main function."""
# #     start_time = time.time()
# #     product_links = await fetch_product_links(CATEGORY_URL)

# #     if not product_links:
# #         print("❌ No product links found.")
# #         return

# #     print("\n📦 Extracting product details...")
# #     # product_details = await asyncio.gather(*[extract_product_info(link) for link in product_links])

# #     # filtered_details = [p for p in product_details if p is not None]  

# #     print(f"\n✅ Extracted {len(product_links)} product details.")

# #     # if filtered_details:
# #     #     df = pd.DataFrame(filtered_details).drop_duplicates(subset=['product_name'])
# #     #     os.makedirs("data", exist_ok=True)
# #     #     # Generate a unique filename with timestamp
# #     #     timestamp = time.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
# #     #     file_path = f"data/indiamart_products_{timestamp}.xlsx"

# #     #     # Save the file
# #     #     df.to_excel(file_path, index=False)
# #     #     print(f"✅ Data saved as '{file_path}'")

# #     print(f"\n⏳ Total Execution Time: {time.time() - start_time:.2f} seconds")

# # # if __name__ == "__main__":
# # #     asyncio.run(main_cat(link))


# import asyncio
# import os
# import json
# import random
# import pandas as pd
# import time
# import requests
# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
# from playwright.async_api import async_playwright
# # :white_check_mark: Constants
# CONCURRENCY_LIMIT =   2# :fire: Lower concurrency to reduce detection
# # CATEGORY_URL = "https://dir.indiamart.com/impcat/hdpe-drums.html"
# USE_CAPTCHA_SOLVER = True  # :fire: Set to True to enable 2Captcha solving
# # :white_check_mark: CAPTCHA Solver API Key (2Captcha)
# API_KEY = "e4d8886140d521e8a2ba1031f3ffc908"
# # :white_check_mark: Random User-Agents (Helps avoid detection)
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# ]
# async def auto_scroll(page):
#     """Scrolls multiple times in a human-like way."""
#     for _ in range(random.randint(5, 10)):
#         await page.evaluate("window.scrollBy(0, window.innerHeight * Math.random())")
#         await asyncio.sleep(random.uniform(3, 7))  # :fire: Increased delay for realism
# async def simulate_human_interaction(page):
#     """Simulates random mouse movements and interactions to bypass bot detection."""
#     for _ in range(random.randint(3, 7)):
#         x, y = random.randint(100, 900), random.randint(100, 600)
#         await page.mouse.move(x, y, steps=random.randint(5, 15))
#         await asyncio.sleep(random.uniform(1, 3))
# async def solve_recaptcha(page):
#     """Solves reCAPTCHA using 2Captcha API."""
#     site_key = await page.evaluate("document.querySelector('iframe[title=\"reCAPTCHA\"]').dataset.sitekey")
#     page_url = page.url
#     print(":warning: CAPTCHA detected! Trying to solve...")
#     response = requests.get(f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={site_key}&pageurl={page_url}")
#     if "OK" not in response.text:
#         print(":x: Failed to submit CAPTCHA request!")
#         return False
#     captcha_id = response.text.split('|')[1]
#     await asyncio.sleep(20)  # :fire: Wait for CAPTCHA to be solved
#     for _ in range(10):  # :fire: Retry fetching solution
#         solution_response = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}")
#         if "OK" in solution_response.text:
#             captcha_solution = solution_response.text.split('|')[1]
#             await page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_solution}";')
#             await page.locator("button[type='submit']").click()
#             print(":white_check_mark: CAPTCHA solved successfully!")
#             return True
#         await asyncio.sleep(5)
#     print(":x: CAPTCHA solution failed!")
#     return False
# async def fetch_product_links(category_url):
#     """Fetches product links using Playwright with anti-detection features."""
#     user_agent = random.choice(USER_AGENTS)
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(
#             headless=False,  # :fire: Use a real browser instead of headless
#             args=["--disable-blink-features=AutomationControlled"]  # :fire: Stealth mode
#         )
#         context = await browser.new_context(
#             user_agent=user_agent,
#             ignore_https_errors=True,
#             viewport={"width": random.randint(900, 1200), "height": random.randint(600, 900)}
#         )
#         page = await context.new_page()
#         # :fire: Load `stealth.min.js` to prevent detection
#         await page.add_init_script("""() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); }""")
#         print(f"\n:mag: Navigating to {category_url} with User-Agent: {user_agent}")
#         try:
#             await page.goto(category_url, timeout=240000, wait_until="networkidle")
#             await auto_scroll(page)
#             await simulate_human_interaction(page)
#             # :fire: Check if CAPTCHA appears
#             if await page.locator('iframe[title="reCAPTCHA"]').count() > 0:
#                 if USE_CAPTCHA_SOLVER:
#                     solved = await solve_recaptcha(page)
#                     if not solved:
#                         print(":x: Exiting due to CAPTCHA failure.")
#                         await browser.close()
#                         return []
#                 else:
#                     print(":x: CAPTCHA detected! Try reducing speed or using a proxy.")
#                     await browser.close()
#                     return []
#             product_link_selector = "a[href*='/proddetail/']"
#             await page.wait_for_selector(product_link_selector, timeout=90000)
#             links = await page.locator(product_link_selector).evaluate_all(
#                 "elements => elements.map(el => el.href)"
#             )
#             await browser.close()
#             print(f":white_check_mark: Extracted {len(links)} product links:")
#             for link in links:
#                 print(f":link: {link}")
#             return list(set(links))
#         except Exception as e:
#             print(f":x: Failed to load {category_url}: {e}")
#             await browser.close()
#             return []
# async def extract_product_info(url):
#     """Extracts product details from IndiaMART using Crawl4AI."""
#     schema = {
#             "name": "HDPE Drum Details",
#             "baseSelector": "body",
#             "fields": [
#                 {"name": "product_title", "selector": "h1.bo.center-heading.centerHeadHeight", "type": "text"},
#                 {"name": "price", "selector": "span.bo.price-unit", "type": "text"},
#                 {
#                     "name": "product_specifications",
#                     "selector": "table.spec-table",
#                     "type": "table"
#                 },
#                 {"name": "product_overview", "selector": "div.fs14.color.tabledesc", "type": "text"},
#                 {"name": "company_details", "selector": "div#aboutUs.aboutus.fs16.lh28.mt30", "type": "text"},
#                 {"name": "business_details", "selector": "div.business-details", "type": "text"},
#                 {"name": "seller_details", "selector": "div.rdsp", "type": "text"},
#                 {"name": "vendor_name", "selector": "a.color6.pd_txu.bo", "type": "text"},
#                 # Not scraping product_url because it's already available
#             ]
#         }
#     crawler_config = CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS,
#         extraction_strategy=JsonCssExtractionStrategy(schema),
#     )
#     async with AsyncWebCrawler() as crawler:
#         await asyncio.sleep(random.uniform(5, 15))
#         result = await crawler.arun(url=url, config=crawler_config, magic=True)
#         if result.success:
#             extracted_data = json.loads(result.extracted_content)
#             if isinstance(extracted_data, list) and extracted_data:
#                 product_info = extracted_data[0]
#                 product_info['product_url'] = url
#                 print(f"\n:white_check_mark: Extracted product details from: {url}")
#                 print(json.dumps(product_info, indent=4))
#                 return product_info
#         else:
#             print(f":x: Failed to extract data from {url}: {result.error_message}")
#             return None
# async def process_in_batches(product_links, batch_size=10):
#     """Processes product links in batches."""
#     product_details = []
#     for i in range(0, len(product_links), batch_size):
#         batch = product_links[i:i + batch_size]
#         print(f"Processing batch {i//batch_size + 1}: Links - {batch}")  # Debugging
#         batch_details = await asyncio.gather(*[extract_product_info(link) for link in batch])
#         product_details.extend(batch_details)  # Append results from the batch
#         await asyncio.sleep(random.uniform(5, 10))  # Add delay after each batch
#     return product_details
# async def main_cat(CATEGORY_URL):
#     """Main function."""
#     start_time = time.time()
#     product_links = await fetch_product_links(CATEGORY_URL)
#     if not product_links:
#         print(":x: No product links found.")
#         return
#     print("\n:package: Extracting product details...", len(product_links))
#     product_details = await process_in_batches(product_links, batch_size=10)  # Process in batches
#     filtered_details = [p for p in product_details if p is not None]
#     print(f"\n:white_check_mark: Extracted {len(filtered_details)} product details.")
#     if filtered_details:
#         df = pd.DataFrame(filtered_details).drop_duplicates(subset=['product_title'])
#         os.makedirs("data", exist_ok=True)
#         # Generate a unique filename with timestamp
#         timestamp = time.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
#         file_path = f"data/indiamart_products_{timestamp}.xlsx"
#         # Save the file
#         df.to_excel(file_path, index=False)
#         print(f":white_check_mark: Data saved as '{file_path}'")
#     print(f"\n:hourglass_flowing_sand: Total Execution Time: {time.time() - start_time:.2f} seconds")

# import asyncio
# import os
# import json
# import random
# import pandas as pd
# import time
# import requests
# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
# from playwright.async_api import async_playwright
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # ✅ Configuration
# CONCURRENCY_LIMIT = 2  # 🔥 Lower concurrency to reduce detection
# USE_CAPTCHA_SOLVER = True  # 🔥 Set to True to enable 2Captcha solving
# USER_AGENTS = [  # ✅ Random User-Agents (Helps avoid detection)
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# ]

# # ✅ Selenium CAPTCHA Detection (Alternative)
# def detect_captcha_selenium(driver, timeout=5):
#     """Detects CAPTCHA using Selenium and prompts manual solving."""
#     try:
#         captcha_element = WebDriverWait(driver, timeout).until(
#             EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'captcha')]"))
#         )
#         if captcha_element:
#             print("CAPTCHA detected by Selenium! Please solve it manually.")
#             input("Press Enter after solving the CAPTCHA...")
#             return True  # CAPTCHA detected and handled
#         else:
#             return False  # No CAPTCHA detected
#     except:
#         return False  # No CAPTCHA detected


# async def auto_scroll(page):
#     """Scrolls multiple times in a human-like way."""
#     for _ in range(random.randint(5, 10)):
#         await page.evaluate("window.scrollBy(0, window.innerHeight * Math.random())")
#         await asyncio.sleep(random.uniform(3, 7))  # 🔥 Increased delay for realism


# async def simulate_human_interaction(page):
#     """Simulates random mouse movements and interactions to bypass bot detection."""
#     for _ in range(random.randint(3, 7)):
#         x, y = random.randint(100, 900), random.randint(100, 600)
#         await page.mouse.move(x, y, steps=random.randint(5, 15))
#         await asyncio.sleep(random.uniform(1, 3))

# async def fetch_product_links(category_url, use_selenium_captcha=False):
#     """Fetches product links using Playwright with anti-detection features."""
#     user_agent = random.choice(USER_AGENTS)
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(
#             headless=False,  # 🔥 Use a real browser instead of headless
#             args=["--disable-blink-features=AutomationControlled"]  # 🔥 Stealth mode
#         )
#         context = await browser.new_context(
#             user_agent=user_agent,
#             ignore_https_errors=True,
#             viewport={"width": random.randint(900, 1200), "height": random.randint(600, 900)}
#         )
#         page = await context.new_page()
#         # 🔥 Load `stealth.min.js` to prevent detection
#         await page.add_init_script("""() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); }""")
#         print(f"\n:mag: Navigating to {category_url} with User-Agent: {user_agent}")
#         try:
#             await page.goto(category_url, timeout=240000, wait_until="networkidle")
#             await auto_scroll(page)
#             await simulate_human_interaction(page)

#             # Selenium CAPTCHA handling
#             if use_selenium_captcha:
#                 # Initialize WebDriver for CAPTCHA detection
#                 selenium_options = webdriver.ChromeOptions()
#                 selenium_options.add_argument(f"user-agent={user_agent}")  # Consistent UA
#                 selenium_options.add_argument("--start-maximized")
#                 selenium_driver = webdriver.Chrome(options=selenium_options)
#                 selenium_driver.get(category_url)  # Load in Selenium
#                 if detect_captcha_selenium(selenium_driver):
#                     # CAPTCHA was handled manually.  Now transfer back control
#                     selenium_driver.quit()  # Close Selenium
#                     # Potentially reload page in Playwright or continue
#                     await page.reload() # reload
#                 else:
#                     selenium_driver.quit() # close
#                     print("No CAPTCHA detected by Selenium")

#             # Playwright CAPTCHA handling
#             if await page.locator('iframe[title="reCAPTCHA"]').count() > 0:
#                 if USE_CAPTCHA_SOLVER:
#                     solved = await solve_recaptcha(page)
#                     if not solved:
#                         print(":x: Exiting due to CAPTCHA failure.")
#                         await browser.close()
#                         return []
#                 else:
#                     print(":x: CAPTCHA detected! Try reducing speed or using a proxy.")
#                     await browser.close()
#                     return []

#             product_link_selector = "a[href*='/proddetail/']"
#             await page.wait_for_selector(product_link_selector, timeout=90000)
#             links = await page.locator(product_link_selector).evaluate_all(
#                 "elements => elements.map(el => el.href)"
#             )
#             await browser.close()
#             print(f":white_check_mark: Extracted {len(links)} product links:")
#             for link in links:
#                 print(f":link: {link}")
#             return list(set(links))
#         except Exception as e:
#             print(f":x: Failed to load {category_url}: {e}")
#             await browser.close()
#             return []

# async def extract_product_info(url):
#     """Extracts product details from IndiaMART using Crawl4AI."""
#     schema = {
#             "name": "HDPE Drum Details",
#             "baseSelector": "body",
#             "fields": [
#                 {"name": "product_title", "selector": "h1.bo.center-heading.centerHeadHeight", "type": "text"},
#                 {"name": "price", "selector": "span.bo.price-unit", "type": "text"},
#                 {
#                     "name": "product_specifications",
#                     "selector": "table.spec-table",
#                     "type": "table"
#                 },
#                 {"name": "product_overview", "selector": "div.fs14.color.tabledesc", "type": "text"},
#                 {"name": "company_details", "selector": "div#aboutUs.aboutus.fs16.lh28.mt30", "type": "text"},
#                 {"name": "business_details", "selector": "div.business-details", "type": "text"},
#                 {"name": "seller_details", "selector": "div.rdsp", "type": "text"},
#                 {"name": "vendor_name", "selector": "a.color6.pd_txu.bo", "type": "text"},
#                 # Not scraping product_url because it's already available
#             ]
#         }
#     crawler_config = CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS,
#         extraction_strategy=JsonCssExtractionStrategy(schema),
#     )
#     async with AsyncWebCrawler() as crawler:
#         await asyncio.sleep(random.uniform(5, 15))
#         result = await crawler.arun(url=url, config=crawler_config, magic=True)
#         if result.success:
#             extracted_data = json.loads(result.extracted_content)
#             if isinstance(extracted_data, list) and extracted_data:
#                 product_info = extracted_data[0]
#                 product_info['product_url'] = url
#                 print(f"\n:white_check_mark: Extracted product details from: {url}")
#                 print(json.dumps(product_info, indent=4))
#                 return product_info
#         else:
#             print(f":x: Failed to extract data from {url}: {result.error_message}")
#             return None

# async def process_in_batches(product_links, batch_size=10):
#     """Processes product links in batches."""
#     product_details = []
#     for i in range(0, len(product_links), batch_size):
#         batch = product_links[i:i + batch_size]
#         print(f"Processing batch {i//batch_size + 1}: Links - {batch}")  # Debugging
#         batch_details = await asyncio.gather(*[extract_product_info(link) for link in batch])
#         product_details.extend(batch_details)  # Append results from the batch
#         await asyncio.sleep(random.uniform(5, 10))  # Add delay after each batch
#     return product_details

# async def main_cat(CATEGORY_URL, use_selenium_captcha=True):
#     """Main function."""
#     start_time = time.time()
#     product_links = await fetch_product_links(CATEGORY_URL, use_selenium_captcha)
#     if not product_links:
#         print(":x: No product links found.")
#         return
#     print("\n:package: Extracting product details...", len(product_links))
#     product_details = await process_in_batches(product_links, batch_size=10)  # Process in batches
#     filtered_details = [p for p in product_details if p is not None]
#     print(f"\n:white_check_mark: Extracted {len(filtered_details)} product details.")
#     if filtered_details:
#         df = pd.DataFrame(filtered_details).drop_duplicates(subset=['product_title'])
#         os.makedirs("data", exist_ok=True)
#         # Generate a unique filename with timestamp
#         timestamp = time.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
#         file_path = f"data/indiamart_products_{timestamp}.xlsx"
#         # Save the file
#         df.to_excel(file_path, index=False)
#         print(f":white_check_mark: Data saved as '{file_path}'")
#     print(f"\n:hourglass_flowing_sand: Total Execution Time: {time.time() - start_time:.2f} seconds")



import asyncio
import os
import json
import random
import pandas as pd
import time
import requests
import re
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from playwright.async_api import async_playwright
# :white_check_mark: Constants
CONCURRENCY_LIMIT = 2  # :fire: Lower concurrency to reduce detection
USE_CAPTCHA_SOLVER = True  # :fire: Enable 2Captcha solving
# :white_check_mark: CAPTCHA Solver API Key (2Captcha)
API_KEY = "e4d8886140d521e8a2ba1031f3ffc908"
# :white_check_mark: Random User-Agents (Helps avoid detection)
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
        return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)  # Remove non-printable ASCII characters
    return text
async def auto_scroll(page):
    """Scrolls multiple times in a human-like way."""
    for _ in range(random.randint(5, 10)):
        await page.evaluate("window.scrollBy(0, window.innerHeight * Math.random())")
        await asyncio.sleep(random.uniform(3, 7))
async def fetch_product_links(category_url):
    """Fetches product links using Playwright with anti-detection features."""
    user_agent = random.choice(USER_AGENTS)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent=user_agent,
            ignore_https_errors=True,
            viewport={"width": random.randint(900, 1200), "height": random.randint(600, 900)}
        )
        page = await context.new_page()
        await page.add_init_script("""() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); }""")
        print(f"\n:mag: Navigating to {category_url} with User-Agent: {user_agent}")
        try:
            await page.goto(category_url, timeout=240000, wait_until="networkidle")
            await auto_scroll(page)
            product_link_selector = "a[href*='/proddetail/']"
            await page.wait_for_selector(product_link_selector, timeout=90000)
            links = await page.locator(product_link_selector).evaluate_all(
                "elements => elements.map(el => el.href)"
            )
            await browser.close()
            print(f":white_check_mark: Extracted {len(links)} product links.")
            return list(set(links))
        except Exception as e:
            print(f":x: Failed to load {category_url}: {e}")
            await browser.close()
            return []
async def extract_product_info(url):
    """Extracts product details from IndiaMART using Crawl4AI."""
    schema = {
        "name": "HDPE Drum Details",
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
                print(f"\n:white_check_mark: Extracted product details from: {url}")
                print(json.dumps(product_info, indent=4))
                return product_info
        else:
            print(f":x: Failed to extract data from {url}: {result.error_message}")
            return None
async def process_in_batches(product_links, batch_size=10):
    """Processes product links in batches."""
    product_details = []
    for i in range(0, len(product_links), batch_size):
        batch = product_links[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}: {batch}")
        batch_details = await asyncio.gather(*[extract_product_info(link) for link in batch])
        product_details.extend(batch_details)
        await asyncio.sleep(random.uniform(5, 10))
    return product_details
async def main_cat(CATEGORY_URL):
    """Main function."""
    start_time = time.time()
    product_links = await fetch_product_links(CATEGORY_URL)
    if not product_links:
        print(":x: No product links found.")
        return
    print("\n:package: Extracting product details...", len(product_links))
    product_details = await process_in_batches(product_links, batch_size=10)
    filtered_details = [p for p in product_details if p is not None]
    print(f"\n:white_check_mark: Extracted {len(filtered_details)} product details.")
    if filtered_details:
        df = pd.DataFrame(filtered_details).drop_duplicates(subset=['product_title'])
        # :fire: Clean all text fields to remove illegal characters
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].apply(clean_text)
        os.makedirs("data", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = f"data/indiamart_products_{timestamp}.xlsx"
        df.to_excel(file_path, index=False)
        print(f":white_check_mark: Data saved as '{file_path}'")
    print(f"\n:hourglass_flowing_sand: Total Execution Time: {time.time() - start_time:.2f} seconds")
# # :fire: Run the script
# if __name__ == "__main__":
#     CATEGORY_URL = "https://dir.indiamart.com/impcat/hdpe-drums.html"
#     asyncio.run(main_cat(CATEGORY_URL))