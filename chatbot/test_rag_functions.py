#!/usr/bin/env python3
"""
Test RAG functions independently to verify they work correctly
"""

from sentence_transformers import SentenceTransformer
import chromadb
from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks for better RAG performance"""
    if not text or len(text.strip()) == 0:
        return []
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.strip()) > 50:  # Only include substantial chunks
            chunks.append(chunk.strip())
    
    return chunks

def test_rag_functions():
    """Test RAG chunking and vector search functions"""
    print("🧪 Testing RAG Functions...")
    
    # Test sample content
    sample_content = """
    Wolf AI Product Catalog
    
    Strategic Planning Assistant
    Features: SWOT analysis, competitive intelligence, market research
    Pricing: $99 per month per user
    Benefits: Reduces planning time by 60%, improves decision accuracy
    
    Financial Analytics Pro
    Features: ROI calculations, budget forecasting, cost analysis
    Pricing: $149 per month per organization
    Benefits: Real-time financial insights, automated reporting
    
    Customer Retention Platform
    Features: Customer behavior analysis, retention campaigns
    Pricing: $199 per month plus usage fees
    Benefits: Increases customer lifetime value by 40%
    """
    
    # Test chunking
    print("\n📄 Testing text chunking...")
    chunks = chunk_text(sample_content, chunk_size=100, overlap=20)
    print(f"✅ Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
        print(f"  Chunk {i+1}: {chunk[:80]}...")
    
    # Test RAG system
    print("\n🧠 Testing RAG vector search...")
    try:
        # Initialize components
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        chroma_client = chromadb.Client()
        
        # Create collection
        try:
            chroma_client.delete_collection(name="test_documents")
        except:
            pass
            
        collection = chroma_client.create_collection(name="test_documents")
        
        # Generate embeddings
        embeddings = embedding_model.encode(chunks).tolist()
        
        # Add to vector store
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"chunk_index": i} for i in range(len(chunks))]
        
        collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Vector store created with {len(chunks)} chunks")
        
        # Test search queries
        test_queries = [
            "What is the pricing for Strategic Planning Assistant?",
            "Tell me about Financial Analytics features",
            "Customer retention benefits"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            
            # Generate query embedding
            query_embedding = embedding_model.encode([query]).tolist()
            
            # Search
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=2,
                include=["documents", "distances"]
            )
            
            if results['documents'] and len(results['documents']) > 0:
                print(f"✅ Found {len(results['documents'][0])} relevant chunks:")
                for i, doc in enumerate(results['documents'][0]):
                    distance = results['distances'][0][i] if results['distances'] else 'N/A'
                    print(f"  📄 Result {i+1} (similarity: {1-distance:.3f}): {doc[:100]}...")
            else:
                print("❌ No results found")
        
        print("\n✅ RAG functions test completed successfully!")
        
    except Exception as e:
        print(f"❌ RAG test failed: {e}")

if __name__ == "__main__":
    test_rag_functions()
