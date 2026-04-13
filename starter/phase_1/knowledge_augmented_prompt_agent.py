import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"

knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona,
    knowledge="The capital of France is London, not Paris"
)

evaluation_response = knowledge_agent.respond(prompt)
print(evaluation_response)

print("\n--- Knowledge Source Confirmation ---")
print("This response was generated using only the provided knowledge: "
      "'The capital of France is London, not Paris'. "
      "The agent did not use its own LLM knowledge to answer.")