"""
Tests for the HDFC Fund Scraper
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import json

from src.data_collection.scraper import HDFCFundScraper
from src.config import settings


class TestHDFCFundScraper:
    """Test cases for HDFCFundScraper"""
    
    @pytest.fixture
    def scraper(self):
        """Create scraper instance for testing"""
        return HDFCFundScraper()
    
    @pytest.fixture
    def sample_html(self):
        """Sample HTML content for testing"""
        return """
        <html>
        <head><title>HDFC Large Cap Fund - Direct Growth</title></head>
        <body>
            <h1>HDFC Large Cap Fund - Direct Growth</h1>
            <div class="fund-category">Large Cap</div>
            <div class="nav-value">₹1,234.56</div>
            <div class="expense-ratio">1.25%</div>
            <div class="min-investment">₹5,000</div>
            <div class="risk-level">Moderately High</div>
            <p>This fund invests in large cap companies...</p>
        </body>
        </html>
        """
    
    def test_initialization(self, scraper):
        """Test scraper initialization"""
        assert scraper.settings is not None
        assert scraper.session is not None
        assert scraper.driver is None
    
    def test_parse_fund_basic_info(self, scraper, sample_html):
        """Test basic fund information parsing"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(sample_html, 'html.parser')
        
        info = scraper._parse_fund_basic_info(soup)
        
        assert 'fund_name' in info
        assert 'HDFC Large Cap Fund' in info['fund_name']
        assert info.get('nav') == '1,234.56'
    
    def test_parse_fund_details(self, scraper, sample_html):
        """Test detailed fund information parsing"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(sample_html, 'html.parser')
        
        details = scraper._parse_fund_details(soup)
        
        assert details.get('expense_ratio') == '1.25%'
        assert details.get('min_investment') == '₹5,000'
        assert details.get('risk_level') == 'Moderately High'
    
    def test_extract_fund_description(self, scraper, sample_html):
        """Test fund description extraction"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(sample_html, 'html.parser')
        
        description = scraper._extract_fund_description(soup)
        
        assert 'invests in large cap companies' in description
    
    @pytest.mark.asyncio
    async def test_scrape_fund_data_success(self, scraper):
        """Test successful fund data scraping"""
        fund_name = "hdfc-large-cap"
        url = "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
        
        with patch.object(scraper, '_fetch_with_requests') as mock_fetch:
            mock_fetch.return_value = self.sample_html
            
            data = await scraper.scrape_fund_data(fund_name, url)
            
            assert data['fund_name'] == fund_name
            assert data['source_url'] == url
            assert 'basic_info' in data
            assert 'details' in data
            assert 'description' in data
            assert 'raw_html' in data
    
    @pytest.mark.asyncio
    async def test_scrape_fund_data_failure(self, scraper):
        """Test fund data scraping failure"""
        fund_name = "hdfc-large-cap"
        url = "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
        
        with patch.object(scraper, '_fetch_with_requests') as mock_fetch:
            mock_fetch.side_effect = Exception("Network error")
            
            with pytest.raises(Exception):
                await scraper.scrape_fund_data(fund_name, url)
    
    def test_save_raw_data(self, scraper, tmp_path):
        """Test saving raw data to files"""
        fund_data = [
            {
                'fund_name': 'test-fund',
                'source_url': 'https://example.com',
                'scraped_at': '2023-01-01 12:00:00',
                'basic_info': {},
                'details': {},
                'description': 'Test description',
                'raw_html': '<html>Test</html>'
            }
        ]
        
        saved_files = scraper.save_raw_data(fund_data, str(tmp_path))
        
        assert len(saved_files) == 1
        assert Path(saved_files[0]).exists()
        
        # Verify file content
        with open(saved_files[0], 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data['fund_name'] == 'test-fund'
        assert saved_data['source_url'] == 'https://example.com'
    
    def test_get_fund_url(self):
        """Test getting fund URL by name"""
        url = settings.get_fund_url('hdfc-large-cap')
        assert 'hdfc-large-cap-fund-direct-growth' in url
        
        url = settings.get_fund_url('non-existent-fund')
        assert url == ""
    
    def test_validate_urls(self):
        """Test URL validation"""
        assert settings.validate_urls() == True
        
        # Test with invalid URL
        original_urls = settings.hdfc_urls.copy()
        settings.hdfc_urls[0] = "https://invalid-url.com"
        
        assert settings.validate_urls() == False
        
        # Restore original URLs
        settings.hdfc_urls = original_urls
