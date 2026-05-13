"""
Main entry point for Mutual Fund FAQ Assistant data ingestion
"""

import asyncio
import sys
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

from src.config import settings, setup_logging, get_logger
from src.data_collection.scraper import HDFCFundScraper
from src.data_collection.content_processor import ContentProcessor
from src.data_collection.metadata_extractor import MetadataExtractor
from src.vector_db.chroma_manager import ChromaManager
from src.vector_db.schema import VectorDBSchema

logger = get_logger(__name__)


class MutualFundDataCollector:
    """Orchestrates the data collection and ingestion process"""
    
    def __init__(self):
        self.settings = settings
        self.scraper = HDFCFundScraper()
        self.processor = ContentProcessor()
        self.metadata_extractor = MetadataExtractor()
        self.chroma_manager = ChromaManager()
        
    async def run_full_pipeline(self):
        """Run the end-to-end ingestion pipeline"""
        logger.info("Starting Mutual Fund Data Ingestion Pipeline")
        start_time = datetime.now()
        
        try:
            # 1. Scrape data
            logger.info("Phase 1: Scraping HDFC Mutual Fund data")
            scraped_data = await self.scraper.scrape_all_funds(self.settings.hdfc_urls)
            
            # 2. Process and ingest
            logger.info("Phase 2: Processing and ingesting data")
            total_chunks = 0
            
            for fund in scraped_data:
                source_url = fund['source_url']
                fund_name = fund['fund_name']
                
                if fund.get('status') == 'success':
                    # Process HTML content
                    processed_content = self.processor.process_html_content(
                        fund['raw_html'], 
                        source_url
                    )
                    
                    # Extract metadata
                    metadata = self.metadata_extractor.extract_metadata(processed_content)
                    metadata['fund_name'] = fund_name
                    
                    # Create document chunks
                    chunks = self.processor.create_chunks(
                        processed_content['text'],
                        source_url,
                        metadata
                    )
                    
                    # Add to vector database
                    if chunks:
                        self.chroma_manager.add_documents(chunks)
                        total_chunks += len(chunks)
                        logger.info(f"Ingested {len(chunks)} chunks for {fund_name}")
                else:
                    logger.warning(f"Skipping fund {fund_name} due to scraping failure")
            
            end_time = datetime.now()
            duration = end_time - start_time
            logger.info(f"Pipeline completed successfully in {duration}")
            logger.info(f"Total chunks ingested: {total_chunks}")
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
        finally:
            self.chroma_manager.close()


async def main():
    """Main execution function"""
    setup_logging()
    collector = MutualFundDataCollector()
    await collector.run_full_pipeline()


if __name__ == "__main__":
    asyncio.run(main())
