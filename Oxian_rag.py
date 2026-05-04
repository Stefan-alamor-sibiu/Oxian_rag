import os
import sys
from dotenv import load_dotenv

load_dotenv()
# 1. REZOLVARE DLL (PENTRU CUDA 13.2)
cuda_bin = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2\bin"
if os.path.exists(cuda_bin):
    os.add_dll_directory(cuda_bin)
else:
    print("!! Folderul CUDA nu a fost găsit. Verifică instalarea!")

try:
    from llama_cpp import Llama
    from pypdf import PdfReader
    import chromadb
    from sentence_transformers import SentenceTransformer
    print(">> [OK] Librării încărcate cu succes.")
except Exception as e:
    print(f"!! Eroare la import: {e}")
    sys.exit()

# 2. CALEA CĂTRE MODELUL TĂU DIN LM STUDIO
MODEL_PATH = os.getenv("MODEL_SECRET_PATH", "./models/qwen-qwen3.5-2b-base-f16.gguf")

print(">> Pornesc RTX 4060... Încarc Qwen 3.5...")
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1, # ARUNCĂ TOT PE PLACA VIDEO
    n_ctx=65536,      # [MODIFICAT] Urcat la 64k pentru RTX 4060 (8GB VRAM)
    verbose=True
)

# 3. CONFIGURARE "CREIER" PDF (RAG)
CALE_EMBEDDER = r"./model_embed"
embedder = SentenceTransformer(CALE_EMBEDDER, local_files_only=True)

db = chromadb.PersistentClient(path="./baza_date_bac")
colectie = db.get_or_create_collection(name="materie_examen")

def invata_pdf(cale_fisier):
    print(f">> Citesc și memorez: {cale_fisier}...")
    pdf = PdfReader(cale_fisier)
    for i, pagina in enumerate(pdf.pages):
        text = pagina.extract_text()
        if text:
            # Transformăm textul în numere (vectori) pe care AI-ul îi înțelege
            vector = embedder.encode(text).tolist()
            colectie.add(embeddings=[vector], documents=[text], ids=[f"pag_{i}"])
    print(">> GATA! Sunt expert în acest PDF.")

# 4. EXECUȚIE
if __name__ == "__main__":
    # PUNE PDF-ul TĂU DE BAC ÎN FOLDER ȘI SCRIE-I NUMELE AICI:
    PDF_DE_INVATAT = "resursa.pdf" 
    
    if os.path.exists(PDF_DE_INVATAT):
        if colectie.count() == 0:
            invata_pdf(PDF_DE_INVATAT)
        
        print("\n" + "="*45)
        print("SISTEM RAG ACTIVAT - 100% OFFLINE - RTX 4060")
        print("="*45)
        
        while True:
            intrebare = input("\nÎntreabă-mă despre materie: ")
            if intrebare.lower() in ["exit", "pa", "bafta"]: break
            
            # Căutăm în document
            v_intrebare = embedder.encode(intrebare).tolist()
            # [MODIFICAT] Am crescut n_results la 50 ca să ia mai mult context (50 pagini) din PDF
            rezultate = colectie.query(query_embeddings=[v_intrebare], n_results=50) 
            context = "\n".join(rezultate["documents"][0])
            
            # Îi dăm AI-ului contextul și întrebarea
            prompt = f"Context: {context}\n\nÎntrebare: {intrebare}\nRăspuns în limba română:"
            
            # [MODIFICAT] Generăm răspunsul cu "manie" (temperature + seed) și max_tokens=-1
            output = llm(
                prompt, 
                max_tokens=-1, 
                stop=["Context:", "Întrebare:"],
                temperature=0.8, # Creativitate / evitarea repetițiilor
                seed=-1          # Haos pseudorandom bazat pe ceasul sistemului
            )
            
            print(f"\n[RĂSPUNS BAC]: {output['choices'][0]['text']}")
    else:
        print(f"!! Pune fișierul '{PDF_DE_INVATAT}' în folderul cu scriptul ca să începem.")