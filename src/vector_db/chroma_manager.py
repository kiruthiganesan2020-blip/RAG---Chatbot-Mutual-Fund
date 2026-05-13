"""
ChromaDB manager for vector storage and retrieval
"""

import asyncio
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import json
import uuid
from datetime import datetime

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
import numpy as np

from src.config import settings, get_logger
from .schema import VectorDBSchema, DocumentChunk, SearchResult

logger = get_logger(__name__)


class ChromaManager:
    """Manager for ChromaDB operations"""
    
    def __init__(self, collection_name: str = "mutual_funds"):
        self.settings = settings
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.embedding_function = None
        self._setup_database()
    
    def _setup_database(self):
        """Set up ChromaDB client and collection"""
        try:
            # Configure ChromaDB settings
            chroma_settings = ChromaSettings(
                persist_directory=self.settings.embeddings_path,
                anonymized_telemetry=False,
                allow_reset=True
            )
            
            # Initialize client
            self.client = chromadb.PersistentClient(
                path=self.settings.embeddings_path,
                settings=chroma_settings
            )
            
            # Initialize embedding function
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function
                )
                logger.info(f"Connected to existing collection: {self.collection_name}")
            except Exception as e:
                logger.warning(f"Could not connect to collection {self.collection_name}: {e}")
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function,
                    metadata=VectorDBSchema.get_collection_metadata()
                )
                logger.info(f"Created new collection: {self.collection_name}")
            
            logger.info("ChromaDB setup completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup ChromaDB: {e}")
            raise
    
    def add_documents(self, chunks: List[DocumentChunk]) -> List[str]:
        """Add document chunks to the vector database"""
        try:
            if not chunks:
                logger.warning("No chunks provided to add")
                return []
            
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            
            for chunk in chunks:
                # Generate unique ID
                chunk_id = str(uuid.uuid4())
                ids.append(chunk_id)
                
                # Add document text
                documents.append(chunk.text)
                
                # Prepare metadata
                metadata = {
                    'source_url': chunk.source_url,
                    'source_type': chunk.source_type,
                    'chunk_index': chunk.chunk_index,
                    'total_chunks': chunk.total_chunks,
                    'chunk_size': chunk.chunk_size,
                    'source_title': chunk.source_title,
                    'processed_at': chunk.processed_at,
                    'fund_name': chunk.metadata.get('fund_name', ''),
                    'category': chunk.metadata.get('category', ''),
                    'added_at': datetime.now().isoformat()
                }
                
                # Add additional metadata
                metadata.update(chunk.metadata)
                metadatas.append(metadata)
            
            # Add to collection in batches
            batch_size = self.settings.batch_size
            added_ids = []
            
            for i in range(0, len(ids), batch_size):
                batch_ids = ids[i:i + batch_size]
                batch_documents = documents[i:i + batch_size]
                batch_metadatas = metadatas[i:i + batch_size]
                
                self.collection.add(
                    ids=batch_ids,
                    documents=batch_documents,
                    metadatas=batch_metadatas
                )
                
                added_ids.extend(batch_ids)
                logger.info(f"Added batch of {len(batch_ids)} chunks to database")
            
            logger.info(f"Successfully added {len(added_ids)} chunks to vector database")
            return added_ids
            
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            raise
    
    def search_similar(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict] = None,
        where_document: Optional[Dict] = None
    ) -> List[SearchResult]:
        """Search for similar documents"""
        try:
            # Perform search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where,
                where_document=where_document,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Convert to SearchResult objects
            search_results = []
            
            if results['ids'] and results['ids'][0]:
                for i, doc_id in enumerate(results['ids'][0]):
                    search_result = SearchResult(
                        id=doc_id,
                        text=results['documents'][0][i],
                        metadata=results['metadatas'][0][i],
                        distance=results['distances'][0][i],
                        similarity_score=1 - results['distances'][0][i]  # Convert distance to similarity
                    )
                    search_results.append(search_result)
            
            logger.info(f"Found {len(search_results)} results for query: {query[:50]}...")
            return search_results
            
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            raise
    
    def get_document_by_id(self, doc_id: str) -> Optional[SearchResult]:
        """Get a specific document by ID"""
        try:
            results = self.collection.get(
                ids=[doc_id],
                include=['documents', 'metadatas']
            )
            
            if results['ids'] and results['ids'][0]:
                return SearchResult(
                    id=results['ids'][0],
                    text=results['documents'][0],
                    metadata=results['metadatas'][0],
                    distance=0.0,
                    similarity_score=1.0
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting document by ID {doc_id}: {e}")
            return None
    
    def update_document(self, doc_id: str, text: str, metadata: Optional[Dict] = None):
        """Update a document in the collection"""
        try:
            update_data = {'documents': [text]}
            
            if metadata:
                update_data['metadatas'] = [metadata]
            
            self.collection.update(
                ids=[doc_id],
                **update_data
            )
            
            logger.info(f"Updated document {doc_id} in ChromaDB")
            
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")
            raise
    
    def delete_document(self, doc_id: str):
        """Delete a document from the collection"""
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted document {doc_id} from ChromaDB")
            
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            raise
    
    def delete_by_source(self, source_url: str):
        """Delete all documents from a specific source"""
        try:
            # Find documents from source
            results = self.collection.get(
                where={'source_url': source_url},
                include=['ids']
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} documents from {source_url}")
            else:
                logger.info(f"No documents found for source: {source_url}")
                
        except Exception as e:
            logger.error(f"Error deleting documents from source {source_url}: {e}")
            raise
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            
            # Get sample of metadata for analysis
            sample_results = self.collection.get(
                limit=100,
                include=['metadatas']
            )
            
            stats = {
                'total_documents': count,
                'collection_name': self.collection_name,
                'sample_sources': list(set([
                    meta.get('source_url', '') 
                    for meta in sample_results.get('metadatas', [])
                ])),
                'sample_funds': list(set([
                    meta.get('fund_name', '') 
                    for meta in sample_results.get('metadatas', [])
                ])),
                'last_updated': datetime.now().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def backup_collection(self, backup_path: Optional[str] = None):
        """Backup the collection"""
        try:
            if backup_path is None:
                backup_path = Path(self.settings.embeddings_path) / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_path = Path(backup_path)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Get all documents
            all_docs = self.collection.get(
                include=['documents', 'metadatas', 'ids']
            )
            
            # Save to JSON
            backup_data = {
                'collection_name': self.collection_name,
                'backup_timestamp': datetime.now().isoformat(),
                'total_documents': len(all_docs['ids']),
                'documents': []
            }
            
            for i, doc_id in enumerate(all_docs['ids']):
                backup_data['documents'].append({
                    'id': doc_id,
                    'text': all_docs['documents'][i],
                    'metadata': all_docs['metadatas'][i]
                })
            
            backup_file = backup_path / f"{self.collection_name}_backup.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Collection backed up to {backup_file}")
            return str(backup_file)
            
        except Exception as e:
            logger.error(f"Error backing up collection: {e}")
            raise
    
    def restore_collection(self, backup_file: str):
        """Restore collection from backup"""
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Clear existing collection
            self.client.delete_collection(self.collection_name)
            
            # Recreate collection
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata=VectorDBSchema.get_collection_metadata()
            )
            
            # Restore documents
            documents = backup_data['documents']
            ids = [doc['id'] for doc in documents]
            texts = [doc['text'] for doc in documents]
            metadatas = [doc['metadata'] for doc in documents]
            
            # Add in batches
            batch_size = self.settings.batch_size
            for i in range(0, len(ids), batch_size):
                batch_ids = ids[i:i + batch_size]
                batch_texts = texts[i:i + batch_size]
                batch_metadatas = metadatas[i:i + batch_size]
                
                self.collection.add(
                    ids=batch_ids,
                    documents=batch_texts,
                    metadatas=batch_metadatas
                )
            
            logger.info(f"Restored {len(documents)} documents from backup")
            
        except Exception as e:
            logger.error(f"Error restoring collection: {e}")
            raise
    
    def reset_collection(self):
        """Reset the entire collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata=VectorDBSchema.get_collection_metadata()
            )
            logger.info(f"Reset collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        try:
            # In 0.4+, PersistentClient doesn't need explicit close, 
            # and reset() wipes the database if allow_reset is True.
            self.client = None
            logger.info("ChromaDB connection closed")
        except Exception as e:
            logger.error(f"Error closing ChromaDB: {e}")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
