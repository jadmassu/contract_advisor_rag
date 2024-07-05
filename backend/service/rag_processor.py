from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

from backend.service.query_analysis import QueryAnalyzer
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere
from langchain.chains import RetrievalQA
class RAGProcessor:
    def __init__(self,  llm):
   
        self.llm = llm
        self.rag = None
        self.rag_chain = None
        self.reRank = None

    def create_rag(self,vector_db):
        try:
            self.rag = vector_db.as_retriever(
                search_type="similarity_score_threshold", 
                search_kwargs={"score_threshold": 0.5}
            )
            return self.rag
        except Exception as e:
            raise RuntimeError(f"An error occurred while creating RAG: {e}")

    def generate_prompt_template(self):
        try:
            template = """
                You are an AI assistant specializing in providing detailed and accurate answers based on the provided context documents. 
                Your task is to understand the user's question, retrieve the most relevant information from the context documents, 
                and generate a well-informed and concise response. Use the information from the documents to support your answers.

                Instructions:
                1. Always prioritize information from the provided context documents.
                2. If the context documents do not contain the required information, acknowledge it and provide a general answer based on your training data.
                3. Ensure your responses are clear, concise, and relevant to the user's question.
                4. If there are multiple relevant points, structure your response in a logical order. please respond with 'I don't know':
                {question}
                Context:
                {context}
                 """

            prompt = ChatPromptTemplate.from_messages([("human", template)])
            return prompt
        except Exception as e:
            raise RuntimeError(f"An error occurred while generating response: {e}")

    def process_rag_chain(self,query_analyzer ):
        try:
            if self.rag is None:
                raise RuntimeError("RAG retriever is not initialized. Please create RAG first.")

            
           
            self.rag_chain = (
                {"context": itemgetter("question") | self.rag, "question": itemgetter("question")|  query_analyzer.get("query_analyzer")}
                | RunnablePassthrough.assign(context=itemgetter("context"))
                | {"response": self.generate_prompt_template() | self.llm, "context": itemgetter("context")}
            )
            
            
            return  self.rag_chain
        except Exception as e:
            raise RuntimeError(f"An error occurred while processing RAG chain: {e}")
    def reRank(self):
        try:
            if self.rag_chain is None:
                raise RuntimeError("RAG chain is not initialized. Please process RAG chain first.")
           
            compressor = CohereRerank()
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=self.rag_chain
            )
            self.reRank = RetrievalQA.from_chain_type(
            llm=Cohere(temperature=0), retriever=compression_retriever
            )
            return self.reRank 
        except Exception as e:
            raise RuntimeError(f"An error occurred while reRank: {e}")

    def invoker(self, question):
        try:
            if self.reRank is None:
                raise RuntimeError("RAG chain is not initialized. Please process RAG chain first.")
            query_analyzer = QueryAnalyzer()
            result = query_analyzer.analyze_query(question)
            
            return self.reRank.invoke({"question": question,query_analyzer: result })
        except Exception as e:
            raise RuntimeError(f"An error occurred while invoking the chain: {e}")
