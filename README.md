# Oxian RAG - 100% Offline AI Assistant

### This project is a high-performance, private, and fully offline AI assistant designed for Baccalaureate exam preparation. It uses RAG (Retrieval-Augmented Generation) to answer questions based on your specific PDF study materials.

# 1. Manual Library Installation

Run these commands one by one in your terminal to set up the environment:
## Install the core LLM engine
    pip install llama-cpp-python

## Install PDF processing tools
    pip install pypdf

## Install the vector database (ChromaDB)
    pip install chromadb

## Install the embedding engine
    pip install sentence-transformers

## Install PyTorch with CUDA 12.4 support (Optimized for RTX 4060)
    pip install torch --index-url https://download.pytorch.org/whl/cu124

# 2. Setting Up the Offline Embedding Model

Since we are keeping this project 100% offline, you need to download the embedding model once and save it locally.

Create a file named setup_embed.py and run it:

    from sentence_transformers import SentenceTransformer

    #This downloads the model and saves it to a local folder
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model.save('./model_embed')

print("Success! The 'model_embed' folder is now ready for offline use.")

# 3. Configuring Your Local Model Path

Since we are not using environment variables, you must manually point the script to your .gguf model file.

    1.Open Oxian_rag.py.

    2.Find the line where MODEL_PATH is defined.

    3.Replace the path with your actual local path.

Example in code:# Change this to your actual local path!
    MODEL_PATH = r"C:\Users\YourName\Path\To\qwen3.5-2b-base-f16.gguf"

# 4. How to Run

    1.Place your study material in the root folder and name it resursa.pdf

    2.Open terminal in the rag folder

    3.Run the main script:
        python Oxian_rag.py

# 5. **The Legend of Oxian: From "Glou-Glou" to AI**

![Oxian](supadevarza.gif)

The name **Oxian** is a tribute to the classic film *"La Soupe aux choux"*. 

In the movie, the visitor from planet **Oxo** initially communicates with humans through strange, turkey-like sounds (**"Glou-Glou"**). As this is my **first serious software project**, the name is a metaphor for the development process:

1.  **The "Glou-Glou" Phase:** Just like the alien, every programmer starts with "sounds" that no one understands—bugs, errors, and trial-and-error. 
2.  **Learning to Talk:** This project represents my journey of turning those initial "turkey sounds" into a coherent, high-tech AI system that can actually "talk" and help with the Baccalaureate.

**Oxian RAG** is more than just code; it's a bridge between a beginner's first steps and the "otherworldly" power of Local Artificial Intelligence.        
