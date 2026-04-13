#evaluation_agent.py
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, EvaluationAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")
prompt = "What is the capital of France?"

# Parameters for the Knowledge Agent
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capitol of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona, knowledge=knowledge)

# Parameters for the Evaluation Agent
persona = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
evaluation_agent = EvaluationAgent(openai_api_key=openai_api_key, persona=persona, evaluation_criteria=evaluation_criteria, worker_agent=knowledge_agent, max_interactions=10)
 
print(f"Prompt: {prompt}\n")
evaluation_response = evaluation_agent.evaluate(prompt)
 
print("\n--- Final Result ---")
print(f"Final Response : {evaluation_response['final_response']}")
print(f"Evaluation     : {evaluation_response['evaluation']}")
print(f"Iterations     : {evaluation_response['iterations']}")