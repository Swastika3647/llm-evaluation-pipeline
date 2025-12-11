# LLM Response Evaluation Pipeline

## 🚀 Project Overview
This project implements a real-time evaluation pipeline for checking the quality of RAG (Retrieval-Augmented Generation) responses. It automatically tests AI-generated answers against three core metrics:
1.  **Relevance:** Does the answer address the user's specific query?
2.  **Faithfulness (Hallucination):** Is the answer grounded strictly in the retrieved context?
3.  **Performance:** Tracks response latency and estimated costs.

## 🛠️ Setup Instructions

### Prerequisites
* Python 3.8+
* A Groq API Key (Free tier used for high-performance inference)

### Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/Swastika3647/llm-evaluation-pipeline.git](https://github.com/Swastika3647/llm-evaluation-pipeline.git)
    cd llm-evaluation-pipeline
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up your API Key:
    * Linux/Mac: `export GROQ_API_KEY="gsk_..."`
    * Windows: `set GROQ_API_KEY="gsk_..."`

### Running the Pipeline
Run the main evaluation script:
```bash
python evaluate_rag.py
