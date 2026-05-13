#!/usr/bin/env python3
"""
Test and compare embedding models for mutual fund RAG system
"""

import sys
import os
from pathlib import Path
import time
import numpy as np
from typing import List, Dict, Any
import json

def main():
    """Test embedding models comparison"""
    print("Embedding Models Comparison Test")
    print("=" * 50)
    
    try:
        # Get project root
        project_root = Path(__file__).parent.parent.parent
        src_path = project_root / "src"
        sys.path.insert(0, str(src_path))
        
        # Sample mutual fund data (based on our actual processed data)
        sample_texts = [
            "HDFC Large Cap Fund invests predominantly in large cap companies with strong fundamentals and growth potential.",
            "The fund aims to generate long-term capital appreciation from a diversified portfolio of equity and equity-related securities.",
            "Investment Objective: To generate long-term capital appreciation through investments in large cap companies.",
            "Asset Allocation: 80-100% in Equity, 0-20% in Debt, 0-20% in Money Market Instruments.",
            "Risk Factors: Mutual Fund investments are subject to market risks. NAV may fluctuate due to market movements.",
            "The fund follows a bottom-up stock picking approach focusing on companies with proven track records.",
            "Minimum Investment: ₹5,000 for lump sum, ₹500 for SIP. Additional Investment: ₹1,000.",
            "Fund Manager: Mr. V S Srinivasan. Experience: 24 years in fund management.",
            "Expense Ratio: 1.25% (Direct Plan). Exit Load: 1% if redeemed within 365 days.",
            "Category: Large Cap Equity. Benchmark: NIFTY 100 TRI. Launch Date: 01-01-2010.",
            "HDFC Mid Cap Fund focuses on investing in mid cap companies with potential for growth and expansion.",
            "The scheme seeks to generate long-term capital appreciation by investing in a portfolio of mid cap stocks.",
            "Suitable for investors with long-term investment horizon and moderate to high risk appetite.",
            "Tax Benefits: ELSS funds offer tax deduction under Section 80C with 3-year lock-in period.",
            "Past performance may or may not be sustained in future. Investors should consult their financial advisors."
        ]
        
        # Test queries (typical user questions)
        test_queries = [
            "What is the investment objective of HDFC Large Cap Fund?",
            "What are the risk factors involved in mutual fund investments?",
            "What is the minimum investment amount for HDFC funds?",
            "Who is the fund manager of HDFC Large Cap Fund?",
            "What is the expense ratio for HDFC Large Cap Fund?",
            "What is the asset allocation strategy?",
            "How does HDFC Mid Cap Fund differ from Large Cap Fund?",
            "What are the tax benefits of ELSS funds?",
            "What is the exit load for HDFC funds?",
            "What is the benchmark for HDFC Large Cap Fund?"
        ]
        
        print(f"Sample texts: {len(sample_texts)}")
        print(f"Test queries: {len(test_queries)}")
        
        # Models to compare
        models_to_test = [
            {
                'name': 'all-MiniLM-L6-v2',
                'description': 'Current model - Fast, lightweight',
                'size': '23MB'
            },
            {
                'name': 'BAAI/bge-small-en-v1.5',
                'description': 'BGE Small English v1.5 - Optimized for retrieval',
                'size': '24MB'
            },
            {
                'name': 'BAAI/bge-base-en-v1.5',
                'description': 'BGE Base English v1.5 - Better performance',
                'size': '109MB'
            }
        ]
        
        results = []
        
        for model_config in models_to_test:
            print(f"\nTesting {model_config['name']}:")
            print(f"  Description: {model_config['description']}")
            print(f"  Size: {model_config['size']}")
            
            try:
                from sentence_transformers import SentenceTransformer
                
                # Load model
                start_time = time.time()
                model = SentenceTransformer(model_config['name'])
                load_time = time.time() - start_time
                print(f"  Load time: {load_time:.2f}s")
                
                # Generate embeddings for sample texts
                start_time = time.time()
                doc_embeddings = model.encode(sample_texts, batch_size=8, show_progress_bar=False)
                doc_embedding_time = time.time() - start_time
                print(f"  Document embedding time: {doc_embedding_time:.2f}s")
                print(f"  Document embedding shape: {doc_embeddings.shape}")
                
                # Generate embeddings for queries
                start_time = time.time()
                query_embeddings = model.encode(test_queries, batch_size=8, show_progress_bar=False)
                query_embedding_time = time.time() - start_time
                print(f"  Query embedding time: {query_embedding_time:.2f}s")
                print(f"  Query embedding shape: {query_embeddings.shape}")
                
                # Test retrieval quality
                from sklearn.metrics.pairwise import cosine_similarity
                
                # For each query, find best matching document
                retrieval_scores = []
                for i, query_emb in enumerate(query_embeddings):
                    similarities = cosine_similarity([query_emb], doc_embeddings)[0]
                    best_match_idx = np.argmax(similarities)
                    best_score = similarities[best_match_idx]
                    retrieval_scores.append(best_score)
                
                avg_retrieval_score = np.mean(retrieval_scores)
                print(f"  Average retrieval score: {avg_retrieval_score:.4f}")
                
                # Test embedding quality metrics
                # 1. Embedding variance (higher is better for diversity)
                embedding_variance = np.var(doc_embeddings)
                print(f"  Embedding variance: {embedding_variance:.6f}")
                
                # 2. Average similarity between documents (lower is better for diversity)
                doc_similarities = cosine_similarity(doc_embeddings)
                # Get upper triangle excluding diagonal
                upper_triangular = doc_similarities[np.triu_indices_from(doc_similarities, k=1)]
                avg_doc_similarity = np.mean(upper_triangular)
                print(f"  Average document similarity: {avg_doc_similarity:.4f}")
                
                # 3. Memory usage estimation
                embedding_memory = doc_embeddings.nbytes + query_embeddings.nbytes
                print(f"  Memory usage: {embedding_memory / (1024*1024):.2f} MB")
                
                # Store results
                result = {
                    'model': model_config['name'],
                    'description': model_config['description'],
                    'size': model_config['size'],
                    'load_time': float(load_time),
                    'doc_embedding_time': float(doc_embedding_time),
                    'query_embedding_time': float(query_embedding_time),
                    'total_embedding_time': float(doc_embedding_time + query_embedding_time),
                    'embedding_dimension': int(doc_embeddings.shape[1]),
                    'avg_retrieval_score': float(avg_retrieval_score),
                    'embedding_variance': float(embedding_variance),
                    'avg_doc_similarity': float(avg_doc_similarity),
                    'memory_usage_mb': float(embedding_memory / (1024*1024)),
                    'throughput_docs_per_sec': float(len(sample_texts) / doc_embedding_time),
                    'throughput_queries_per_sec': float(len(test_queries) / query_embedding_time)
                }
                results.append(result)
                
            except Exception as e:
                print(f"  ERROR: Failed to test {model_config['name']}: {e}")
                continue
        
        # Compare results
        if len(results) > 1:
            print(f"\n{'='*80}")
            print("MODEL COMPARISON RESULTS")
            print(f"{'='*80}")
            
            # Sort by retrieval score (primary metric)
            results.sort(key=lambda x: x['avg_retrieval_score'], reverse=True)
            
            print(f"\nRanking by Retrieval Quality:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['model']}")
                print(f"   Retrieval Score: {result['avg_retrieval_score']:.4f}")
                print(f"   Embedding Variance: {result['embedding_variance']:.6f}")
                print(f"   Document Similarity: {result['avg_doc_similarity']:.4f}")
                print(f"   Load Time: {result['load_time']:.2f}s")
                print(f"   Throughput: {result['throughput_docs_per_sec']:.1f} docs/sec")
                print(f"   Memory: {result['memory_usage_mb']:.2f} MB")
                print()
            
            # Recommendation based on our use case
            print("RECOMMENDATION ANALYSIS:")
            print("=" * 50)
            
            # Criteria weights for our mutual fund RAG system
            retrieval_weight = 0.4
            speed_weight = 0.3
            memory_weight = 0.2
            diversity_weight = 0.1
            
            # Calculate composite scores
            for result in results:
                # Normalize metrics (higher is better)
                max_retrieval = max(r['avg_retrieval_score'] for r in results)
                max_speed = max(r['throughput_docs_per_sec'] for r in results)
                min_memory = min(r['memory_usage_mb'] for r in results)
                max_variance = max(r['embedding_variance'] for r in results)
                
                norm_retrieval = result['avg_retrieval_score'] / max_retrieval
                norm_speed = result['throughput_docs_per_sec'] / max_speed
                norm_memory = min_memory / result['memory_usage_mb']  # Lower memory is better
                norm_diversity = result['embedding_variance'] / max_variance
                
                composite_score = (
                    norm_retrieval * retrieval_weight +
                    norm_speed * speed_weight +
                    norm_memory * memory_weight +
                    norm_diversity * diversity_weight
                )
                
                result['composite_score'] = composite_score
            
            # Sort by composite score
            results.sort(key=lambda x: x['composite_score'], reverse=True)
            
            print("Overall Ranking (Weighted Score):")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['model']} - Score: {result['composite_score']:.3f}")
                print(f"   Best for: ", end="")
                
                if result['avg_retrieval_score'] == max(r['avg_retrieval_score'] for r in results):
                    print("Best retrieval quality", end="")
                elif result['throughput_docs_per_sec'] == max(r['throughput_docs_per_sec'] for r in results):
                    print("Fastest processing", end="")
                elif result['memory_usage_mb'] == min(r['memory_usage_mb'] for r in results):
                    print("Lowest memory usage", end="")
                else:
                    print("Balanced performance", end="")
                
                print()
            
            # Final recommendation
            best_model = results[0]
            print(f"\nFINAL RECOMMENDATION: {best_model['model']}")
            print(f"Reason: Best overall performance for mutual fund RAG system")
            print(f"Retrieval Quality: {best_model['avg_retrieval_score']:.4f}")
            print(f"Processing Speed: {best_model['throughput_docs_per_sec']:.1f} docs/sec")
            print(f"Memory Usage: {best_model['memory_usage_mb']:.2f} MB")
            
            # Save results
            results_file = project_root / "data" / "embedding_models_comparison.json"
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nDetailed results saved to: {results_file}")
            
        else:
            print("\nERROR: Could not compare models (insufficient successful tests)")
            return 1
        
        return 0
        
    except Exception as e:
        print(f"\nERROR: Embedding models comparison failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
