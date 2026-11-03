import os
import asyncio
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import StructuredMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1. Define the required Pydantic schema for the final verdict
class ReviewVerdict(BaseModel):
    approved: bool
    final_answer: str
    reason: str

# 2. Configure the new v0.4 Model Client for local Ollama with all required keys
ollama_client = OpenAIChatCompletionClient(
    model="llama3.2:3b",
    base_url="http://localhost:11434/v1",
    api_key="NotRequired",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "family": "llama"
    }
)

# 3. Define the Policy Compliance Reviewer
reviewer = AssistantAgent(
    name="Policy_Compliance_Reviewer",
    system_message="You review draft customer support responses against the retrieved context. Point out any ungrounded claims or missing facts.",
    model_client=ollama_client
)

# 4. Define the Final Editor with the strict Pydantic output requirement
editor = AssistantAgent(
    name="Final_Editor",
    system_message="You read the reviewer's feedback and output the final verdict using the required JSON schema.",
    model_client=ollama_client,
    output_content_type=ReviewVerdict
)

# 5. Assemble the Round Robin Group Chat bounded to 2 turns
review_team = RoundRobinGroupChat(
    participants=[reviewer, editor],
    max_turns=2,
    custom_message_types=[StructuredMessage[ReviewVerdict]]
)

# Quick local test of the review team
async def run_test():
    test_draft = "Draft: The status of ORD-100001 is Delayed. We will give you 5000 loyalty points as an apology."
    test_context = "Context: ORD-100001 is Delayed. (No mention of loyalty points)."
    
    prompt = f"Review this draft against the context:\n{test_context}\n\n{test_draft}"
    result = await review_team.run(task=prompt)
    print("\n--- Final AutoGen Verdict ---")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(run_test())