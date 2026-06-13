from flask import Flask, render_template, request, jsonify
import tempfile, os, json, re
from rag_core import load_contract_file, load_contract_text, build_vectorstore
from analyzers import extract_metadata, scan_risks, check_missing_clauses, plain_english_summary, overall_risk_score

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        chunks = None

        uploaded_file = request.files.get('contract_file') or request.files.get('pdf')
        if uploaded_file and uploaded_file.filename:
            _, ext = os.path.splitext(uploaded_file.filename)
            ext = ext.lower()
            if ext not in {'.pdf', '.txt', '.docx'}:
                return jsonify({'error': 'Unsupported file type. Please upload a PDF, TXT, or DOCX file.'}), 400

            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                    uploaded_file.save(tmp.name)
                    tmp_path = tmp.name
                chunks = load_contract_file(tmp_path, ext)
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        elif request.form.get('contract_text', '').strip():
            text = request.form.get('contract_text').strip()
            chunks = load_contract_text(text)
        else:
            return jsonify({'error': 'Please upload a PDF, TXT, or DOCX file, or paste contract text.'}), 400

        vectorstore = build_vectorstore(chunks)

        metadata  = extract_metadata(vectorstore)
        risks     = scan_risks(vectorstore)
        missing   = check_missing_clauses(vectorstore)
        summary   = plain_english_summary(vectorstore)

        # Pass risk + missing analysis into scoring for accurate context
        risk_text = risks.get('result', '')
        missing_text = missing.get('result', '')
        score_obj = overall_risk_score(vectorstore, risk_analysis=risk_text, missing_analysis=missing_text)

        return jsonify({
            'chunk_count': len(chunks),
            'metadata':    metadata.get('result', ''),
            'risks':       risk_text,
            'missing':     missing_text,
            'summary':     summary.get('result', ''),
            'score':       score_obj.get('result', ''),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    app.run(debug=debug, host='0.0.0.0', port=port)
