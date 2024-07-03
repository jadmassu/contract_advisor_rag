import os
import sys
import json
sys.path.insert(0, '/home/miki/Precision_RAG')
from openai import OpenAI

import numpy as np
# from data_generation._data_generation import file_reader
from dotenv import find_dotenv, load_dotenv
import numpy as np

env_file_path = find_dotenv(raise_error_if_not_found=True)
load_dotenv(env_file_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)



def get_completion(messages):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages= [messages],
        max_tokens = 500,
        temperature=0,
)
    return response

def evaluate(prompt, questions, context ) -> str:
  
    response = get_completion(
        [
            {
                "role": "system", 
                "content": prompt.replace("{Context}", context).replace("{Question}", questions)
            }
        ],
       
    )
    
    print(response)
    system_msg = str(response.choices[0].message.content)

    for logprob in response.choices[0].logprobs.content[0].top_logprobs:
       result = classify_response(system_msg, logprob)
    return result



def classify_response(system_msg, logprob):
    """Classify the response based on system message and log probability."""
    accuracy = np.round(np.exp(logprob.logprob) * 100, 2)
    output = f'\nhas_sufficient_context_for_answer: {system_msg}, \nlogprobs: {logprob.logprob}, \naccuracy: {accuracy}%\n'
    print(output)
    
    if system_msg == 'true' and accuracy >= 95.00:
        classification = 'true'
    elif system_msg == 'false' and accuracy >= 95.00:
        classification = 'false'
    else:
        classification = 'false'

    return {'classification': classification, 'accuracy': f'{accuracy}%'}




