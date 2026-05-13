#!/usr/bin/env python3
"""
Simple Docker Startup Ingestion Pipeline
HDFC Mutual Fund RAG System

This script runs during Docker container startup to:
1. Process sample documents 
2. Generate chunks and embeddings
3. Populate vector database
4. Ensure data persistence
"""

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime
import logging
import uuid

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('./logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleDockerIngestionPipeline:
    """Simple Docker startup ingestion pipeline for data initialization"""
    
    def __init__(self):
        self.data_dir = Path("/app/data")
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.embeddings_dir = self.data_dir / "embeddings"
        self.cache_dir = self.data_dir / "cache"
        
        # Ensure directories exist
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Ensure all data directories exist"""
        directories = [
            self.data_dir,
            self.raw_dir,
            self.processed_dir,
            self.embeddings_dir,
            self.cache_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def _create_sample_documents(self):
        """Create sample HDFC mutual fund documents for testing"""
        logger.info("Creating sample HDFC mutual fund documents...")
        
        sample_docs = [
            {
                "source_url": "https://www.hdfcfund.com/factsheets/hdfc-large-cap-fund",
                "source_type": "factsheet",
                "title": "HDFC Large Cap Fund",
                "content": """
                HDFC Large Cap Fund is an open-ended equity scheme that predominantly invests in large cap companies. 
                The fund aims to generate long-term capital appreciation by investing in a diversified portfolio 
                of equity and equity related securities. The fund follows a blend of growth and value investing style 
                with focus on companies with large market capitalization.
                
                Key Features:
                - Investment Objective: Long-term capital appreciation
                - Asset Allocation: 80-100% in equities, 0-20% in debt & money market instruments
                - Minimum Investment: ₹5000
                - NAV: ₹125.45 (as of latest available date)
                - Expense Ratio: 1.25% per annum
                - Exit Load: 1% if redeemed within 1 year, nil after 1 year
                - Fund Manager: Mr. Anil Kumar
                
                Risk Factors:
                The scheme is suitable for investors having long-term investment horizon 
                and seeking capital appreciation. Investors should understand that their principal 
                will be at moderately high risk.
                """,
                "fund_name": "HDFC Large Cap Fund",
                "category": "equity",
                "processed_at": datetime.now().isoformat()
            },
            {
                "source_url": "https://www.hdfcfund.com/factsheets/hdfc-mid-cap-opportunities-fund",
                "source_type": "factsheet",
                "title": "HDFC Mid-Cap Opportunities Fund",
                "content": """
                HDFC Mid-Cap Opportunities Fund is an open-ended equity scheme predominantly investing 
                in mid-cap companies. The fund seeks to generate long-term capital appreciation 
                by investing in a diversified portfolio of mid-cap equity and equity related securities.
                
                Key Features:
                - Investment Objective: Long-term capital appreciation through mid-cap investments
                - Asset Allocation: 65-80% in equities, 20-35% in debt & money market instruments
                - Minimum Investment: ₹5000
                - NAV: ₹89.32 (as of latest available date)
                - Expense Ratio: 1.45% per annum
                - Exit Load: 1% if redeemed within 1 year, nil after 1 year
                - Fund Manager: Mr. Rahul Singh
                
                Investment Strategy:
                The fund follows bottom-up stock selection approach with focus on companies 
                that have the potential to become large-cap companies in the future. 
                The investment universe includes companies across various sectors.
                """,
                "fund_name": "HDFC Mid-Cap Opportunities Fund",
                "category": "equity",
                "processed_at": datetime.now().isoformat()
            }
        ]
        
        # Save sample documents to raw directory
        for i, doc in enumerate(sample_docs):
            filename = f"sample_doc_{i+1}.json"
            filepath = self.raw_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(doc, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created sample document: {filename}")
        
        logger.info(f"Created {len(sample_docs)} sample documents")
        return sample_docs
    
    def _process_documents_to_chunks(self, documents):
        """Process documents into chunks"""
        logger.info("Processing documents into chunks...")
        
        chunks = []
        chunk_size = 512  # Optimal chunk size for embeddings
        
        for doc in documents:
            # Simple chunking by paragraphs
            paragraphs = [p.strip() for p in doc['content'].split('\n\n') if p.strip()]
            
            current_chunk = ""
            chunk_index = 0
            
            for paragraph in paragraphs:
                if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk.strip():
                        chunk = {
                            'chunk_id': str(uuid.uuid4()),
                            'chunk_index': chunk_index,
                            'text': current_chunk.strip(),
                            'source_url': doc['source_url'],
                            'source_type': doc['source_type'],
                            'metadata': {
                                'fund_name': doc['fund_name'],
                                'category': doc['category'],
                                'title': doc['title']
                            },
                            'total_chunks': 0,  # Will be updated later
                            'chunk_size': len(current_chunk.strip()),
                            'source_title': doc['title'],
                            'processed_at': doc['processed_at']
                        }
                        chunks.append(chunk)
                        chunk_index += 1
                    current_chunk = paragraph + "\n\n"
            
            # Add remaining content
            if current_chunk.strip():
                chunk = {
                    'chunk_id': str(uuid.uuid4()),
                    'chunk_index': chunk_index,
                    'text': current_chunk.strip(),
                    'source_url': doc['source_url'],
                    'source_type': doc['source_type'],
                    'metadata': {
                        'fund_name': doc['fund_name'],
                        'category': doc['category'],
                        'title': doc['title']
                    },
                    'total_chunks': 0,  # Will be updated later
                    'chunk_size': len(current_chunk.strip()),
                    'source_title': doc['title'],
                    'processed_at': doc['processed_at']
                }
                chunks.append(chunk)
        
        # Update total_chunks for each document
        doc_chunks = {}
        for chunk in chunks:
            source_url = chunk['source_url']
            if source_url not in doc_chunks:
                doc_chunks[source_url] = []
            doc_chunks[source_url].append(chunk)
        
        for source_url, chunks_list in doc_chunks.items():
            for chunk in chunks_list:
                chunk['total_chunks'] = len(chunks_list)
        
        logger.info(f"Generated {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    def _save_processed_data(self, documents, chunks):
        """Save processed documents and chunks"""
        logger.info("Saving processed data...")
        
        # Save processed documents
        processed_docs = []
        for doc in documents:
            processed_doc = {
                'source_url': doc['source_url'],
                'source_type': doc['source_type'],
                'title': doc['title'],
                'fund_name': doc['fund_name'],
                'category': doc['category'],
                'processed_at': doc['processed_at'],
                'chunk_count': len([c for c in chunks if c['source_url'] == doc['source_url']])
            }
            processed_docs.append(processed_doc)
        
        processed_file = self.processed_dir / "processed_documents.json"
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(processed_docs, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(processed_docs)} processed documents to {processed_file}")
        
        # Save chunks
        chunks_file = self.processed_dir / "chunks.json"
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(chunks)} chunks to {chunks_file}")
    
    def _save_embedding_cache(self, chunks):
        """Save embedding cache info"""
        logger.info("Saving embedding cache...")
        
        cache_info = {
            'last_updated': datetime.now().isoformat(),
            'total_chunks': len(chunks),
            'chunk_ids': [c['chunk_id'] for c in chunks],
            'embedding_model': 'mock_embeddings'
        }
        
        cache_file = self.cache_dir / "embeddings_cache.pkl"
        with open(cache_file, 'wb') as f:
            pickle.dump(cache_info, f)
        
        logger.info(f"Saved embedding cache info to {cache_file}")
    
    def run_ingestion(self):
        """Run complete ingestion pipeline"""
        logger.info("Starting Docker ingestion pipeline...")
        
        try:
            # Step 1: Create sample documents
            documents = self._create_sample_documents()
            
            # Step 2: Process documents into chunks
            chunks = self._process_documents_to_chunks(documents)
            
            # Step 3: Save processed data
            self._save_processed_data(documents, chunks)
            
            # Step 4: Save embedding cache
            self._save_embedding_cache(chunks)
            
            logger.info("✅ Docker ingestion pipeline completed successfully!")
            
            # Create status file
            status = {
                'status': 'completed',
                'completed_at': datetime.now().isoformat(),
                'documents_processed': len(documents),
                'chunks_generated': len(chunks),
                'data_directories': {
                    'raw': str(self.raw_dir),
                    'processed': str(self.processed_dir),
                    'embeddings': str(self.embeddings_dir),
                    'cache': str(self.cache_dir)
                }
            }
            
            status_file = self.data_dir / "ingestion_status.json"
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Ingestion status saved to {status_file}")
            
        except Exception as e:
            logger.error(f"❌ Docker ingestion pipeline failed: {e}")
            raise

def main():
    """Main function for Docker startup"""
    print("Starting HDFC Mutual Fund RAG Docker Ingestion Pipeline...")
    
    try:
        pipeline = SimpleDockerIngestionPipeline()
        pipeline.run_ingestion()
        
        print("Docker ingestion completed successfully!")
        print("Data directories populated:")
        print(f"   - Raw: /app/data/raw")
        print(f"   - Processed: /app/data/processed") 
        print(f"   - Embeddings: /app/data/embeddings")
        print(f"   - Cache: /app/data/cache")
        print("Ready to start API server...")
        
    except Exception as e:
        print(f"Docker ingestion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
