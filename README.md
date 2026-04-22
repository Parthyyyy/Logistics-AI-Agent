# Enterprise Logistics AI Platform 🚀

A comprehensive AI platform combining Generative AI, Agentic AI, and DevOps best practices to solve complex supply chain and logistics queries.

## 🏗️ The 3 Pillars of this Project

### 1. Generative AI (RAG System)
* Processes and embeds proprietary logistics manuals and bills of lading.
* Utilizes **HuggingFace** for secure, local vector embeddings.
* Powered by **ChromaDB** for semantic similarity search.

### 2. Agentic AI (Autonomous Agents)
* Uses **LangChain & LangGraph** to create a reasoning loop.
* The Agent has access to tools:
  * **RAG Tool**: To search internal company documents.
  * **Web Search Tool**: To check live weather, port congestions, and global shipping news.
* Powered by **Groq (LLaMA 3)** for real-time, high-speed reasoning.

### 3. DevOps (CI/CD & Containerization)
* **Dockerized**: Containerized for seamless deployment across environments.
* **Automated Testing**: Uses `pytest` to ensure agent reliability.
* **CI/CD Pipeline**: GitHub Actions automatically lints, tests, and builds the application on every push.

## How to Run Locally
1. `pip install -r requirements.txt`
2. Add your Groq API key to `.env`
3. `streamlit run src/app.py`