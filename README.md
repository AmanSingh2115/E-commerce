# E-commerce AI Support Agent (Nykaa)

**Track:** Nykaa (E-commerce & Retail)

A production-grade e-commerce AI support agent built with CrewAI, AutoGen, and FastAPI. Features a ChromaDB RAG pipeline for Nykaa policies, real-time order lookups, PII guardrails, and a multi-agent QA review stage. Includes a deployable backend and zero-network mock LLM evaluation.

### Mandatory Grading Confirmations
* **Environment:** This entire system runs under `MOCK_LLM` / local `llama3.2:3b` using Ollama with strictly zero API keys and zero outbound network access. 
* **Telemetry:** CrewAI telemetry has been explicitly disabled via `os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"`.
* **Dataset Design (Task 1):** The deterministic dataset generator uses seed 42, an amount range of ₹500 - ₹15,000, and equal weighting across all categories and statuses.
* **RAG Threshold (Task 4):** Based on empirical testing, the measured distance score for in-scope queries was ~0.85. The "I don't know" fallback distance threshold is strictly set to 1.10 to block out-of-scope hallucinations.

---

### AI Governance & Risk Assessment (Task 15)

**Principle of Least Autonomy:** 
The system strictly enforces least autonomy through architectural tool isolation. In the CrewAI setup, only the Lookup Agent is explicitly instantiated with `tools=[check_order_status]`. The RAG Agent and the Final Composer Agent do not have this tool in their arrays. Because tools are scoped strictly to individual agents rather than the global crew, it is physically impossible for the composer or retriever to execute unauthorized database queries.

**System Risk Classification: Medium Risk**
This capstone operates at a Medium Risk level. It automates customer support tasks and processes pseudo-PII (like phone numbers, which are masked by guardrails) and order data. While an error could cause customer frustration, the system does not make High-Risk determinations (e.g., medical diagnoses, financial lending, or automated hiring), nor is it purely Low-Risk (e.g., generic summarization without external data impact).