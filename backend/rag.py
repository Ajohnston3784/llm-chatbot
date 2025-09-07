
import os
import logging
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Directory where the vectorstore will be persisted
VECTOR_DIR = os.getenv("VECTOR_DIR", "./vectorstore")

# Initialize embeddings and Chroma vectorstore
try:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    logging.info(f"Creating Chroma vectorstore at {VECTOR_DIR}...")

    vectorstore = Chroma(collection_name="docs", embedding_function=embeddings, persist_directory=VECTOR_DIR)
    logging.info("Chroma vectorstore created.")

    # Create a retriever for similarity search
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
except Exception as e:
    logging.error(f"Error initializing vectorstore or embeddings: {e}")
    raise

# Initialize the language model
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define a custom prompt template for a more direct RAG pipeline
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that provides detailed answers based on the given context.

CONTEXT:
{context}

USER QUESTION:
{question}

YOUR TASK:
- Provide a comprehensive and helpful answer to the question using ONLY the information from the context.
- If the context doesn't contain enough information to answer fully, say so clearly.
- Use a conversational, friendly tone.
- Include specific details from the context.
- Do not make up information or include information not in the context.
- Format your answer nicely using markdown if appropriate.

YOUR ANSWER:
""")

# Create a more direct and reliable RAG pipeline
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


# Split documents into chunks and add metadata for traceability
def chunk_documents(documents, chunk_size=500, chunk_overlap=100):
    try:
        logging.info(f"Chunking {len(documents)} documents")
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        all_chunks = []
        for doc in documents:
            # Extract metadata from doc or set defaults
            filename = doc.metadata.get("source", "unknown") if hasattr(doc, "metadata") else "unknown"
            source = doc.metadata.get("source", filename) if hasattr(doc, "metadata") else filename
            date = doc.metadata.get("date", datetime.now().isoformat()) if hasattr(doc, "metadata") else datetime.now().isoformat()
            
            # Split and add page number metadata
            chunks = splitter.split_documents([doc])
            total_pages = len(chunks)

            for i, chunk in enumerate(chunks):
                # Ensure each chunk has its own metadata
                chunk.metadata = dict(chunk.metadata) if hasattr(chunk, "metadata") else {}
                chunk.metadata["source"] = source
                chunk.metadata["filename"] = filename
                chunk.metadata["date"] = date
                chunk.metadata["page_number"] = f"{i+1} of {total_pages}"
            all_chunks.extend(chunks)

        logging.info(f"Chunked into {len(all_chunks)} total chunks.")
        return all_chunks
    except Exception as e:
        logging.error(f"Error during chunking: {e}")
        raise

# Ingest documents into the vectorstore
def ingest_docs(documents, chunk_size=500, chunk_overlap=100, batch_size=50):
    try:
        logging.info("Starting document ingestion...")
        all_chunks = chunk_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        total_chunks = len(all_chunks)

        for i in range(0, total_chunks, batch_size):
            batch = all_chunks[i:i+batch_size]
            vectorstore.add_documents(batch)
            logging.info(f"Added batch {i//batch_size + 1} ({len(batch)} chunks)")
        
        logging.info(f"Ingested {len(documents)} documents, split into {total_chunks} chunks.")
    except Exception as e:
        logging.error(f"Error during document ingestion: {e}")
        raise

# Query the vectorstore and return the answer and sources
def query_docs(query: str):
    try:
        logging.info(f"Querying vectorstore with: {query}")
        
        # Retrieve relevant documents using the recommended .invoke() method
        docs = retriever.invoke(query)
        logging.info(f"Retrieved {len(docs)} documents")
        
        # Log document contents for debugging
        for i, doc in enumerate(docs):
            content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            logging.info(f"Document {i+1}: {content_preview}")
            logging.info(f"Metadata: {doc.metadata}")
        
        if not docs:
            answer = "I couldn't find any relevant information in the documents. Please try asking a different question."
            sources = []
        else:
            # Use our new RAG pipeline
            answer = rag_chain.invoke(query)
            sources = [doc.metadata.get("source", "unknown") for doc in docs]
        
        # Ensure we have an answer
        if not answer or answer.strip() == "":
            answer = "I couldn't generate a specific answer based on the documents. Please try asking in a different way."
            logging.warning(f"Empty answer returned for query: {query}")
        
        logging.info(f"Answer (first 100 chars): {answer[:100]}...")
        logging.info(f"Sources: {sources}")
        
        return answer, sources
    except Exception as e:
        logging.error(f"Error during query: {e}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        # Return a fallback answer when an error occurs
        return "I encountered an error processing your question. Please try again or rephrase your question.", []
