"""
Pinecone RAG: Retrieve context from Pinecone and build LLM prompt
"""
from app.services.pinecone_client import pinecone_index
from app.services.openai_service import get_embedding, generate_reply

# Retrieve top-k context from Pinecone
def retrieve_context_from_pinecone(query, namespace="kb", top_k=5):
    emb = get_embedding(query)
    res = pinecone_index.query(vector=emb, top_k=top_k, include_metadata=True, namespace=namespace)
    contexts = []
    for match in res.matches:
        meta = match.metadata
        text = meta.get("content") or meta.get("answer") or meta.get("title") or ""
        contexts.append(text)
    return contexts

def build_rag_prompt(user_message, contexts):
    context_block = "\n\n---\n\n".join(contexts)
    prompt = f"You are a helpful assistant. Use the following context to answer the question.\n\nContext:\n{context_block}\n\nQuestion: {user_message}\nAnswer:"
    return prompt

def answer_with_rag(user_message, namespace="kb", top_k=5):
    contexts = retrieve_context_from_pinecone(user_message, namespace=namespace, top_k=top_k)
    prompt = build_rag_prompt(user_message, contexts)
    return generate_reply(prompt)
