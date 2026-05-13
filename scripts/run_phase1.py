#!/usr/bin/env python3
"""
Example script to run Phase 1 data collection
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.main import MutualFundDataCollector
from src.config.logging_config import get_logger

logger = get_logger(__name__)


async def main():
    """Run Phase 1 data collection"""
    logger.info("Starting Phase 1 data collection example")
    
    try:
        # Initialize collector
        collector = MutualFundDataCollector()
        
        # Run full pipeline
        success = await collector.run_full_pipeline()
        
        if success:
            logger.info("SUCCESS: Phase 1 data collection completed successfully!")
            print("\nPhase 1 Implementation Complete!")
            print("\nNext steps:")
            print("1. Review the collected data in data/raw/")
            print("2. Check processed data in data/processed/")
            print("3. Verify vector database in data/embeddings/")
            print("4. Run tests: pytest tests/")
            print("5. Proceed to Phase 2: RAG System Implementation")
        else:
            logger.error("FAILED: Phase 1 data collection failed")
            print("\nPhase 1 failed. Check logs for details.")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n⚠️  Operation cancelled")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
