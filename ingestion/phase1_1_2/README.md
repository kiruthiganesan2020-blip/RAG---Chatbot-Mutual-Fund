# Phase 1.1.2: Web Scraping Implementation

## Overview

This sub-phase implements robust web scraping for HDFC mutual fund URLs with fallback mechanisms and comprehensive error handling.

## Objective

Build robust web scraping for HDFC mutual fund URLs with Selenium fallback, retry logic, and respectful scraping practices.

## Components

### Web Scraper
- `src/data_collection/scraper.py` - HDFCFundScraper class
- HTML content extraction from Groww URLs
- Selenium fallback for JavaScript-heavy pages
- Rate limiting and respectful scraping

### Data Extraction
- Structured data extraction (fund name, NAV, expense ratio)
- Pattern-based information parsing
- Metadata extraction and validation
- Raw data storage with timestamps

### Error Handling
- Retry mechanisms with exponential backoff
- Network failure recovery
- Graceful degradation strategies
- Comprehensive logging

## Usage

### Basic Scraping
```python
from src.data_collection import HDFCFundScraper

async with HDFCFundScraper() as scraper:
    # Scrape single fund
    fund_data = await scraper.scrape_fund_data("hdfc-large-cap", url)
    
    # Scrape all funds
    all_funds = await scraper.scrape_all_funds()
    
    # Save data
    saved_files = scraper.save_raw_data(all_funds)
```

### Command Line
```bash
# Run scraping for all funds
python src/main.py --mode collect

# Run for specific fund
python src/main.py --mode collect --fund hdfc-large-cap

# Run with debug logging
python src/main.py --mode collect --log-level DEBUG
```

## Configuration

### Scraping Settings
- `SCRAPING_DELAY` - Delay between requests (default: 2s)
- `MAX_RETRIES` - Maximum retry attempts (default: 3)
- `REQUEST_TIMEOUT` - Request timeout (default: 30s)
- `CONCURRENT_REQUESTS` - Concurrent requests (default: 5)

### URLs Configuration
The system is configured to scrape exactly these 5 HDFC URLs:
- HDFC Large Cap Fund Direct Growth
- HDFC Mid Cap Fund Direct Growth  
- HDFC Equity Fund Direct Growth
- HDFC Focused Fund Direct Growth
- HDFC ELSS Tax Saver Fund Direct Plan Growth

## Data Structure

### Scraped Data Format
```json
{
  "fund_name": "hdfc-large-cap",
  "source_url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
  "scraped_at": "2023-01-01 12:00:00",
  "basic_info": {
    "fund_name": "HDFC Large Cap Fund - Direct Growth",
    "nav": "1,234.56",
    "category": "Large Cap"
  },
  "details": {
    "expense_ratio": "1.25%",
    "min_investment": "₹5,000",
    "risk_level": "Moderately High"
  },
  "description": "Fund description text...",
  "raw_html": "<html>...</html>"
}
```

## Error Handling

### Retry Logic
- Exponential backoff with configurable delays
- Different strategies for network vs. parsing errors
- Circuit breaker pattern for repeated failures

### Fallback Mechanisms
- Primary: requests library for static content
- Fallback: Selenium for dynamic JavaScript content
- Final fallback: Partial data extraction

## Compliance

- **Rate Limiting**: Respectful scraping with delays
- **User-Agent**: Proper browser identification
- **Source Limitation**: Only official HDFC/AMFI sources
- **Data Privacy**: No PII collection

## Validation

Run scraping validation:
```bash
python src/main.py --mode validate
```

## Deliverables

✅ `src/data_collection/scraper.py` with HDFCFundScraper class
✅ Support for both requests and Selenium-based scraping  
✅ Raw data storage in `data/raw/` directory
✅ Comprehensive error handling and logging
✅ Rate limiting and respectful scraping practices
✅ Structured data extraction with metadata

## Next Steps

After completing Phase 1.1.2, proceed to Phase 1.1.3: Content Processing and Structuring.
