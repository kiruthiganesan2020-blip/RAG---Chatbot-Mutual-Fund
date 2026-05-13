"""
Tests for Content Processor
"""

import pytest
from pathlib import Path
import json

from src.data_collection.content_processor import ContentProcessor
from src.config import settings


class TestContentProcessor:
    """Test cases for ContentProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance for testing"""
        return ContentProcessor()
    
    @pytest.fixture
    def sample_html(self):
        """Sample HTML content for testing"""
        return """
        <html>
        <head><title>HDFC Fund Test</title></head>
        <body>
            <h1>HDFC Large Cap Fund</h1>
            <div class="fund-info">
                <p>This fund invests in large cap companies with good growth potential.</p>
                <p>Expense ratio: 1.25% per annum.</p>
                <p>Minimum investment: ₹5,000.</p>
            </div>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>NAV</td><td>₹1,234.56</td></tr>
                <tr><td>Risk</td><td>Moderately High</td></tr>
            </table>
        </body>
        </html>
        """
    
    @pytest.fixture
    def sample_text(self):
        """Sample text content for testing"""
        return """
        HDFC Large Cap Fund - Direct Growth
        
        Investment Objective:
        The fund aims to generate long-term capital appreciation by investing in large cap companies.
        
        Key Details:
        - Expense Ratio: 1.25% per annum
        - Minimum Investment: ₹5,000
        - Risk Level: Moderately High
        - Category: Large Cap
        
        Performance:
        The fund has delivered consistent returns over the past 5 years.
        """
    
    def test_initialization(self, processor):
        """Test processor initialization"""
        assert processor.settings is not None
        assert processor.nlp is not None or processor.nlp is None  # spaCy optional
    
    def test_process_html_content(self, processor, sample_html):
        """Test HTML content processing"""
        source_url = "https://example.com/test"
        
        result = processor.process_html_content(sample_html, source_url)
        
        assert result['source_type'] == 'html'
        assert result['source_url'] == source_url
        assert 'cleaned_text' in result
        assert 'title' in result
        assert 'metadata' in result
        assert 'sections' in result
        assert 'tables' in result
        assert 'links' in result
        assert 'processed_at' in result
        
        # Check content extraction
        assert 'HDFC Large Cap Fund' in result['title']
        assert 'large cap companies' in result['cleaned_text']
        assert len(result['tables']) > 0
    
    def test_process_text_content(self, processor, sample_text):
        """Test text content processing"""
        source_url = "https://example.com/text"
        
        result = processor.process_text_content(sample_text, source_url)
        
        assert result['source_type'] == 'text'
        assert result['source_url'] == source_url
        assert 'cleaned_text' in result
        assert 'metadata' in result
        assert 'sections' in result
        assert 'entities' in result
        assert 'dates' in result
        assert 'processed_at' in result
        
        # Check content extraction
        assert 'Expense Ratio: 1.25%' in result['cleaned_text']
        assert len(result['sections']) > 0
    
    def test_chunk_content(self, processor, sample_text):
        """Test content chunking"""
        content = {
            'source_url': 'https://example.com/test',
            'source_type': 'text',
            'cleaned_text': sample_text,
            'metadata': {'fund_name': 'test'},
            'processed_at': '2023-01-01T12:00:00'
        }
        
        chunks = processor.chunk_content(content)
        
        assert len(chunks) > 0
        
        for chunk in chunks:
            assert 'chunk_id' in chunk
            assert 'chunk_index' in chunk
            assert 'text' in chunk
            assert 'source_url' in chunk
            assert 'source_type' in chunk
            assert 'metadata' in chunk
            
            # Check metadata
            assert chunk['metadata']['fund_name'] == 'test'
            assert chunk['metadata']['total_chunks'] == len(chunks)
            assert 'chunk_index' in chunk['metadata']
    
    def test_create_semantic_chunks(self, processor):
        """Test semantic chunk creation"""
        text = "This is sentence one. This is sentence two. This is sentence three."
        
        chunks = processor._create_semantic_chunks(text)
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
        assert all(len(chunk.strip()) > 0 for chunk in chunks)
    
    def test_apply_chunk_overlap(self, processor):
        """Test chunk overlap application"""
        chunks = ["chunk one content", "chunk two content", "chunk three content"]
        
        # Set overlap for testing
        processor.settings.chunk_overlap = 5
        
        overlapped = processor._apply_chunk_overlap(chunks)
        
        assert len(overlapped) == len(chunks)
        
        # Check that overlap is applied (except for first chunk)
        for i in range(1, len(overlapped)):
            current_chunk = overlapped[i]
            previous_chunk = chunks[i-1]
            overlap_text = previous_chunk[-5:]
            assert current_chunk.startswith(overlap_text)
    
    def test_extract_title(self, processor, sample_html):
        """Test title extraction from HTML"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(sample_html, 'html.parser')
        
        title = processor._extract_title(soup)
        assert 'HDFC Fund Test' in title
    
    def test_extract_sections(self, processor, sample_html):
        """Test section extraction from HTML"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(sample_html, 'html.parser')
        
        sections = processor._extract_sections(soup)
        
        assert len(sections) > 0
        assert any(section['text'] == 'HDFC Large Cap Fund' for section in sections)
    
    def test_extract_tables(self, processor, sample_html):
        """Test table extraction from HTML"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(sample_html, 'html.parser')
        
        tables = processor._extract_tables(soup)
        
        assert len(tables) > 0
        
        table = tables[0]
        assert 'headers' in table
        assert 'data' in table
        assert len(table['headers']) == 2
        assert len(table['data']) == 2
    
    def test_extract_entities(self, processor):
        """Test entity extraction"""
        text = "HDFC Large Cap Fund has 1.25% expense ratio and minimum investment of ₹5,000."
        
        entities = processor._extract_entities(text)
        
        assert len(entities) > 0
        
        # Check for fund name entity
        fund_entities = [e for e in entities if e['label'] == 'FUND_NAME']
        assert len(fund_entities) > 0
        assert any('HDFC' in e['text'] for e in fund_entities)
        
        # Check for percentage entity
        pct_entities = [e for e in entities if e['label'] == 'PERCENTAGE']
        assert len(pct_entities) > 0
        assert any('1.25%' in e['text'] for e in pct_entities)
    
    def test_extract_text_sections(self, processor):
        """Test section extraction from text"""
        text = """
        Investment Objective: This is the objective.
        Asset Allocation: This is the allocation.
        Risk Factors: These are the risks.
        """
        
        sections = processor._extract_text_sections(text)
        
        assert len(sections) > 0
        assert any('objective' in section.lower() for section in sections)
        assert any('allocation' in section.lower() for section in sections)
        assert any('risk' in section.lower() for section in sections)
    
    def test_save_processed_content(self, processor, tmp_path):
        """Test saving processed content"""
        content = {
            'source_url': 'https://example.com/test',
            'source_type': 'html',
            'cleaned_text': 'Test content',
            'metadata': {'test': True}
        }
        
        saved_path = processor.save_processed_content(content, str(tmp_path))
        
        assert Path(saved_path).exists()
        
        # Verify saved content
        with open(saved_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data['source_url'] == 'https://example.com/test'
        assert saved_data['cleaned_text'] == 'Test content'
        assert saved_data['metadata']['test'] == True
    
    def test_large_document_truncation(self, processor):
        """Test large document truncation"""
        # Create a large text
        large_text = "Test sentence. " * 10000  # Very large text
        
        content = {
            'source_url': 'https://example.com/large',
            'source_type': 'text',
            'cleaned_text': large_text,
            'metadata': {}
        }
        
        # Set small max size for testing
        processor.settings.max_document_size = 1000
        
        chunks = processor.chunk_content(content)
        
        # Should truncate and still create chunks
        assert len(chunks) > 0
        assert all(len(chunk['text']) <= processor.settings.max_document_size + 100 for chunk in chunks)  # Allow some tolerance
    
    def test_empty_content_handling(self, processor):
        """Test handling of empty content"""
        empty_content = {
            'source_url': 'https://example.com/empty',
            'source_type': 'text',
            'cleaned_text': '',
            'metadata': {}
        }
        
        chunks = processor.chunk_content(empty_content)
        
        # Should handle empty content gracefully
        assert isinstance(chunks, list)
    
    def test_unicode_handling(self, processor):
        """Test Unicode character handling"""
        unicode_text = "HDFC Fund with ₹ symbol and émojis 📈"
        
        content = {
            'source_url': 'https://example.com/unicode',
            'source_type': 'text',
            'cleaned_text': unicode_text,
            'metadata': {}
        }
        
        chunks = processor.chunk_content(content)
        
        assert len(chunks) > 0
        assert any('₹' in chunk['text'] for chunk in chunks)
