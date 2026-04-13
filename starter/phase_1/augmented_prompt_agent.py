# TODO: 1 - Import the AugmentedPromptAgent class
from workflow_agents.base_agents import AugmentedPromptAgent 
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# TODO: 2 - Instantiate an object of AugmentedPromptAgent with the required parameters
augmented_agent = AugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona
)

# TODO: 3 - Send the 'prompt' to the agent and store the response in a variable named 'augmented_agent_response'
augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# TODO: 4 - Add a comment explaining:
# - What knowledge the agent likely used to answer the prompt.
# - How the system prompt specifying the persona affected the agent's response.
# The agent likely used its general knowledge about world capitals to answer the prompt. 
# The system prompt specifying the persona as a college professor influenced the agent to respond in a more formal and educational tone, 
# starting with "Dear students," which is characteristic of how a professor might address their students.
print("\n--- Knowledge Source ---")
print("The agent uses the LLM's general pre-trained knowledge. "
      "It does not have access to external documents or provided knowledge.")

print("\n--- Persona Impact ---")
print("By specifying the persona in the system message, the agent adopts "
      "that role consistently, producing responses with a different tone, "
      "style, and focus compared to a direct prompt without a persona.")