"""
Content processing and structuring logic
"""

import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from src.config import settings, get_logger
from src.vector_db.schema import DocumentChunk, VectorDBSchema

logger = get_logger(__name__)

class ContentProcessor:
    """Processes and structures raw scraped content"""
    
    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
    
    def process_html_content(self, html_content: str, source_url: str) -> Dict[str, Any]:
        """Clean and structure HTML content"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else "Untitled Document"
            
            # Get main text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Basic cleanup
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\[.*?\]', '', text)
            
            return {
                'title': title,
                'text': text,
                'source_url': source_url,
                'processed_at': datetime.now().isoformat() if 'datetime' in globals() else ""
            }
        except Exception as e:
            logger.error(f"Error processing HTML: {e}")
            return {'title': 'Error', 'text': '', 'source_url': source_url}

    def create_chunks(
        self, 
        text: str, 
        source_url: str, 
        metadata: Dict[str, Any]
    ) -> List[DocumentChunk]:
        """Split text into chunks for vector storage"""
        if not text:
            return []
            
        # Simple character-based chunking with overlap
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            # Create chunk object
            chunk = VectorDBSchema.create_document_chunk(
                text=chunk_text,
                source_url=source_url,
                source_type='html',
                chunk_index=chunk_index,
                metadata=metadata
            )
            chunks.append(chunk)
            
            start += (self.chunk_size - self.chunk_overlap)
            chunk_index += 1
            
        # Update total chunks for each chunk
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total
            
        return chunks
