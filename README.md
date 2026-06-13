# ⚖️ ContractIQ — AI Contract Risk Scanner

> **From raw contract upload to structured legal-risk report in under a minute. Built for fast first-pass contract review, not legal advice.**

ContractIQ is a production-ready AI contract analysis app built with **Flask + LangChain + Groq + HuggingFace embeddings + FAISS**. Users can upload a contract as **PDF, TXT, or DOCX**, or paste text directly. ContractIQ extracts key metadata, scans risky clauses, checks for missing protections, writes a plain-English summary, and returns an overall risk score with a clear recommendation.

---

![Flask](https://img.shields.io/badge/Flask-Web_App-000000?style=for-the-badge&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-RAG_Pipeline-1C3C3C?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-2E6BE6?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

---

## 🧩 The Problem It Solves

Freelancers, founders, consultants, and small teams often receive contracts they do not fully understand. Before sending a document to a lawyer, they usually need a fast first-pass answer:

- Who are the parties?
- What are the payment terms?
- Are there risky clauses?
- Which standard protections are missing?
- Is this safe to sign, or should it be negotiated first?

Doing that manually takes time and legal confidence. **ContractIQ turns a contract into a clear AI-generated risk report in one workflow.**

---

## ⚙️ End-to-End Workflow

```
[User Uploads PDF / TXT / DOCX]
        or
[User Pastes Contract Text]
        ↓
[Flask Backend]
Validates input | Saves temporary file | Extracts text
        ↓
[LangChain Text Splitter]
Chunks contract into searchable sections
        ↓
[HuggingFace Embeddings]
Creates local semantic embeddings with all-MiniLM-L6-v2
        ↓
[FAISS Vector Store]
Retrieves the most relevant contract sections for each analysis step
        ↓
[Groq Llama 3.3 70B]
Runs 5 focused contract analysis chains
        ↓
[Interactive Web Report]
Metadata | Risks | Missing clauses | Summary | Score | Recommendation
```

---

## 🤖 What the AI Actually Does

### 1. Contract Metadata
Extracts core business details from the document:
- **Party 1**
- **Party 2**
- **Contract Type**
- **Payment Terms**
- **Start Date**
- **End Date**
- **Auto-Renewal**
- **Governing Law / Jurisdiction**

### 2. Risk Clause Scanner
Reviews 6 high-impact contract areas and classifies each one:
- **Liability Cap**
- **Indemnification**
- **IP Ownership**
- **Termination Terms**
- **Non-Compete / Exclusivity**
- **Payment Protection**

Each risk is labeled as:

```text
HIGH | MODERATE | LOW | NOT_FOUND
```

### 3. Missing Clause Check
Checks whether standard protective clauses are present or missing:
- **Dispute Resolution**
- **Confidentiality / NDA**
- **Scope Change / Additional Work**
- **Late Payment Penalty**
- **Force Majeure**
- **Limitation of Liability**

### 4. Plain-English Summary
Explains the contract in exactly 3 simple sentences:
- What the agreement is about
- What each side must do
- The most important thing to watch out for

### 5. Overall Risk Score
Calculates a 1–10 risk score using the AI risk analysis and missing-clause results:

```text
1–3   → SAFE TO SIGN
4–5   → REVIEW RECOMMENDED
6–7   → NEGOTIATE FIRST
8–10  → DO NOT SIGN
```

---

## 🛠️ Tech Stack

| Tool | Role | Cost |
|------|------|------|
| Flask | Web server and API routes | Free |
| LangChain | RAG pipeline and analysis chains | Free |
| Groq Llama 3.3 70B | LLM contract reasoning | Free tier available |
| HuggingFace all-MiniLM-L6-v2 | Local embeddings | Free |
| FAISS | Local vector search | Free |
| pypdf | PDF text extraction | Free |
| python-docx | DOCX text extraction | Free |
| Gunicorn | Production WSGI server | Free |
| Docker | Containerized deployment | Free |
| Vanilla HTML/CSS/JS | Frontend UI | Free |

> **No database required. Uploaded files are processed through temporary files and removed after extraction.**

---

## 📁 Repository Structure

```
contractiq/
│
├── app.py                  ← Flask app, routes, health check, upload handling
├── rag_core.py             ← PDF/TXT/DOCX loaders, splitter, embeddings, FAISS
├── analyzers.py            ← LangChain prompts and contract analysis chains
├── requirements.txt        ← Python dependencies
├── Dockerfile              ← Production Docker image
├── docker-compose.yml      ← Local Docker Compose setup
├── .dockerignore           ← Keeps secrets and local files out of the image
├── .env.example            ← Example environment file
│
├── templates/
│   └── index.html          ← Flask-rendered frontend UI
│
├── test_contracts/
│   ├── best_contract.txt
│   ├── good_contract.txt
│   └── worst_contract.txt
│
└── README.md
```

---

## 🚀 Local Setup

### 1. Clone or open the project folder

```bash
cd ContractIQ
```

### 2. Create and activate a virtual environment

**Mac / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows Command Prompt:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Windows PowerShell:**

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The first install may take a few minutes because `sentence-transformers` installs PyTorch and embedding dependencies.

### 4. Add your Groq API key

Create a `.env` file:

```bash
cp .env.example .env
```

Then add:

```text
GROQ_API_KEY=gsk_...your_actual_key_here
```

Get a key from:

```text
https://console.groq.com/keys
```

### 5. Run locally

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## 🐳 Docker Setup

Build the image:

```bash
docker build -t contractiq .
```

Run the container:

```bash
docker run --env-file .env -p 5000:5000 contractiq
```

Or use Docker Compose:

```bash
docker compose up --build
```

Open:

```text
http://localhost:5000
```

The Docker image uses CPU-only Torch to avoid downloading unnecessary CUDA/GPU packages.

---

## ☁️ Deployment

Recommended platforms:

| Platform | Best For |
|----------|----------|
| Render | Easiest production deploy for this project |
| Railway | Fast portfolio/demo deployment |
| Fly.io | Docker-first deployment with more control |
| DigitalOcean App Platform | Simple managed app hosting |
| AWS EC2 / Lightsail | Manual VPS-style deployment |

### Recommended Render Settings

- **Runtime:** Docker or Python
- **Environment variable:** `GROQ_API_KEY`
- **Health check path:** `/health`
- **Start command without Docker:**

```bash
gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 180 app:app
```

Keep `workers` low on small instances because the embedding model is loaded into memory.

---

## ✅ Testing Checklist

Use one of the sample contracts in `test_contracts/`, or upload your own contract.

- [ ] PDF upload works
- [ ] TXT upload works
- [ ] DOCX upload works
- [ ] Paste text works
- [ ] Loading spinner appears during analysis
- [ ] Contract Details show extracted metadata
- [ ] Risk Scanner shows HIGH / MODERATE / LOW / NOT_FOUND results
- [ ] Missing Clause Check shows PRESENT / MISSING results
- [ ] Plain-English Summary returns 3 clear sentences
- [ ] Overall Risk Score returns a number from 1 to 10
- [ ] `/health` returns `{"status":"ok"}`

---

## 🔧 Customization Options

- Add contract-type specific analysis for NDAs, employment agreements, vendor contracts, SaaS terms, or freelance agreements
- Add user accounts and saved report history
- Export the final report as PDF
- Add clause-level citations with page numbers
- Add a confidence score for each extracted field
- Add a lawyer-review handoff workflow
- Add email delivery for completed reports
- Replace Groq with another LangChain-supported LLM
- Move FAISS to a persistent vector database for multi-document search

---

## 🧯 Troubleshooting

**`ModuleNotFoundError: No module named 'langchain_groq'`**

Make sure your virtual environment is activated, then run:

```bash
pip install -r requirements.txt
```

**Groq authentication error**

Check that `.env` contains:

```text
GROQ_API_KEY=gsk_...
```

No quotes, no extra spaces.

**`413 Request Entity Too Large`**

The uploaded file is over the Flask limit. Update `MAX_CONTENT_LENGTH` in `app.py` if you need larger files.

**First analysis is slow**

HuggingFace downloads and caches the `all-MiniLM-L6-v2` embedding model on first use.

**Docker image is large**

This is expected because `sentence-transformers`, PyTorch, FAISS, and SciPy are ML-heavy dependencies. The Dockerfile uses CPU-only Torch to keep it much smaller than a CUDA-based image.

---

## 💼 Freelance Pitch

> "I built ContractIQ, an AI contract risk scanner that uses LangChain RAG to analyze PDF, TXT, and DOCX contracts. It extracts key terms, flags risky clauses, checks for missing protections, summarizes the agreement in plain English, and generates a 1–10 risk score. Stack: Flask, Groq Llama 3.3 70B, HuggingFace embeddings, FAISS, and Docker."

Use cases:
- Freelance contract review tools
- NDA first-pass screening
- Vendor agreement analysis
- Employment offer review
- SaaS terms review
- Legal-tech MVPs

---

## ⚠️ Legal Disclaimer

ContractIQ provides AI-generated first-pass analysis only. It is **not legal advice** and should not replace review by a qualified lawyer.

---

## 📄 License

This project is released under a proprietary license.

The repository is provided for portfolio and evaluation purposes only. Commercial use, redistribution, resale, and client deployment are prohibited without explicit written permission from the author.

---

*Built by Dhanraj Sharma — AI Automation Specialist*
