from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class ParaphrasedQuery(BaseModel):
    """You have performed query expansion to generate a paraphrasing of a question."""
    paraphrased_query: str = Field(
        ...,
        description="A unique paraphrasing of the original question.",
    )

class QueryAnalyzer:
    def __init__(self, model_name="gpt-3.5-turbo-0125", temperature=0):
        self.system_message = """You are an expert at converting user questions into database queries. \
        You have access to a database of tutorial videos about a software library for building LLM-powered applications. \
        Perform query expansion. If there are multiple common ways of phrasing a user question \
        or common synonyms for key words in the question, make sure to return multiple versions \
        of the query with the different phrasings. If there are acronyms or words you are not familiar with, do not try to rephrase them. \
        Return at least 3 versions of the question."""
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),
                ("human", "{question}"),
            ]
        )
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.llm_with_tools = self.llm.bind_tools([ParaphrasedQuery])
        self.query_analyzer = self.prompt | self.llm_with_tools | PydanticToolsParser(tools=[ParaphrasedQuery])

    def analyze_query(self, question: str):
        return self.query_analyzer.invoke({"question": question})

