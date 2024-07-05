import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from service.file_processor import FileProcessor
from service.chroma_db_manager import ChromaDBManager
from service.rag_processor import RAGProcessor
from service.ragas import RAGTestsetEvaluator

load_dotenv()

class Controller:
    def __init__(self):
        self.llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.file_path = os.getenv("PATH_TO_TXT")
        self.rag_processor = None
        self.response_prompt = None
        self.user_prompt = None
        self.file = None

    def generate_prompt(self, prompt):
        try:
       
            self.user_prompt = prompt
            res = self.rag_processor.invoker(prompt)
            self.prompt = res["response"].content
            return self.prompt
        except Exception as e:
            raise RuntimeError(f"error: {e}")

    def init_process(self):
        try:
            self.file = FileProcessor(self.file_path)
            self.file.load_file()
            sp = file.split_file()
       
            chroma = ChromaDBManager()
            chromadb = chroma.store_and_load_chroma_db(sp)
            self.rag_processor = RAGProcessor(self.llm)
            rag = self.rag_processor.create_rag(chromadb)
      
            self.rag_processor.process_rag_chain()
        except Exception as e:
            raise RuntimeError(f"error: {e}")

    def evaluate(self):
        try:
            eval = RAGTestsetEvaluator()
            eval.evaluate(self.file)
        except Exception as e:
            raise RuntimeError(f"error: {e}")