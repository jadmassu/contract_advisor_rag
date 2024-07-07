import os, sys
from autogen import AssistantAgent, UserProxyAgent,agentchat
from dotenv import load_dotenv
rpath = os.path.abspath('/home/user/Documents/10/w11/contract_advisor_rag')

if rpath not in sys.path:
    sys.path.insert(0, rpath)
load_dotenv()

from backend.service.chroma_db_manager import ChromaDBManager
from backend.service.rag_processor import RAGProcessor
from backend.controller import Controller as controller

class AssistantAgentManager:
    def __init__(self, llm_config):
        self.llm_config = llm_config
        try:
            self.assistant_agent = self.create_assistant_agent()
            self.worker_agent = self.create_worker_agent()
            self.user_proxy = self.create_user_proxy()
            self.groupchat = self.create_groupchat()
            self.manager = self.create_manager()
        except Exception as e:
            print(f"Initialization error: {e}")

    def create_assistant_agent(self):
        try:
            assistant_agent = AssistantAgent(assistant, llm_config=self.llm_config)
            assistant_agent.register_function(
                function_map={
                    "init_process_ext": self.init_process_ext,
                }
            )
            return assistant_agent
        except Exception as e:
            print(f"Error creating assistant agent: {e}")
            return None

    def create_worker_agent(self):
        try:
            worker_agent = AssistantAgent(worker, llm_config=self.llm_config)
            worker_agent.register_function(
                function_map={
                    "prompte_ext": self.prompte_ext,
                    "evaluation_ext": self.evaluation_ext,
                }
            )
            return worker_agent
        except Exception as e:
            print(f"Error creating worker agent: {e}")
            return None

    def create_user_proxy(self):
        try:
            return UserProxyAgent("user_proxy", code_execution_config=False)
        except Exception as e:
            print(f"Error creating user proxy agent: {e}")
            return None

    def create_groupchat(self):
        try:
            return autogen.GroupChat(
                agents=[self.user_proxy, self.assistant_agent, self.worker_agent],
                messages=[],
                max_round=50
            )
        except Exception as e:
            print(f"Error creating group chat: {e}")
            return None

    def create_manager(self):
        try:
            return autogen.GroupChatManager(
                groupchat=self.groupchat,
                llm_config=self.llm_config
            )
        except Exception as e:
            print(f"Error creating group chat manager: {e}")
            return None

    def init_process_ext(self):
        try:
            return controller.init_process()
        except Exception as e:
            print(f"Error in init_process_ext: {e}")
            return None

    def prompte_ext(self):
        try:
            return controller.generate_prompt()
        except Exception as e:
            print(f"Error in prompte_ext: {e}")
            return None

    def evaluation_ext(self):
        try:
            return controller.evaluate()
        except Exception as e:
            print(f"Error in evaluation_ext: {e}")
            return None

    def initiate_chat(self, message):
        try:
            self.user_proxy.initiate_chat(self.manager, message=message)
        except Exception as e:
            print(f"Error initiating chat: {e}")

