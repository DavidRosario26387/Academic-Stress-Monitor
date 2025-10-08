import chromadb
import uuid
import pandas as pd

collection = None  # global placeholder

def setup_rag(csv_path="rags.csv"):
    global collection
    if collection is not None:
        return collection  # already initialized

    df = pd.read_csv(csv_path, encoding="latin-1")
    chroma_client = chromadb.PersistentClient('vectorstore')
    collection = chroma_client.get_or_create_collection(name="rag_content")

    if not collection.count():
        for _, row in df.iterrows():
            collection.add(
            documents=[row["Issue"]],
            metadatas=[{"Recommondation": row["Recommondation"]}],
            ids=[str(uuid.uuid4())]
        )

    return collection

def rag_query(text,n):
    """
    Query the RAG database for relevant recommendations.

    Args:
        text (str): User input message.
        n (int): Number of results to fetch.

    Returns:
        str: Recommendations formatted as numbered list.
    """
    x=collection.query(query_texts=[text],n_results=n).get("metadatas",[])
    res=""
    if x and x[0]:
        for i, rec in enumerate(x[0], 1):
            res+=f"{i}. {rec['Recommondation']}\n"
    else:
        res="No relevant measures found in RAG, Give your own Recommondation"
    return res.strip()
