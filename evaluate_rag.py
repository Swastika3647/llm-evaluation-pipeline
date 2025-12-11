import os
import time
import json
import csv
from openai import OpenAI
from datetime import datetime


os.environ["GROQ_API_KEY"] = "PASTE_YOUR_KEY_HERE" 

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)



def save_to_csv(data: dict, filename="evaluation_report.csv"):
    """Saves the evaluation result to a CSV file."""
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    print(f"   📂 Saved result to {filename}")



def run_evaluation_pipeline(query: str):
    print(f"\n🚀 Starting Evaluation for Query: '{query}'")
    
   
    try:
        with open('sample_context_vectors-01.json', 'r') as f:
            data = json.load(f)
            vectors = data.get("data", {}).get("vector_data", [])
            context = "\n".join([f"- {v.get('text', '')}" for v in vectors])
    except FileNotFoundError:
        print("❌ Error: Context file not found.")
        return

   
    print("   🤖 Generating Answer (via Groq Llama-3)...")
    start_time = time.time()
    
    try:
       
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Answer strictly based on this context:\n{context}"},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message.content
        latency = (time.time() - start_time) * 1000 
    except Exception as e:
        print(f"❌ API Error during Generation: {e}")
        return

    
    print("   ⚖️  Auditing Response...")
    
    
    judge_prompt = f"""
    You are a QA Auditor. Evaluate this RAG interaction.
    
    User Query: {query}
    Retrieved Context: {context[:15000]} 
    AI Answer: {answer}
    
    Return a JSON object with this exact format:
    {{
      "relevance_score": 0.0,
      "relevance_reason": "...",
      "hallucination_score": 0.0,
      "hallucination_reason": "..."
    }}
    
    Criteria:
    - relevance_score: Did the AI answer the specific question? (0.0=No, 1.0=Yes)
    - hallucination_score: Is the answer supported by the text? (0.0=Hallucinated, 1.0=Grounded)
    """

    try:
        judge_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful judge. Output valid JSON only."},
                {"role": "user", "content": judge_prompt}
            ],
            response_format={"type": "json_object"}
        )
        scores_dict = json.loads(judge_res.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ API Error during Evaluation: {e}")
        return

   
    result_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "answer_snippet": answer[:50] + "...", 
        "latency_ms": round(latency, 2),
        "cost_usd": 0.0, 
        "relevance_score": scores_dict.get("relevance_score", 0),
        "relevance_reason": scores_dict.get("relevance_reason", "N/A"),
        "hallucination_score": scores_dict.get("hallucination_score", 0),
        "hallucination_reason": scores_dict.get("hallucination_reason", "N/A")
    }
    
    save_to_csv(result_data)

   
    print("\n📊 EVALUATION SUMMARY")
    print(f"   Answer: {answer}")
    print(f"   ⏱️  Latency: {latency:.2f} ms")
    print(f"   💰 Cost: $0.00 (Groq Free Tier)")
    print(f"   ✅ Relevance: {result_data['relevance_score']}")
    print(f"   🤥 Faithfulness: {result_data['hallucination_score']}")
    print("-" * 50)

if __name__ == "__main__":
    run_evaluation_pipeline("What is the cost of a complete IVF cycle?")