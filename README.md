# enterprise-banking-ai-assistant

## Overview

Enterprise Banking AI Assistant is an Agentic AI-powered customer support platform designed for banking environments. The application leverages Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), LangGraph workflows, Human-in-the-Loop (HITL) approval mechanisms, and MCP-based tool integration to provide intelligent and secure customer support.

The system enables users to query banking policies, retrieve information from uploaded documents, manage customer complaints, maintain conversational context, and execute banking support workflows through AI-driven agents.

---

## Key Features

### Agentic AI Workflow

* LangGraph-based multi-agent orchestration
* Intelligent query routing
* Tool execution workflows
* Response generation pipelines

### Retrieval-Augmented Generation (RAG)

* FAISS vector database
* Hybrid retrieval architecture
* Context-aware document search
* Source-grounded responses

### Conversational Memory

* Session memory management
* Dialogue state tracking
* Context preservation across interactions

### Human-in-the-Loop (HITL)

* Approval workflows for sensitive operations
* Risk-based escalation mechanisms
* Human review checkpoints

### MCP Integration

* Tool registry architecture
* MCP-compatible tool adapters
* Extensible external service integration

### Complaint Management

* Complaint creation and tracking
* Status monitoring
* Customer support workflows

### Security & Access Control

* Role-based access management
* Authentication and authorization
* Secure API architecture

### Evaluation Framework

* Regression testing suite
* Custom evaluation metrics
* Performance monitoring

---

## Technology Stack

### AI & LLM Frameworks

* LangChain
* LangGraph
* OpenAI
* Anthropic

### Backend

* Python
* FastAPI

### Frontend

* Streamlit

### Retrieval & Search

* FAISS
* Hybrid Search

### Document Processing

* PDF Processing
* OCR Support

### Agent Components

* MCP
* HITL
* Conversational Memory
* Tool Calling

### Deployment

* Docker
* Docker Compose

---

## Project Architecture

User Query
→ LangGraph Router
→ Memory Retrieval
→ RAG Retrieval
→ Tool Execution
→ HITL Validation
→ Response Generation
→ User Response

---

## Folder Structure

```text
app/
app_tools/
chains/
graph/
memory/
mcp/
hitl/
callbacks/
eval/
config/
docker/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/abirami-arivazhagan/enterprise-banking-ai-assistant.git
cd enterprise-banking-ai-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file:

```env
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

### Run Backend

```bash
uvicorn app.main:app --reload
```

### Run Frontend

```bash
streamlit run frontend.py
```

---

## Future Enhancements

* Real-time banking system integration
* Advanced multi-agent collaboration
* Voice-enabled customer support
* Automated ticket resolution
* Production-grade monitoring dashboards

---

## Author

**Abirami Arivazhagan**

AI Engineer | Generative AI Enthusiast

GitHub: https://github.com/abirami-arivazhagan
