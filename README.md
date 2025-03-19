# Crawl4AI Webscraper

## Overview
Crawl4AI Webscraper is a Python-based web scraping tool designed to extract product information from IndiaMART. It uses advanced techniques to avoid detection and handle CAPTCHAs, ensuring reliable data extraction.

## Features
- **Asynchronous Web Scraping**: Utilizes `asyncio` for concurrent web scraping.
- **CAPTCHA Handling**: Supports automatic CAPTCHA solving using 2Captcha.
- **Random User-Agents**: Rotates user-agents to avoid detection.
- **Data Cleaning**: Cleans extracted data to remove illegal characters for Excel compatibility.
- **Batch Processing**: Processes product links in batches to manage load and avoid detection.
