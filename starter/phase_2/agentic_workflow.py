# agentic_workflow.py

from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
import os
from dotenv import load_dotenv
 
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 

# load the product spec
with open("Product-Spec-Email-Router.txt", "r") as f:
    product_spec = f.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. " 
    + product_spec
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager,
    knowledge=knowledge_product_manager
)

# Product Manager - Evaluation Agent
# This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_product_manager = "The answer should be user stories that follow this exact structure: " \
                      "As a [type of user], I want [an action or feature] so that [benefit/value]."
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager_eval,
    evaluation_criteria=evaluation_criteria_product_manager,
    worker_agent=product_manager_knowledge_agent 
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

 
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria="The answer should be product features that follow the following structure: " \
                      "Feature Name: A clear, concise title that identifies the capability\n" \
                      "Description: A brief explanation of what the feature does and its purpose\n" \
                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
                      "User Benefit: How this feature creates value for the user",
    worker_agent=None  # This will be set to the program_manager_knowledge_agent after its instantiation
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story." 
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer
)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents." 
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria="The answer should be tasks following this exact structure: " \
                      "Task ID: A unique identifier for tracking purposes\n" \
                      "Task Title: Brief description of the specific development work\n" \
                      "Related User Story: Reference to the parent user story\n" \
                      "Description: Detailed explanation of the technical work required\n" \
                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
                      "Estimated Effort: Time or complexity estimation\n" \
                      "Dependencies: Any tasks that must be completed first",
    worker_agent=development_engineer_knowledge_agent
)


# Routing Agent - This agent will route the workflow steps to the appropriate support function (product manager, program manager, or development engineer).
def product_manager_support_function(query):
    """Routes to Product Manager: generates & evaluates user stories."""
    result = product_manager_evaluation_agent.evaluate(query)
    return result["final_response"]
 
 
def program_manager_support_function(query):
    """Routes to Program Manager: generates & evaluates product features."""
    result = program_manager_evaluation_agent.evaluate(query)
    return result["final_response"]
 
 
def development_engineer_support_function(query):
    """Routes to Dev Engineer: generates & evaluates development tasks."""
    result = development_engineer_evaluation_agent.evaluate(query)
    return result["final_response"]



routing_agent = [
    {
        "name": "product manager agent",
        "description": "Agent responsible for defining user stories based on the product specification.",
        "func": product_manager_support_function
    },
    {
        "name": "program manager agent",
        "description": "Agent responsible for defining product features by organizing user stories.",
        "func": program_manager_support_function
    },
    {
        "name": "development engineer agent",
        "description": "Agent responsible for defining development tasks based on user stories.",
        "func": development_engineer_support_function
    }
]
routing_agent = RoutingAgent(openai_api_key=openai_api_key, agents=routing_agent)


# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "What would the development tasks for this product be?"
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).
workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
print(f"\nExtracted {len(workflow_steps)} workflow steps:")
for idx, step in enumerate(workflow_steps, 1):
    print(f"  {idx}. {step}")
 
# Step 2 – initialize completed steps list
completed_steps = []
 
# Step 3 – loop through steps and route each one
for idx, step in enumerate(workflow_steps, 1):
    if not step.strip():
        continue  # skip empty lines
 
    print(f"\n{'='*60}")
    print(f"Executing step {idx}: {step}")
    print(f"{'='*60}")
 
    result = routing_agent.route(step)
    completed_steps.append(result)
 
    print(f"\n✅ Step {idx} result:\n{result}")
 
# Step 4 – print the final output (last completed step)
print(f"\n{'='*60}")
print("*** Workflow complete ***")
print(f"{'='*60}")
if completed_steps:
    print("\nFinal workflow output (last completed step):")
    print(completed_steps[-1])