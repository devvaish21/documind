from utils.vector_store import get_relevant_chunks

test_queries = [
    "What is the leave application process?",
    "How do I escalate a customer complaint?",
    "What are the data privacy rules?",
    "Steps to onboard a new employee",
    "Who approves expense reimbursement?"
]

print("=" * 60)
print("DocuMind RAG Pipeline — Retrieval Test (HuggingFace)")
print("=" * 60)

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    results = get_relevant_chunks(query, k=2)
    for i, doc in enumerate(results, 1):
        print(f"\n  Result {i}:")
        print(f"  Source: {doc.metadata}")
        print(f"  Text:   {doc.page_content[:150]}...")