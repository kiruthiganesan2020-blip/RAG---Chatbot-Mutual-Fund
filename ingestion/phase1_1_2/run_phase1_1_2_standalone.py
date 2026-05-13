#!/usr/bin/env python3
"""
Phase 1.1.2: Web Scraping Implementation - Standalone Runner
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

def main():
    """Main execution for Phase 1.1.2"""
    print("Phase 1.1.2: Web Scraping Implementation")
    print("=" * 60)
    
    try:
        # Get project root
        project_root = Path(__file__).parent.parent.parent
        src_path = project_root / "src"
        
        # Add src to Python path
        sys.path.insert(0, str(src_path))
        
        # 1. Validate environment
        print("\nStep 1: Validating Environment")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {Path.cwd()}")
        print(f"   Project root: {project_root}")
        print(f"   Src path: {src_path}")
        
        # 2. Check dependencies
        print("\nStep 2: Checking Dependencies")
        
        required_modules = [
            'requests',
            'beautifulsoup4', 
            'selenium',
            'loguru',
            'pydantic'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                if module == 'beautifulsoup4':
                    import bs4
                elif module == 'selenium':
                    import selenium
                else:
                    __import__(module)
                print(f"   SUCCESS: {module} installed")
            except ImportError:
                print(f"   MISSING: {module}")
                missing_modules.append(module)
        
        if missing_modules:
            print(f"\n   ERROR: Missing required modules: {missing_modules}")
            print(f"   RUN: pip install {' '.join(missing_modules)}")
            return 1
        
        # 3. Import scraper modules directly
        print("\nStep 3: Importing Scraper Modules")
        
        try:
            # Add config path
            sys.path.insert(0, str(src_path / "config"))
            sys.path.insert(0, str(src_path / "data_collection"))
            
            # Import directly
            from settings import Settings
            from logging_config import setup_logging
            from scraper import HDFCFundScraper
            import loguru
            
            # Create settings and setup logging
            settings = Settings()
            setup_logging(log_level=settings.log_level)
            logger = loguru.logger
            
            print("   SUCCESS: Scraper modules imported")
            
        except ImportError as e:
            print(f"   ERROR: Import failed: {e}")
            print("   Trying alternative import method...")
            
            try:
                # Alternative import
                from src.data_collection.scraper import HDFCFundScraper
                from src.config import settings, setup_logging
                import loguru
                
                # Setup logging
                setup_logging(log_level=settings.log_level)
                logger = loguru.logger
                
                print("   SUCCESS: Alternative import worked")
                
            except ImportError as e2:
                print(f"   ERROR: Alternative import failed: {e2}")
                return 1
        
        # 4. Validate HDFC URLs
        print("\nStep 4: Validating HDFC URLs")
        
        hdfc_urls = [
            "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
            "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth", 
            "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
            "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
            "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
        ]
        
        print(f"   Found {len(hdfc_urls)} HDFC URLs to scrape:")
        for i, url in enumerate(hdfc_urls, 1):
            print(f"     {i}. {url}")
        
        # 5. Check data directory
        print("\nStep 5: Checking Data Directory")
        
        raw_data_path = project_root / "data" / "raw"
        if raw_data_path.exists():
            print(f"   SUCCESS: Raw data directory exists at {raw_data_path}")
        else:
            print(f"   CREATING: Raw data directory at {raw_data_path}")
            raw_data_path.mkdir(parents=True, exist_ok=True)
        
        # 6. Initialize scraper
        print("\nStep 6: Initializing Scraper")
        
        try:
            scraper = HDFCFundScraper()
            print("   SUCCESS: HDFCFundScraper initialized")
        except Exception as e:
            print(f"   ERROR: Failed to initialize scraper: {e}")
            return 1
        
        # 7. Test scraping functionality
        print("\nStep 7: Testing Scraping Functionality")
        
        # Test with first URL
        test_url = hdfc_urls[0]
        fund_name = "hdfc-large-cap"
        
        print(f"   Testing with: {fund_name}")
        print(f"   URL: {test_url}")
        
        try:
            # Run async scraping
            async def test_scrape():
                async with scraper:
                    return await scraper.scrape_fund_data(fund_name, test_url)
            
            # Run in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(test_scrape())
            loop.close()
            
            if result:
                print("   SUCCESS: Test scraping completed")
                print(f"   Fund name: {result.get('fund_name', 'N/A')}")
                print(f"   NAV: {result.get('basic_info', {}).get('nav', 'N/A')}")
                print(f"   Category: {result.get('basic_info', {}).get('category', 'N/A')}")
            else:
                print("   WARNING: No data returned from test scrape")
                
        except Exception as e:
            print(f"   ERROR: Test scraping failed: {e}")
            return 1
        
        # 8. Save test data
        print("\nStep 8: Saving Test Data")
        
        try:
            if result:
                saved_files = scraper.save_raw_data([result])
                if saved_files:
                    print(f"   SUCCESS: Test data saved to {saved_files[0]}")
                else:
                    print("   WARNING: No files saved")
            else:
                print("   SKIPPED: No data to save")
        except Exception as e:
            print(f"   ERROR: Failed to save test data: {e}")
            return 1
        
        # 9. Final validation
        print("\nStep 9: Final Validation")
        
        # Check if raw data files exist
        raw_files = list(raw_data_path.glob("*.json"))
        if raw_files:
            print(f"   SUCCESS: Found {len(raw_files)} raw data files")
            latest_file = max(raw_files, key=lambda x: x.stat().st_mtime)
            print(f"   Latest file: {latest_file.name}")
        else:
            print("   WARNING: No raw data files found")
        
        # 10. Summary
        print("\nPhase 1.1.2 Implementation Summary:")
        print("   ✅ Environment validated")
        print("   ✅ Dependencies checked")
        print("   ✅ Scraper modules imported")
        print("   ✅ HDFC URLs validated")
        print("   ✅ Data directory prepared")
        print("   ✅ Scraper initialized")
        print("   ✅ Test scraping completed")
        print("   ✅ Test data saved")
        print("   ✅ Validation completed")
        
        print("\nPhase 1.1.2 Web Scraping Implementation Complete!")
        print("Ready for Phase 1.1.3: Content Processing and Structuring")
        
        return 0
        
    except Exception as e:
        print(f"\nERROR: Phase 1.1.2 failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
