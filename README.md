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

## 🎬 Live Demo

[![Watch Demo](https://img.shields.io/badge/Watch_Demo-Loom_Video-625DF5?style=for-the-badge)](https://drive.google.com/file/d/1F9EN21CxG02ZtMq7jc_slgyGSZYlY6Kv/view?usp=sharing)

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

---prot

## ⚠️ Legal Disclaimer

ContractIQ provides AI-generated first-pass analysis only. It is **not legal advice** and should not replace review by a qualified lawyer.

---

## 📬 Hire Me

I build custom client intake, lead qualification, and consultation automation systems for freelancers and agencies.

- 🔗 **Upwork:** [*Dhanraj Sharma*](https://www.upwork.com/freelancers/~010e4c7ac19e0fdda1?mp_source=share)
- 🔗 **Contra:** [*Dhanraj Sharma*](https://contra.com/dhanraj_sharma_rgam8kpb?referralExperimentNid=DEFAULT_REFERRAL_PROGRAM&referrerUsername=dhanraj_sharma_rgam8kpb)
- 💼 **LinkedIn:** [*Dhanraj Sharma*](https://www.linkedin.com/in/dhanraj-sharma-nddimension/)
- 📧 **Email:** *hinatashoyo101824@gmail.com*

---

## 📄 License

This project is released under a proprietary license.

The repository is provided for portfolio and evaluation purposes only. Commercial use, redistribution, resale, and client deployment are prohibited without explicit written permission from the author.

---

*Built by Dhanraj Sharma — AI Automation Specialist*
