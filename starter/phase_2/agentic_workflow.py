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

worker_agent=product_manager_knowledge_agent 
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager_eval,
    evaluation_criteria=evaluation_criteria_product_manager,
    worker_agent=product_manager_knowledge_agent,
    max_interactions=3
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups." 
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager,
    knowledge=knowledge_program_manager
)

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
    worker_agent=program_manager_knowledge_agent , # This will be set to the program_manager_knowledge_agent after its instantiation
    max_interactions=3
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story." 
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer
)

persona_dev_engineer_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)
evaluation_criteria_dev_engineer = (
    "The answer should be tasks following this exact structure: "
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
)
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria=evaluation_criteria_dev_engineer,
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=3
) 

# Routing Agent - This agent will route the workflow steps to the appropriate support function (product manager, program manager, or development engineer).
def product_manager_support_function(query):
    """
    1. KnowledgeAugmentedPromptAgent generates user stories.
    2. EvaluationAgent validates / refines iteratively.
    3. Returns the final validated response.
    """
    # Step 1: generate initial response from knowledge agent
    knowledge_response = product_manager_knowledge_agent.respond(query)
    print(f"\n[PM Knowledge Agent]\n{knowledge_response}")
 
    # Step 2: evaluate and refine — the evaluator's worker_agent will handle
    # corrections if the initial response doesn't meet the criteria
    result = product_manager_evaluation_agent.evaluate(query)
    return result["final_response"]
 
 
def program_manager_support_function(query):
    """
    1. KnowledgeAugmentedPromptAgent generates product features.
    2. EvaluationAgent validates / refines iteratively.
    3. Returns the final validated response.
    """
    # Step 1: generate initial response from knowledge agent
    knowledge_response = program_manager_knowledge_agent.respond(query)
    print(f"\n[PgM Knowledge Agent]\n{knowledge_response}")
 
    # Step 2: evaluate and refine
    result = program_manager_evaluation_agent.evaluate(query)
    return result["final_response"]
 
 
def development_engineer_support_function(query):
    """
    1. KnowledgeAugmentedPromptAgent generates engineering tasks.
    2. EvaluationAgent validates / refines iteratively.
    3. Returns the final validated response.
    """
    # Step 1: generate initial response from knowledge agent
    knowledge_response = development_engineer_knowledge_agent.respond(query)
    print(f"\n[Dev Engineer Knowledge Agent]\n{knowledge_response}")
 
    # Step 2: evaluate and refine
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
 
workflow_prompt = (
    "Create a comprehensive project plan for the Email Router product. "
    "The plan must include: "
    "1. User stories defined from the product spec. "
    "2. Product features grouped from the user stories. "
    "3. Development tasks for each user story."
)
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")
print("\nDefining workflow steps from the workflow prompt")
 
workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
print(f"\nExtracted {len(workflow_steps)} workflow steps:")
for idx, step in enumerate(workflow_steps, 1):
    print(f"  {idx}. {step}")

email_router_prompt = (
    "Based on the Email Router product specification, which describes an AI-powered "
    "system that automatically classifies, routes, and manages incoming emails using "
    "NLP and machine learning, please provide the required output."
)
print(f"\n{'='*60}")
print("Generating User Stories (Product Manager)...")
print(f"{'='*60}")
user_stories_output = product_manager_support_function(email_router_prompt)
 
print(f"\n{'='*60}")
print("Generating Product Features (Program Manager)...")
print(f"{'='*60}")
product_features_output = program_manager_support_function(email_router_prompt)
 
print(f"\n{'='*60}")
print("Generating Development Tasks (Development Engineer)...")
print(f"{'='*60}")
development_tasks_output = development_engineer_support_function(email_router_prompt)
 

final_output = {
    "user_stories": user_stories_output,
    "product_features": product_features_output,
    "development_tasks": development_tasks_output,
}
 
print(f"\n{'='*60}")
print("*** Final Email Router Project Plan ***")
print(f"{'='*60}")
for section, content in final_output.items():
    print(f"\n{section.upper().replace('_', ' ')}:")
    print(f"{'-'*40}")
    print(content)