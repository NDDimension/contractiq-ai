from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
from rag_core import get_llm


def _chain(vectorstore, prompt_template: str, k: int = 5):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )
    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=vectorstore.as_retriever(search_kwargs={"k": k}),
        chain_type_kwargs={"prompt": prompt}
    )


# ── 1. Metadata ──────────────────────────────────────────────────────────────

METADATA_PROMPT = """
You are a precise contract analyst. Using ONLY the contract text below, extract the following.
If any item is not found, write "Not specified".

Contract text:
{context}

Extract: {question}

Respond in this exact format (one item per line, no extra commentary):
Party 1: 
Party 2: 
Contract Type: 
Contract Value / Payment: 
Start Date: 
End Date: 
Auto-Renewal: 
Governing Law / Jurisdiction: 
"""

def extract_metadata(vectorstore):
    chain = _chain(vectorstore, METADATA_PROMPT, k=4)
    return chain.invoke("Extract all parties, contract type, payment terms, start date, end date, auto-renewal, and governing law.")


# ── 2. Risk Scanner ──────────────────────────────────────────────────────────

RISK_PROMPT = """
You are a contract risk analyst protecting the interests of the person who hired you.

Contract text:
{context}

Question: {question}

For EACH risk area, respond in EXACTLY this format (one per line):
RISK|LEVEL|CLAUSE_NAME|PLAIN_ENGLISH_EXPLANATION|WHY_IT_MATTERS

Where LEVEL is exactly one of: HIGH, MODERATE, LOW, NOT_FOUND

IMPORTANT CLASSIFICATION RULES:
- HIGH: Clause is dangerously one-sided (e.g., unlimited liability, one-sided termination with no pay, overly broad IP grab, 3+ year non-compete)
- MODERATE: Clause exists but has some imbalance or gaps (e.g., liability cap but very high, vague IP terms, short termination notice)
- LOW: Clause is fair and balanced for both parties (e.g., mutual liability cap at contract value, mutual indemnification, clear fair IP split, reasonable termination with notice)
- NOT_FOUND: Clause is completely absent from the contract

Key: Mutual/balanced terms = LOW risk. One-sided terms = HIGH risk. A contract with liability cap at contract value AND mutual indemnification AND fair termination is LOW risk on those areas.

Analyze these 6 areas: Liability Cap, Indemnification, IP Ownership, Termination Terms, Non-Compete / Exclusivity, Payment Protection

Output exactly 6 lines, one per area, nothing else.
"""

def scan_risks(vectorstore):
    chain = _chain(vectorstore, RISK_PROMPT, k=5)
    return chain.invoke("Identify all risk clauses: liability cap, indemnification, IP ownership, termination terms, non-compete, payment protection.")


# ── 3. Missing Clauses ───────────────────────────────────────────────────────

MISSING_PROMPT = """
You are reviewing a contract to identify which standard protective clauses are present or absent.

Contract text:
{context}

Question: {question}

For EACH clause, respond in EXACTLY this format (one per line):
CLAUSE|STATUS|CLAUSE_NAME|BRIEF_DESCRIPTION

Where STATUS is exactly: PRESENT or MISSING

Example:
CLAUSE|PRESENT|Confidentiality|Both parties agree to keep all shared information confidential for 2 years.
CLAUSE|MISSING|Late Payment Penalty|No penalty for late payment — you have no leverage if they delay.

Check these 6 clauses: Dispute Resolution, Confidentiality / NDA, Scope Change / Additional Work, Late Payment Penalty, Force Majeure, Limitation of Liability

Output exactly 6 lines, one per clause, nothing else.
"""

def check_missing_clauses(vectorstore):
    chain = _chain(vectorstore, MISSING_PROMPT, k=5)
    return chain.invoke("Check which standard protective clauses are present or missing: dispute resolution, confidentiality, scope change, late payment penalty, force majeure, limitation of liability.")


# ── 4. Plain English Summary ─────────────────────────────────────────────────

SUMMARY_PROMPT = """
You are explaining a legal contract to someone with no legal background whatsoever.

Contract text:
{context}

Question: {question}

Write exactly 3 sentences in plain English:
1. What this agreement is about and who the parties are.
2. What the main obligations are (what each party must do).
3. The single most important thing the person should watch out for.

No legal jargon. No bullet points. Just 3 clear sentences.
"""

def plain_english_summary(vectorstore):
    chain = _chain(vectorstore, SUMMARY_PROMPT, k=6)
    return chain.invoke("Summarize this contract in plain English for a non-lawyer.")


# ── 5. Overall Risk Score ────────────────────────────────────────────────────

SCORE_PROMPT = """You are a senior contract attorney. You MUST score this contract using the formula below.

=== RISK CLAUSE ANALYSIS ===
{risk_analysis}

=== MISSING CLAUSE ANALYSIS ===
{missing_analysis}

STEP 1: Count from the analysis above:
- H = number of HIGH risk clauses
- M = number of MODERATE risk clauses  
- X = number of MISSING clauses

STEP 2: Calculate score using this EXACT formula:
  raw_score = 1 + (H * 1.5) + (M * 0.5) + (X * 0.5)
  final_score = min(10, round(raw_score))

STEP 3: Determine recommendation:
- Score 1-3: "SAFE TO SIGN"
- Score 4-5: "REVIEW RECOMMENDED"  
- Score 6-7: "NEGOTIATE FIRST"
- Score 8-10: "DO NOT SIGN"

Respond in EXACTLY this format (three lines, nothing else):
SCORE|<final_score number>
VERDICT|<one sentence about the key risk factors, max 25 words>
RECOMMENDATION|<one of: SAFE TO SIGN, REVIEW RECOMMENDED, NEGOTIATE FIRST, DO NOT SIGN>"""


def overall_risk_score(vectorstore, risk_analysis="", missing_analysis=""):
    """Score using the full analysis context with strict formula."""
    llm = get_llm()

    prompt = SCORE_PROMPT.format(
        risk_analysis=risk_analysis or "Not available",
        missing_analysis=missing_analysis or "Not available",
    )

    response = llm.invoke(prompt)
    raw = response.content if hasattr(response, 'content') else str(response)

    # Extract just the SCORE|, VERDICT|, RECOMMENDATION| lines
    lines = [l.strip() for l in raw.split('\n') if l.strip().startswith(('SCORE|', 'VERDICT|', 'RECOMMENDATION|'))]
    return {"result": "\n".join(lines) if lines else raw}
