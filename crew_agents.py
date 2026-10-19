from crewai import Agent, Task, Crew, LLM
from tools import check_order_status
from guardrails import mask_pii

# 1. Connect directly to your local Ollama Llama 3.2 model
local_llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434"
)

# 2. Define the Support Agent
support_agent = Agent(
    role="Customer Support Representative",
    goal="Resolve customer inquiries quickly and accurately.",
    backstory="You are a helpful Nykaa support agent. You strictly use the order status tool to find information before answering.",
    llm=local_llm, 
    tools=[check_order_status], # <-- THIS IS THE NEW LINE
    allow_delegation=False
)

# 3. Define the Escalation Agent
escalation_agent = Agent(
    role="Escalation Manager",
    goal="Handle highly delayed orders.",
    backstory="You are a senior manager stepping in for difficult or delayed cases.",
    llm=local_llm, 
    allow_delegation=False
)

# 4. Define the core Task
process_inquiry = Task(
    description="Review the customer's inquiry: {customer_query}. Provide a resolution.",
    expected_output="A final response resolving the query.",
    agent=support_agent
)

# 5. Assemble the Crew
ecommerce_crew = Crew(
    agents=[support_agent, escalation_agent],
    tasks=[process_inquiry],
    verbose=True
)

if __name__ == "__main__":
    raw_input = "What is the status of ORD-100001? Call me at 9876543210."
    print("--- 1. Original Input ---")
    print(raw_input)
    
    safe_input = mask_pii(raw_input)
    print("\n--- 2. Guardrail Applied ---")
    print(safe_input)
    
    print("\n--- 3. CrewAI Execution ---")
    result = ecommerce_crew.kickoff(inputs={'customer_query': safe_input})
    print("\n--- 4. Final Output ---")
    print(result)
