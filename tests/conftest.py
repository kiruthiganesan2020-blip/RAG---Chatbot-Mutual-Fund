"""
Pytest configuration and fixtures
"""

import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil

from src.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_settings(temp_dir):
    """Create sample settings for testing"""
    # Override settings for testing
    settings.raw_data_path = str(temp_dir / "raw")
    settings.processed_data_path = str(temp_dir / "processed") 
    settings.embeddings_path = str(temp_dir / "embeddings")
    settings.log_file = str(temp_dir / "test.log")
    
    # Ensure directories exist
    settings.ensure_directories()
    
    yield settings


@pytest.fixture
def sample_fund_data():
    """Sample fund data for testing"""
    return {
        'fund_name': 'hdfc-large-cap',
        'source_url': 'https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth',
        'scraped_at': '2023-01-01 12:00:00',
        'basic_info': {
            'fund_name': 'HDFC Large Cap Fund - Direct Growth',
            'nav': '1,234.56'
        },
        'details': {
            'expense_ratio': '1.25%',
            'min_investment': '₹5,000',
            'risk_level': 'Moderately High'
        },
        'description': 'This fund invests in large cap companies...',
        'raw_html': '<html><body><h1>HDFC Large Cap Fund</h1></body></html>'
    }


@pytest.fixture
def sample_processed_content():
    """Sample processed content for testing"""
    return {
        'source_type': 'html',
        'source_url': 'https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth',
        'cleaned_text': 'HDFC Large Cap Fund invests in large cap companies with good growth potential.',
        'title': 'HDFC Large Cap Fund',
        'metadata': {
            'fund_name': 'HDFC Large Cap Fund',
            'category': 'Large Cap'
        },
        'sections': [
            {'level': 1, 'text': 'HDFC Large Cap Fund'}
        ],
        'tables': [],
        'links': [],
        'processed_at': '2023-01-01T12:00:00'
    }
