import os
import re
import markdown
import subprocess

DOCS_DIR = r"c:\Users\gaura\OneDrive\Desktop\Minor Project\docs"
MD_FILE = os.path.join(DOCS_DIR, "PROJECT_REPORT.md")
HTML_FILE = os.path.join(r"c:\Users\gaura\OneDrive\Desktop\Minor Project\scratch", "report.html")
PDF_FILE = os.path.join(DOCS_DIR, "PROJECT_REPORT.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

with open(MD_FILE, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Replace \newpage with page break divs
md_content = raw_md.replace(r"\newpage", '<div class="page-break"></div>')

# Extract Title, Subtitle, Submitted by, etc. from raw markdown if needed, or let markdown parse it
html_body = markdown.markdown(
    md_content,
    extensions=["tables", "fenced_code", "nl2br"]
)

# Replace mermaid code blocks with styled architectural cards / SVG
def format_mermaid(match):
    code = match.group(1)
    if "graph TD" in code:
        return """
        <div class="architecture-diagram">
            <div class="diagram-title">System Architecture: Layered Full-Stack Flow</div>
            <div class="diagram-grid">
                <div class="dia-box client-box">
                    <strong>Frontend Client (React 19 + Tailwind CSS v4)</strong><br>
                    Social Feed &bull; Live Toxicity Analyzer &bull; Admin Queue &bull; Analytics Telemetry
                </div>
                <div class="dia-arrow">&darr; REST API Calls (JWT / JSON) &darr;</div>
                <div class="dia-box api-box">
                    <strong>API Gateway (FastAPI + Uvicorn)</strong><br>
                    JWT Auth &amp; RBAC &bull; /api/predict &bull; /api/comments &bull; /api/admin &bull; /api/models
                </div>
                <div class="dia-arrow">&darr; Text Pipeline &darr;</div>
                <div class="dia-split">
                    <div class="dia-box nlp-box">
                        <strong>NLP Preprocessing Pipeline</strong><br>
                        Regex Stripper &bull; Slang Map (50+) &bull; Negation Filter &bull; WordNet Lemmatizer
                    </div>
                    <div class="dia-box dl-box">
                        <strong>Deep Learning Inference Engine</strong><br>
                        Embedding (64d) &bull; Conv1D &bull; BiLSTM &bull; Dense Dropout &bull; 6x Sigmoid Heads
                    </div>
                </div>
                <div class="dia-arrow">&darr; Persistence &amp; Policy &darr;</div>
                <div class="dia-box db-box">
                    <strong>Database Persistence &amp; Audit Layer (SQLite + SQLAlchemy)</strong><br>
                    Users Table &bull; Comments Table (Scores &amp; Status) &bull; Moderation Logs Audit Trail
                </div>
            </div>
        </div>
        """
    elif "sequenceDiagram" in code:
        return """
        <div class="architecture-diagram">
            <div class="diagram-title">Process Flow: Real-Time Ingestion, Moderation &amp; Administrative Review</div>
            <div class="seq-list">
                <div class="seq-step"><strong>1. Post Submission:</strong> User enters comment &rarr; React sends <code>POST /api/comments</code> with Bearer JWT.</div>
                <div class="seq-step"><strong>2. Token Verification:</strong> FastAPI authenticates identity and extracts user payload.</div>
                <div class="seq-step"><strong>3. Text Preprocessing:</strong> Regex cleansing, 50+ toxic slang expansions, and WordNet lemmatization.</div>
                <div class="seq-step"><strong>4. Model Inference:</strong> Hybrid CNN + BiLSTM predicts probabilities across 6 toxicity dimensions.</div>
                <div class="seq-step"><strong>5. Policy Evaluation:</strong>
                    <ul>
                        <li><strong>Score &lt; 0.40:</strong> Automatically <em>Approved</em> &rarr; Instant feed broadcast.</li>
                        <li><strong>0.40 &le; Score &lt; 0.75:</strong> Auto-<em>Flagged</em> &rarr; Rendered with "Under Review" banner &rarr; Sent to Admin Queue.</li>
                        <li><strong>Score &ge; 0.75 (or Threat &ge; 0.50):</strong> Auto-<em>Blocked</em> &rarr; Hidden from public display &rarr; Logged as violation.</li>
                    </ul>
                </div>
                <div class="seq-step"><strong>6. Human-in-the-Loop Override:</strong> Admin inspects flagged queue &rarr; executes 1-click Approve or Delete &rarr; logged to audit trail.</div>
            </div>
        </div>
        """
    return f"<pre><code>{code}</code></pre>"

html_body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', format_mermaid, html_body, flags=re.DOTALL)

# HTML template with professional academic print styling
complete_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ToxicGuard AI - Project Report</title>
    <style>
        @page {{
            size: A4;
            margin: 20mm 18mm 20mm 18mm;
            @bottom-right {{
                content: counter(page);
                font-size: 10pt;
                font-family: 'Times New Roman', serif;
            }}
        }}
        
        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 11.5pt;
            line-height: 1.5;
            color: #111827;
            background: #ffffff;
            margin: 0;
            padding: 0;
        }}

        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        h1, h2, h3, h4 {{
            font-family: 'Times New Roman', Times, serif;
            color: #0f172a;
            margin-top: 1.2em;
            margin-bottom: 0.5em;
            font-weight: bold;
        }}

        h1 {{
            font-size: 19pt;
            text-align: center;
            border-bottom: 2px solid #1e293b;
            padding-bottom: 6px;
            margin-top: 0;
        }}

        h2 {{
            font-size: 14pt;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 4px;
        }}

        h3 {{
            font-size: 12.5pt;
        }}

        h4 {{
            font-size: 11.5pt;
        }}

        p {{
            text-align: justify;
            margin-bottom: 0.8em;
            text-indent: 1.5em;
        }}

        p.no-indent, .no-indent p {{
            text-indent: 0 !important;
        }}

        ul, ol {{
            margin-top: 0.3em;
            margin-bottom: 0.8em;
            padding-left: 2em;
        }}

        li {{
            margin-bottom: 0.3em;
            text-align: justify;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.2em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #475569;
            padding: 6px 10px;
            text-align: left;
        }}

        th {{
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: bold;
        }}

        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}

        /* Front Page & Certificate Styling */
        .title-page {{
            text-align: center;
            padding-top: 40px;
            page-break-after: always;
        }}

        .title-page h1 {{
            font-size: 24pt;
            border-bottom: none;
            margin-bottom: 10px;
        }}

        .title-page h2 {{
            font-size: 16pt;
            font-weight: normal;
            border-bottom: none;
            margin-bottom: 40px;
            letter-spacing: 1px;
            color: #334155;
        }}

        .title-page .submitted-by {{
            margin-top: 60px;
            margin-bottom: 50px;
            font-size: 12pt;
        }}

        .title-page .author-name {{
            font-size: 15pt;
            font-weight: bold;
            margin-top: 10px;
            color: #0f172a;
        }}

        .title-page .degree-block {{
            margin-top: 50px;
            font-size: 12pt;
            line-height: 1.7;
        }}

        .title-page .cu-block {{
            margin-top: 70px;
            font-size: 13pt;
            font-weight: bold;
            color: #1e293b;
        }}

        .cert-signatures {{
            display: flex;
            justify-content: space-between;
            margin-top: 70px;
            margin-bottom: 50px;
        }}

        .cert-signatures div {{
            text-align: center;
            width: 45%;
        }}

        /* Architecture box styling */
        .architecture-diagram {{
            border: 1px solid #94a3b8;
            border-radius: 6px;
            padding: 12px;
            margin: 1.5em 0;
            background: #f8fafc;
            page-break-inside: avoid;
        }}

        .diagram-title {{
            font-weight: bold;
            font-size: 11pt;
            text-align: center;
            margin-bottom: 10px;
            color: #1e293b;
        }}

        .diagram-grid {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            align-items: center;
        }}

        .dia-box {{
            width: 90%;
            padding: 8px;
            border-radius: 4px;
            font-size: 9.5pt;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .client-box {{ background: #e0f2fe; border: 1px solid #7dd3fc; color: #0369a1; }}
        .api-box {{ background: #dcfce7; border: 1px solid #86efac; color: #15803d; }}
        .nlp-box {{ background: #fef3c7; border: 1px solid #fde047; color: #b45309; }}
        .dl-box {{ background: #f3e8ff; border: 1px solid #d8b4fe; color: #7e22ce; }}
        .db-box {{ background: #ffedd5; border: 1px solid #fdba74; color: #c2410c; }}

        .dia-split {{
            display: flex;
            gap: 10px;
            width: 95%;
            justify-content: center;
        }}

        .dia-split .dia-box {{
            width: 48%;
        }}

        .dia-arrow {{
            font-size: 11pt;
            color: #64748b;
            font-weight: bold;
        }}

        .seq-list {{
            font-size: 10pt;
            line-height: 1.6;
        }}

        .seq-step {{
            margin-bottom: 6px;
            padding: 4px 8px;
            background: #ffffff;
            border-left: 3px solid #3b82f6;
        }}

        code {{
            font-family: Consolas, monospace;
            background-color: #f1f5f9;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 9.5pt;
            color: #0f172a;
        }}

        pre code {{
            display: block;
            padding: 10px;
            overflow-x: auto;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(complete_html)

print(f"HTML successfully generated at: {HTML_FILE}")

# Execute headless Microsoft Edge to render to PDF
cmd = [
    EDGE_PATH,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_FILE}",
    "--no-pdf-header-footer",
    HTML_FILE
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Edge return code:", res.returncode)
if os.path.exists(PDF_FILE):
    size_kb = os.path.getsize(PDF_FILE) / 1024
    print(f"SUCCESS: PDF created at {PDF_FILE} ({size_kb:.1f} KB)")
else:
    print("FAILED to create PDF")
