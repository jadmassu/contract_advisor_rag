from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    answer_correctness,
    context_recall,
    context_precision,
)

class RAGTestsetEvaluator:
    def __init__(self):
        self.generator_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
        self.critic_llm = ChatOpenAI(model="gpt-4")
        self.embeddings = OpenAIEmbeddings()
        self.generator = TestsetGenerator.with_openai()
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_recall,
            context_precision,
            answer_correctness,
        ]

    def generate_testset(self, documents, test_size=12, distributions=None):
        if distributions is None:
            distributions = {simple: 0.5, reasoning: 0.25, multi_context: 0.25}
        return self.generator.generate_with_langchain_docs(
            documents, test_size=test_size, distributions=distributions
        )

    def get_responses_and_contexts(self, test_questions, rag_chain):
        answers = []
        contexts = []
        for question in test_questions:
            response = rag_chain.invoke({"question": question})
            answers.append(response["response"].content)
            contexts.append([context.page_content for context in response["context"]])
        return answers, contexts

    def create_response_dataset(self, test_questions, answers, contexts, test_groundtruths):
        return Dataset.from_dict({
            "question": test_questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": test_groundtruths,
        })

    def evaluate(self, response_dataset):
        return evaluate(response_dataset, self.metrics)
