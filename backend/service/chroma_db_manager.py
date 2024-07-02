from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import chromadb
class ChromaDBManager:
    def __init__(self, persist_directory='./data',):
        self.persist_directory = persist_directory
        self.db = None
   

    def store_and_load_chroma_db(self, docs):
        try:
            embedding_function = OpenAIEmbeddings(  model="text-embedding-ada-002")
            persistent_client = chromadb.PersistentClient()
            # Store and load Chroma DB from disk
            self.db = Chroma.from_documents(docs, embedding_function,collection_name="biography", persist_directory=self.persist_directory,client=persistent_client)
            return self.db
        except Exception as e:
            raise RuntimeError(f"An error occurred while storing and loading Chroma DB: {e}")

    def search_chroma_db(self,  query):
        try:
            # Perform similarity search
            docs = self.db.similarity_search(query)
            return docs
        except Exception as e:
            raise RuntimeError(f"An error occurred while querying Chroma DB: {e}")
        
    
    def search_chroma_db_with_score(self,  query):
        try:
            # Perform similarity search
            docs = self.db.similarity_search_with_score(query)
            # augmented_input = query + " ".join(retrieved_docs)

            # # Use ChatGPT (or another LLM) to generate response
            # response = chatgpt.generate(augmented_input) 
           
            return docs
        except Exception as e:
            raise RuntimeError(f"An error occurred while querying Chroma DB: {e}")


    def update_document_metadata(self,  doc_id, metadata):
        try:
            # Update metadata for a document
            self.db.update_document(doc_id, metadata)
            print("Metadata updated successfully.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while updating document metadata: {e}")

    def delete_document(self,  doc_id):
        try:
            # Delete document
            self.db._collection.delete(ids=[doc_id])
            print("Document deleted successfully.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while deleting document: {e}")

