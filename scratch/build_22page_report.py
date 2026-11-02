import os
import subprocess
import pypdf
import base64

DOCS_DIR = r"c:\Users\gaura\OneDrive\Desktop\Minor Project\docs"
IMAGES_DIR = os.path.join(DOCS_DIR, "images")
HTML_FILE = os.path.join(r"c:\Users\gaura\OneDrive\Desktop\Minor Project\scratch", "report_22pages.html")
PDF_FILE = os.path.join(DOCS_DIR, "PROJECT_REPORT.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def get_b64(filename):
    path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_0 = get_b64("logo_0.png")
logo_1 = get_b64("logo_1.png")
fig3_1 = get_b64("fig3_1_flowchart.png")
fig3_2 = get_b64("fig3_2_architecture.png")
fig4_1 = get_b64("fig4_1_about.png")
fig4_2 = get_b64("fig4_2_login.png")
fig4_3 = get_b64("fig4_3_feed.png")
fig4_4 = get_b64("fig4_4_live_check.png")
fig4_5 = get_b64("fig4_5_live_prediction.png")
fig4_6 = get_b64("fig4_6_admin_queue.png")
fig4_7 = get_b64("fig4_7_analytics_trends.png")
fig4_8 = get_b64("fig4_8_analytics_distribution.png")
fig4_9 = get_b64("fig4_9_model_performance.png")
fig4_10 = get_b64("fig4_10_swagger_docs.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ToxicGuard AI - Project Report</title>
    <style>
        @page {{
            size: A4;
            margin: 20mm 20mm 20mm 20mm;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 11pt;
            line-height: 1.45;
            color: #000;
            background: #fff;
            margin: 0;
            padding: 0;
        }}

        .page {{
            width: 100%;
            height: 252mm; /* strictly fit A4 height minus 40mm margins */
            position: relative;
            page-break-after: always;
            break-after: page;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            overflow: hidden;
        }}

        .page-num {{
            position: absolute;
            bottom: 0mm;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 11pt;
            color: #000;
        }}

        /* Headings */
        h1.chap-num {{
            text-align: center;
            font-size: 13pt;
            font-weight: bold;
            margin: 0 0 4px 0;
            letter-spacing: 0.5px;
        }}

        h1.chap-title {{
            text-align: center;
            font-size: 13pt;
            font-weight: bold;
            margin: 0 0 16px 0;
            letter-spacing: 0.5px;
        }}

        h2.sec-heading {{
            font-size: 11.5pt;
            font-weight: bold;
            margin: 12px 0 6px 0;
        }}

        h3.subsec-heading {{
            font-size: 11pt;
            font-weight: bold;
            margin: 8px 0 4px 0;
        }}

        p {{
            margin: 0 0 8px 0;
            text-align: justify;
            text-indent: 0;
            line-height: 1.45;
        }}

        p.indent {{
            text-indent: 1.5em;
        }}

        /* Lists */
        ol, ul {{
            margin: 0 0 8px 0;
            padding-left: 22px;
        }}

        li {{
            margin-bottom: 4px;
            text-align: justify;
        }}

        /* Tables */
        table.academic-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0 4px 0;
            font-size: 9.5pt;
        }}

        table.academic-table th, table.academic-table td {{
            border: 1px solid #444;
            padding: 5px 7px;
            text-align: left;
            vertical-align: top;
        }}

        table.academic-table th {{
            background-color: #f1f5f9;
            font-weight: bold;
            text-align: center;
        }}

        .caption {{
            text-align: center;
            font-weight: bold;
            font-size: 10.5pt;
            margin: 6px 0 10px 0;
        }}

        /* Figures */
        .fig-box {{
            text-align: center;
            margin: 6px 0 4px 0;
        }}

        .fig-img {{
            max-width: 90%;
            max-height: 185px;
            border: 1px solid #94a3b8;
            border-radius: 3px;
        }}

        .fig-img-wide {{
            max-width: 98%;
            max-height: 195px;
            border: 1px solid #94a3b8;
            border-radius: 3px;
        }}

        .fig-caption {{
            text-align: center;
            font-weight: bold;
            font-size: 10.5pt;
            margin-top: 5px;
            margin-bottom: 8px;
        }}

        /* TOC */
        .toc-row {{
            display: flex;
            align-items: baseline;
            margin-bottom: 3.5px;
            font-size: 10.5pt;
        }}
        .toc-bold {{
            font-weight: bold;
            margin-top: 5px;
        }}
        .toc-sub {{
            padding-left: 18px;
            font-size: 10pt;
        }}
        .toc-leader {{
            flex-grow: 1;
            border-bottom: 1px dotted #333;
            margin: 0 5px;
        }}
    </style>
</head>
<body>

<!-- ==================== PAGE 1: TITLE / COVER PAGE ==================== -->
<div class="page" style="text-align: center; justify-content: space-between; padding: 5px 0 15px 0;">
    <div>
        <img src="{logo_0}" style="width: 100%; max-height: 60px; object-fit: contain;" alt="CU NAAC A+ Logo">
    </div>

    <div style="margin-top: 20px;">
        <div style="font-size: 18pt; font-weight: bold; margin-bottom: 15px; line-height: 1.3;">
            ToxicGuard AI: Multi-Label Toxic Comment Moderation System
        </div>
        <div style="font-size: 14pt; font-weight: bold; letter-spacing: 0.5px; margin-bottom: 25px;">
            MINI PROJECT REPORT
        </div>
        <div style="font-size: 11pt; margin-bottom: 6px;">Submitted by</div>
        <div style="font-size: 14pt; font-weight: bold; margin-bottom: 4px;">
            Gaurav Singh (25MCI10104)
        </div>
        <div style="font-size: 11pt; margin-bottom: 25px;">
            Section: 25MAM 1-A
        </div>

        <div style="font-size: 10.5pt; font-style: italic; margin-bottom: 6px;">
            in partial fulfillment for the award of the degree of
        </div>
        <div style="font-size: 13pt; font-weight: bold; margin-bottom: 4px;">
            MASTER OF COMPUTER APPLICATIONS
        </div>
        <div style="font-size: 11pt; font-weight: bold; margin-bottom: 4px;">
            IN
        </div>
        <div style="font-size: 12pt; font-weight: bold;">
            ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING
        </div>
    </div>

    <div>
        <img src="{logo_1}" style="width: 85px; object-fit: contain; margin-bottom: 15px;" alt="Chandigarh University Crest">
        <div style="font-size: 12pt; font-weight: bold; margin-bottom: 4px;">
            Chandigarh University, India.
        </div>
        <div style="font-size: 11pt;">
            October 2026
        </div>
    </div>
    <div class="page-num">1</div>
</div>

<!-- ==================== PAGE 2: BONAFIDE CERTIFICATE ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-title" style="margin-top: 15px; margin-bottom: 30px;">BONAFIDE CERTIFICATE</h1>
    
    <p style="text-align: justify; line-height: 1.7; margin-bottom: 50px;">
        Certified that this project report <strong>“ToxicGuard AI: Multi-Label Toxic Comment Moderation System”</strong> is the bonafide work of <strong>“Gaurav Singh (25MCI10104)”</strong> who carried out the project work under my supervision on 29/10/2026.
    </p>

    <div style="display: flex; justify-content: space-between; margin-bottom: 70px;">
        <div style="width: 45%;">
            <div style="font-weight: bold; font-size: 11pt; margin-bottom: 35px;">SIGNATURE</div>
            <div style="font-weight: bold; font-size: 11.5pt;">Dr Amanpreet Kaur Sandhu</div>
            <div style="font-weight: bold; font-size: 11pt;">HEAD OF THE DEPARTMENT</div>
            <div style="font-size: 10.5pt;">University Institute of Computing</div>
        </div>
        <div style="width: 45%; text-align: right;">
            <div style="font-weight: bold; font-size: 11pt; margin-bottom: 35px;">SIGNATURE</div>
            <div style="font-weight: bold; font-size: 11.5pt;">Ms. Sweta</div>
            <div style="font-weight: bold; font-size: 11pt;">SUPERVISOR</div>
            <div style="font-size: 10.5pt;">assistant professor</div>
            <div style="font-size: 10.5pt;">UIC</div>
        </div>
    </div>

    <div style="text-align: left; margin-bottom: 70px; font-size: 11pt;">
        Submitted for the project viva-voce examination held on 29/10/2026
    </div>

    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 11pt;">
        <div>INTERNAL EXAMINER</div>
        <div>EXTERNAL EXAMINER</div>
    </div>

    <div class="page-num">2</div>
</div>

<!-- ==================== PAGE 3: ACKNOWLEDGEMENT ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-title" style="margin-top: 15px; margin-bottom: 30px;">ACKNOWLEDGEMENT</h1>

    <p style="text-align: justify; line-height: 1.65; margin-bottom: 18px;">
        I would like to express my heartfelt gratitude to all those who assisted me in preparing and completing my project report titled <strong>“ToxicGuard AI: Multi-Label Toxic Comment Moderation System.”</strong> I extend my sincere appreciation and thanks to <strong>Ms. Sweta</strong> for inspiring, cooperating with, and encouraging me throughout this work. With her valuable suggestions and guidance, I was able to complete my work within the stipulated time frame at this institution.
    </p>

    <p style="text-align: justify; line-height: 1.65; margin-bottom: 18px;">
        I also convey my respect and gratitude to <strong>Dr Amanpreet Kaur Sandhu</strong>, Head of the Department, University Institute of Computing, and Chandigarh University, as well as all the faculty members, for their valuable suggestions and guidance towards completing the report. I am also thankful to the open-source community behind FastAPI, React, PyTorch, Keras, and SQLite, and to the developers of modern natural language processing toolkits. Last but not least, I am immensely grateful to my parents, who served as a constant source of encouragement and inspiration throughout the completion of this work at Chandigarh University, Mohali.
    </p>

    <div style="margin-top: 50px;">
        <div style="font-weight: bold; font-size: 11.5pt; margin-bottom: 4px;">Gaurav Singh (25MCI10104)</div>
        <div style="font-size: 11pt; margin-bottom: 2px;">University Institute of Computing</div>
        <div style="font-size: 11pt;">Chandigarh University, Mohali</div>
    </div>

    <div class="page-num">3</div>
</div>

<!-- ==================== PAGE 4: TABLE OF CONTENTS ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-title" style="margin-top: 15px; margin-bottom: 25px;">TABLE OF CONTENTS</h1>

    <div class="toc-row toc-bold"><span>ABSTRACT</span><span class="toc-leader"></span><span>5</span></div>
    
    <div class="toc-row toc-bold"><span>CHAPTER 1. INTRODUCTION</span><span class="toc-leader"></span><span>6</span></div>
    <div class="toc-row toc-sub"><span>1. Identification of Client/ Need/ Relevant Contemporary issue</span><span class="toc-leader"></span><span>6</span></div>
    <div class="toc-row toc-sub"><span>2. Identification of Problem</span><span class="toc-leader"></span><span>6</span></div>
    <div class="toc-row toc-sub"><span>3. Identification of Tasks</span><span class="toc-leader"></span><span>6</span></div>
    <div class="toc-row toc-sub"><span>4. Timeline</span><span class="toc-leader"></span><span>7</span></div>

    <div class="toc-row toc-bold"><span>CHAPTER 2. LITERATURE REVIEW/BACKGROUND STUDY</span><span class="toc-leader"></span><span>8</span></div>
    <div class="toc-row toc-sub"><span>1. Existing solutions</span><span class="toc-leader"></span><span>8</span></div>
    <div class="toc-row toc-sub"><span>2. Bibliometric analysis</span><span class="toc-leader"></span><span>8</span></div>
    <div class="toc-row toc-sub"><span>3. Review Summary</span><span class="toc-leader"></span><span>9</span></div>
    <div class="toc-row toc-sub"><span>4. Goals/Objectives</span><span class="toc-leader"></span><span>9</span></div>

    <div class="toc-row toc-bold"><span>CHAPTER 3. DESIGN FLOW/PROCESS</span><span class="toc-leader"></span><span>10</span></div>
    <div class="toc-row toc-sub"><span>1. Evaluation &amp; Selection of Specifications/Features</span><span class="toc-leader"></span><span>10</span></div>
    <div class="toc-row toc-sub"><span>2. Design Constraints</span><span class="toc-leader"></span><span>10</span></div>
    <div class="toc-row toc-sub"><span>3. Analysis of Features and finalization subject to constraints</span><span class="toc-leader"></span><span>11</span></div>
    <div class="toc-row toc-sub"><span>4. Design Flow</span><span class="toc-leader"></span><span>11</span></div>
    <div class="toc-row toc-sub"><span>5. Design selection</span><span class="toc-leader"></span><span>12</span></div>
    <div class="toc-row toc-sub"><span>6. Implementation plan/methodology</span><span class="toc-leader"></span><span>12</span></div>

    <div class="toc-row toc-bold"><span>CHAPTER 4. RESULTS ANALYSIS AND VALIDATION</span><span class="toc-leader"></span><span>14</span></div>
    <div class="toc-row toc-sub"><span>1. Implementation of solution</span><span class="toc-leader"></span><span>14</span></div>
    <div class="toc-row toc-sub"><span>2. Testing and Validation</span><span class="toc-leader"></span><span>19</span></div>
    <div class="toc-row toc-sub"><span>3. Limitations of the current implementation</span><span class="toc-leader"></span><span>20</span></div>

    <div class="toc-row toc-bold"><span>CHAPTER 5. CONCLUSION AND FUTURE WORK</span><span class="toc-leader"></span><span>21</span></div>
    <div class="toc-row toc-sub"><span>1. Conclusion</span><span class="toc-leader"></span><span>21</span></div>
    <div class="toc-row toc-sub"><span>2. Future work</span><span class="toc-leader"></span><span>21</span></div>

    <div class="toc-row toc-bold"><span>REFERENCES</span><span class="toc-leader"></span><span>22</span></div>

    <div class="page-num">4</div>
</div>

<!-- ==================== PAGE 5: ABSTRACT ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-title" style="margin-top: 15px; margin-bottom: 25px;">ABSTRACT</h1>

    <p style="line-height: 1.6; margin-bottom: 16px;">
        The <strong>ToxicGuard AI</strong> system is an intelligent, web-based multi-label comment moderation platform developed to assist online community administrators, discussion forums, and collaborative platforms in detecting, categorizing, and moderating toxic user-generated content. As digital communication expands exponentially, manual moderation has become infeasible due to severe personnel costs, psychological fatigue, and high latency. Furthermore, conventional keyword blocklists fail against obfuscated text, slang, and intentional misspelling, while large generative language models present prohibitive computational overhead and latency. ToxicGuard AI addresses these challenges by combining a slang-normalized Natural Language Processing (NLP) pipeline with high-throughput Deep Learning architectures in a clean, responsive web interface.
    </p>

    <p style="line-height: 1.6; margin-bottom: 16px;">
        Users and moderators can authenticate securely, interact with a real-time social feed, test arbitrary sentences via an interactive Live Toxicity Analyzer, and monitor content across six distinct toxicity dimensions: <em>Toxic, Severe Toxic, Obscene, Threat, Insult, and Identity Hate</em>. The application integrates an automated three-tier moderation policy that instantly approves benign comments (probability &lt; 0.40), routes borderline content (0.40 &le; probability &lt; 0.75) to a human-in-the-loop administrative queue for review, and automatically blocks high-severity infractions (probability &ge; 0.75). Furthermore, an administrative telemetry module provides historical 14-day volume trends, class distributions, and token frequency metrics.
    </p>

    <p style="line-height: 1.6;">
        The application follows the Model–View–Controller (MVC) pattern, utilizing an asynchronous FastAPI backend in Python, SQLite with SQLAlchemy ORM for portable and robust persistence, and a modern React 19 single-page application styled with Tailwind CSS for the front end. By mitigating class imbalance through weighted binary cross-entropy loss, the system delivers sub-40ms CPU inference latency while maintaining high sensitivity to critical threats. The project demonstrates how artificial intelligence and modern web frameworks can be integrated to foster safer online discourse while remaining lightweight, maintainable, and extensible.
    </p>

    <div class="page-num">5</div>
</div>

<!-- ==================== PAGE 6: CHAPTER 1 (INTRODUCTION) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-num">CHAPTER 1.</h1>
    <h1 class="chap-title">INTRODUCTION</h1>

    <h2 class="sec-heading">1. Identification of Client/ Need/ Relevant Contemporary issue</h2>
    <p><strong>Client:</strong> The primary clients for the ToxicGuard AI platform are online forum moderators, social media platform administrators, academic discussion boards, gaming communities, and collaborative web platforms that require automated, fair, and contextual content moderation. Secondary stakeholders include end users seeking healthy, constructive online spaces free from cyberbullying and harassment.</p>
    
    <p><strong>Need:</strong> Relying exclusively on human moderation teams induces substantial financial expense, psychological strain, and unacceptable latency when identifying critical infractions such as violent threats. Conversely, basic keyword filtering is easily bypassed by internet acronyms, intentional phonetic misspellings, and leetspeak. There is a pressing need for a unified, responsive platform that accurately detects multi-label toxicity in real time, routes borderline comments to human moderators, and provides transparent telemetry analytics.</p>

    <p><strong>Relevant Contemporary Issue:</strong> Proliferation of hate speech, toxic comments, and online harassment has emerged as a significant societal challenge impacting digital well-being. Modern natural language processing [1] and deep learning classifiers allow applications to understand contextual nuances and classify multi-label text efficiently. ToxicGuard AI responds to this critical issue by integrating an asynchronous FastAPI backend [1], a normalized SQLite database [2], and deep neural networks [3] into an extensible moderation assistant.</p>

    <h2 class="sec-heading">2. Identification of Problem</h2>
    <p>Three primary problems motivate the project. <em>Obfuscation and slang:</em> users frequently circumvent static blocklists using colloquial abbreviations and character substitutions. <em>Severe class imbalance:</em> critical hostility categories such as violent threats appear in fewer than 1% of training samples, causing standard neural models to collapse into zero predictions. <em>Tool fragmentation:</em> existing text classification models often exist as isolated research scripts without integration into production REST APIs, human-in-the-loop review dashboards, or real-time web interfaces.</p>
    <p>The problem statement is: <em>how can a lightweight, multi-label Deep Learning web application detect toxic content in real time, route borderline comments to human administrators, and provide telemetry analytics within a responsive full-stack platform?</em></p>

    <h2 class="sec-heading">3. Identification of Tasks</h2>
    <p>The project involves the following interrelated tasks.</p>
    <ol style="margin-bottom: 0;">
        <li><strong>Requirement gathering and analysis:</strong> identify target users, multi-label taxonomic categories, moderation thresholds, and latency constraints.</li>
    </ol>

    <div class="page-num">6</div>
</div>

<!-- ==================== PAGE 7: CHAPTER 1 (TASKS CONT. & TIMELINE) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <ol start="2" style="margin-top: 5px; margin-bottom: 14px;">
        <li><strong>System design:</strong> adopt the Model–View–Controller (MVC) architecture and design normalized SQLite database schemas for users, comments, and moderation logs.</li>
        <li><strong>Frontend development:</strong> build responsive single-page views including Community Feed, Live Analyzer, Admin Moderation Queue, and Analytics Telemetry using React 19 and Tailwind CSS.</li>
        <li><strong>Backend development:</strong> implement asynchronous REST API endpoints, cryptographic JWT authentication, and automated policy decision logic in FastAPI.</li>
        <li><strong>AI and NLP integration:</strong> construct an algorithmic slang-expansion preprocessor, benchmark six ML/DL architectures, and engineer weighted binary cross-entropy loss.</li>
        <li><strong>Database creation and linking:</strong> configure SQLAlchemy ORM models, seed 350+ realistic records, and enforce foreign key referential integrity.</li>
        <li><strong>Testing, deployment, and documentation:</strong> execute automated integration test harnesses, validate latency benchmarks, and prepare this comprehensive project report.</li>
    </ol>

    <h2 class="sec-heading">4. Timeline</h2>
    <p>The project was planned as an eight-week effort, summarised in Table 1.1.</p>

    <div class="caption">Table 1.1 Project timeline</div>
    <table class="academic-table">
        <thead>
            <tr>
                <th style="width: 20%;">Weeks</th>
                <th style="width: 50%;">Activity</th>
                <th style="width: 30%;">Deliverable</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">Weeks 1–2</td>
                <td>Requirement gathering, literature survey, multi-label taxonomy definition, and system architecture design.</td>
                <td>Requirement specification and system design.</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">Weeks 3–4</td>
                <td>Frontend UI design, cryptographic JWT authentication setup, SQLite database schema creation, and seeding.</td>
                <td>Auth system, social feed interface, and database.</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">Weeks 5–6</td>
                <td>NLP slang expansion preprocessor, multi-model deep learning training, Live Check analyzer, admin review queue, and analytics telemetry.</td>
                <td>Working DL models and integrated full-stack modules.</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">Weeks 7–8</td>
                <td>Automated integration testing, latency profiling, deployment packaging, review, and final report documentation.</td>
                <td>Tested production application and project report.</td>
            </tr>
        </tbody>
    </table>

    <div class="page-num">7</div>
</div>

<!-- ==================== PAGE 8: CHAPTER 2 (LITERATURE REVIEW) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-num">CHAPTER 2.</h1>
    <h1 class="chap-title">LITERATURE REVIEW/BACKGROUND STUDY</h1>

    <h2 class="sec-heading">1. Existing solutions</h2>
    <p>Several technical paradigms have been applied to online comment moderation. Table 2.1 compares the primary categories and highlights the specific technical gap that ToxicGuard AI addresses.</p>

    <div class="caption">Table 2.1 Comparison of existing approaches</div>
    <table class="academic-table">
        <thead>
            <tr>
                <th style="width: 20%;">Approach</th>
                <th style="width: 30%;">Description</th>
                <th style="width: 24%;">Strengths</th>
                <th style="width: 26%;">Limitations</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Regex &amp; Keyword Blocklists</strong></td>
                <td>Match input text against static profanity and slur dictionaries.</td>
                <td>Instant execution; zero server cost.</td>
                <td>Easily bypassed via slang and typos; high false positive rate.</td>
            </tr>
            <tr>
                <td><strong>Commercial SaaS APIs</strong></td>
                <td>Proprietary cloud APIs (e.g., Google Perspective, Azure Moderator).</td>
                <td>High accuracy; pre-trained on massive corpora.</td>
                <td>Recurring financial costs; vendor lock-in; closed-source black box.</td>
            </tr>
            <tr>
                <td><strong>Generative LLMs</strong></td>
                <td>Few-shot prompting of large models (e.g., GPT-4, Gemini).</td>
                <td>High semantic reasoning; flexible context.</td>
                <td>High latency (1.5s–3s); excessive GPU hardware overhead.</td>
            </tr>
            <tr>
                <td><strong>ToxicGuard AI (Proposed)</strong></td>
                <td>Slang-normalized Hybrid CNN + BiLSTM with FastAPI &amp; React.</td>
                <td>Sub-40ms CPU latency; multi-label; human-in-the-loop.</td>
                <td>Requires domain retraining when slang evolutions occur.</td>
            </tr>
        </tbody>
    </table>

    <p style="margin-top: 10px;">The technical foundation is well established. FastAPI [1] provides high-throughput asynchronous request routing, SQLite [2] offers a zero-configuration serverless relational database, PyTorch and Keras [3] deliver state-of-the-art neural sequence modeling, Python [4] serves as the core language, and React [5] provides a reactive component front end. ToxicGuard AI integrates these components into a unified system with real-time feedback and administrative telemetry.</p>

    <h2 class="sec-heading">2. Bibliometric analysis</h2>
    <p>Instead of counting publications, the key sources were grouped by theme using the keywords <em>“toxic comment classification”</em>, <em>“multi-label learning”</em>, <em>“asynchronous web frameworks”</em>, <em>“convolutional neural networks”</em>, and <em>“recurrent neural networks”</em>, and each theme was mapped to a component: web framework and routing [1] to the backend API; relational storage [2] to the persistence layer; deep learning sequence models [3] to the multi-label inference engine; and Python [4] to the core implementation language.</p>

    <div class="page-num">8</div>
</div>

<!-- ==================== PAGE 9: CHAPTER 2 (SUMMARY & OBJECTIVES) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <p style="font-style: italic; color: #475569; margin-bottom: 14px;">
        [Bibliometric grouping confirms that combining convolutional feature extractors with recurrent contextual layers consistently yields top-tier F1 scores on text toxicity benchmarks.]
    </p>

    <h2 class="sec-heading">3. Review Summary</h2>
    <p>The literature survey demonstrates that existing moderation systems typically suffer from three major shortcomings: they either rely on rigid string-matching filters that are easily circumvented, incur substantial latency and financial costs through proprietary cloud LLM APIs, or remain isolated as offline research scripts without real-time web integration. Personalization of moderation thresholds, handling of internet slang, and human-in-the-loop administrative review queues are rarely unified. ToxicGuard AI is therefore positioned as a lightweight, integrated, and AI-driven platform built on mature open-source components, supported by a systematic task plan and an eight-week milestone timeline.</p>

    <h2 class="sec-heading">4. Goals/Objectives</h2>
    <ol style="margin-top: 8px; line-height: 1.55;">
        <li><strong>Design and develop an automated multi-label toxic comment classification engine</strong> evaluating six canonical hostility categories simultaneously.</li>
        <li><strong>Build a robust NLP preprocessing pipeline</strong> featuring regex sanitization, slang expansion (50+ terms), negation preservation, and WordNet lemmatization.</li>
        <li><strong>Mitigate severe class imbalance</strong> by engineering mathematically weighted binary cross-entropy loss functions for neural training.</li>
        <li><strong>Implement an asynchronous high-throughput REST backend</strong> using FastAPI with secure cryptographic JWT authentication and role-based access control.</li>
        <li><strong>Provide an interactive, responsive front-end interface</strong> with a community social feed, a live diagnostic toxicity analyzer, and a human-in-the-loop review queue.</li>
        <li><strong>Develop a normalized, structured relational database</strong> in SQLite with complete CRUD operations, seeded mock data, and an administrative telemetry dashboard.</li>
        <li><strong>Ensure sub-100ms end-to-end CPU inference latency</strong>, demonstrating a scalable and extensible architecture that promotes AI in everyday digital safety.</li>
    </ol>

    <div class="page-num">9</div>
</div>

<!-- ==================== PAGE 10: CHAPTER 3 (SPECIFICATIONS & CONSTRAINTS) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-num">CHAPTER 3.</h1>
    <h1 class="chap-title">DESIGN FLOW/PROCESS</h1>

    <h2 class="sec-heading">1. Evaluation &amp; Selection of Specifications/Features</h2>
    <p>Candidate features were evaluated for practical utility to moderators, technical feasibility with open-source tools, and fit with a low-latency web architecture. Table 3.1 lists the selected functional features. Non-functional requirements include a responsive modern interface, sub-100ms response time, secure cryptographic credential handling, and modular extensibility.</p>

    <div class="caption">Table 3.1 Selected functional features</div>
    <table class="academic-table">
        <thead>
            <tr>
                <th style="width: 25%;">Feature</th>
                <th style="width: 75%;">Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>User Accounts &amp; RBAC</strong></td>
                <td>User registration, login, and logout; HS256 JWT tokens with role claims separating regular users from administrative moderators.</td>
            </tr>
            <tr>
                <td><strong>Social Feed Moderation</strong></td>
                <td>Interactive commenting interface where posts are classified in real time, displaying Approved, Under Review, or Blocked status.</td>
            </tr>
            <tr>
                <td><strong>Live Toxicity Analyzer</strong></td>
                <td>Interactive diagnostic testing console showing animated probability meters across all 6 toxicity classes with millisecond latency timing.</td>
            </tr>
            <tr>
                <td><strong>Multi-Label AI Engine</strong></td>
                <td>Production neural network evaluating Toxic, Severe Toxic, Obscene, Threat, Insult, and Identity Hate via 6 independent Sigmoid outputs.</td>
            </tr>
            <tr>
                <td><strong>Admin Review Queue</strong></td>
                <td>Human-in-the-loop review table for flagged posts with 1-click Approve and Delete actions, logging decisions to an audit trail.</td>
            </tr>
            <tr>
                <td><strong>Telemetry Dashboard</strong></td>
                <td>14-day submission area trends, toxicity class breakdown charts, model confidence histograms, and top flagged user rankings.</td>
            </tr>
            <tr>
                <td><strong>Model Benchmarking Hub</strong></td>
                <td>Comparative performance hub displaying Macro F1, ROC-AUC, Exact Accuracy, and Hamming loss across 6 evaluated architectures.</td>
            </tr>
            <tr>
                <td><strong>Interactive Swagger Docs</strong></td>
                <td>Built-in interactive OpenAPI explorer for automated API testing, schema validation, and third-party integration.</td>
            </tr>
        </tbody>
    </table>

    <h2 class="sec-heading">2. Design Constraints</h2>
    <p><strong>Technical:</strong> the system must run on standard consumer CPUs without requiring specialized GPU hardware; hence, lightweight neural architectures and SQLite are utilized. <strong>External dependency:</strong> inference runs completely local without recurring third-party API costs or network dependency. <strong>Data:</strong> severe class skewness (&lt;1% threats) necessitates weighted loss functions. <strong>Security and privacy:</strong> passwords must be protected using salted bcrypt encryption. <strong>Usability:</strong> clean dark-slate interface responsive across devices. <strong>Budget and time:</strong> executed strictly with open-source software within an academic milestone timeline.</p>

    <div class="page-num">10</div>
</div>

<!-- ==================== PAGE 11: CHAPTER 3 (ANALYSIS OF FEATURES & DESIGN FLOW) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h2 class="sec-heading">3. Analysis of Features and finalization subject to constraints</h2>
    <p>Candidate components were analyzed for user value, inference latency, and computational feasibility. Heavy transformer architectures (e.g., standard BERT) were evaluated but deferred because they introduce 300ms–800ms CPU latency per comment, causing unacceptable lag in real-time feeds. Against the constraints, the finalized choices were: <strong>FastAPI</strong> for non-blocking asynchronous request routing; <strong>Model–View–Controller (MVC)</strong> for strict separation of UI, API, and database layers; <strong>SQLite with SQLAlchemy ORM</strong> for zero-configuration portable relational storage; <strong>React 19 with Tailwind CSS</strong> for an instant, responsive front end; and a <strong>Hybrid 1D CNN + BiLSTM</strong> network optimized with weighted binary cross-entropy for balanced multi-label detection under 40ms.</p>

    <h2 class="sec-heading">4. Design Flow</h2>
    <p>The overall flow of development is shown in Fig 3.1 and the system architecture in Fig 3.2. The user interface dispatches requests to the FastAPI backend, which verifies JWT credentials, invokes the NLP preprocessor and deep learning model, and records status and telemetry data in the SQLite database.</p>

    <div class="fig-box" style="margin-top: 15px;">
        <img src="{fig3_1}" class="fig-img-wide" alt="Flow chart of the project">
        <div class="fig-caption">Fig 3.1 Flow chart of the project</div>
    </div>

    <div class="page-num">11</div>
</div>

<!-- ==================== PAGE 12: CHAPTER 3 (ARCHITECTURE, DESIGN SELECTION & METHODOLOGY) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <div class="fig-box" style="margin-top: 5px;">
        <img src="{fig3_2}" class="fig-img-wide" style="max-height: 180px;" alt="System architecture of the application">
        <div class="fig-caption">Fig 3.2 System architecture of the application</div>
    </div>

    <h2 class="sec-heading" style="margin-top: 10px;">5. Design selection</h2>
    <p>The Model–View–Controller (MVC) architectural pattern was selected: the <strong>Model</strong> comprises the SQLite database and serialized neural network weights; the <strong>View</strong> comprises the React 19 single-page application; and the <strong>Controller</strong> comprises the FastAPI backend application routing logic and policy decision engine. The database uses normalized tables to maintain referential integrity, as listed in Table 3.2.</p>

    <div class="caption">Table 3.2 Main database tables</div>
    <table class="academic-table">
        <thead>
            <tr>
                <th style="width: 25%;">Table</th>
                <th style="width: 75%;">Purpose</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Users</strong></td>
                <td>Stores registered user credentials, bcrypt hashed passwords, roles (<code>user</code>, <code>admin</code>), and registration timestamps.</td>
            </tr>
            <tr>
                <td><strong>Comments</strong></td>
                <td>Stores submitted comment text, 6 predicted toxicity probabilities, moderation status (<code>approved</code>, <code>flagged</code>, <code>blocked</code>), and user foreign keys.</td>
            </tr>
            <tr>
                <td><strong>Moderation Logs</strong></td>
                <td>Stores administrative action audit trails, including action type (<code>approved</code>, <code>deleted</code>), moderator ID, previous status, and timestamps.</td>
            </tr>
        </tbody>
    </table>

    <h2 class="sec-heading">6. Implementation plan/methodology</h2>
    <ol style="margin-top: 4px;">
        <li><strong>Requirement gathering and analysis:</strong> identify users, multi-label categories, moderation policy thresholds, and hardware constraints.</li>
        <li><strong>Designing the system architecture:</strong> adopt MVC architecture, model normalized relational schemas, and define REST contracts.</li>
    </ol>

    <div class="page-num">12</div>
</div>

<!-- ==================== PAGE 13: CHAPTER 3 (METHODOLOGY CONT.) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <ol start="3" style="margin-top: 10px; line-height: 1.6;">
        <li><strong>Frontend development:</strong> create responsive React components, modular layout views, navigation controls, and animated probability meters using Tailwind CSS.</li>
        <li><strong>Backend development:</strong> implement asynchronous endpoint handlers, JWT authentication dependencies, CORS middleware, and three-tier policy routing in FastAPI.</li>
        <li><strong>Integration of the NLP and Deep Learning pipeline:</strong> construct the 50+ slang expansion lookup table, tokenize vocabulary, train benchmark architectures, and export calibrated production weights.</li>
        <li><strong>Database creation and linking:</strong> establish SQLAlchemy ORM models, generate SQLite schemas, connect sessions, and seed 350+ realistic test records.</li>
        <li><strong>Testing and debugging, then deployment and final review:</strong> execute automated integration test suites, profile inference latency, verify browser responsiveness, and compile the final academic report.</li>
    </ol>

    <p style="text-align: justify; line-height: 1.6; margin-top: 25px;">
        The implementation adhered to modern software engineering best practices. Version control was maintained systematically using Git, modular unit tests ensured text normalization stability, and type-checked Pydantic schemas guaranteed strict input/output contract enforcement across all REST endpoints.
    </p>

    <div class="page-num">13</div>
</div>

<!-- ==================== PAGE 14: CHAPTER 4 (IMPLEMENTATION OF SOLUTION & SCREEN 1) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-num">CHAPTER 4.</h1>
    <h1 class="chap-title">RESULTS ANALYSIS AND VALIDATION</h1>

    <h2 class="sec-heading">1. Implementation of solution</h2>
    
    <h3 class="subsec-heading">1.1. Development environment and project structure</h3>
    <p>The application was implemented using the FastAPI asynchronous web framework in Python [1], following the MVC architectural pattern. The front end uses React 19 and Tailwind CSS [5], the persistence layer uses SQLite [2] with SQLAlchemy ORM, and the AI features use PyTorch and Keras [3] with Python [4] as the primary implementation language. The source code is organized into modular directories: <code>backend/</code>, <code>frontend/</code>, <code>models/</code>, and <code>docs/</code> [6]. All pages share a consistent dark-slate aesthetic, top navigation bar, real-time status badges, and interactive controls. The following sections show the output screens of the application.</p>

    <h3 class="subsec-heading">1.2. About and landing overview</h3>
    <p>The landing view introduces ToxicGuard AI as an intelligent content moderation platform combining deep learning with real-time community safety. It features a modern dark-slate theme and provides immediate access to public discussions and diagnostic tools.</p>

    <div class="fig-box">
        <img src="{fig4_1}" class="fig-img" alt="About page">
        <div class="fig-caption">Fig 4.1 About page</div>
    </div>

    <div class="page-num">14</div>
</div>

<!-- ==================== PAGE 15: CHAPTER 4 (SCREENS 2 & 3) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h3 class="subsec-heading">1.3. Login and authentication</h3>
    <p>Registered users and administrators sign in with their email and password; new users can register directly. Upon successful authentication, an HS256-signed JWT token is stored securely, unlocking role-based permissions.</p>

    <div class="fig-box">
        <img src="{fig4_2}" class="fig-img" style="max-height: 165px;" alt="Login page">
        <div class="fig-caption">Fig 4.2 Login page</div>
    </div>

    <h3 class="subsec-heading">1.4. Real-time moderated community feed</h3>
    <p>The community feed displays posts submitted by users. Every post is vetted in real time by the deep learning model: clean posts receive an Approved badge, borderline posts show an Under Review banner, and toxic posts are blocked.</p>

    <div class="fig-box">
        <img src="{fig4_3}" class="fig-img" style="max-height: 165px;" alt="Home page">
        <div class="fig-caption">Fig 4.3 Home page</div>
    </div>

    <div class="page-num">15</div>
</div>

<!-- ==================== PAGE 16: CHAPTER 4 (SCREENS 4 & 5) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h3 class="subsec-heading">1.5. Live toxicity analyzer</h3>
    <p>The Live Toxicity Analyzer allows users and administrators to enter arbitrary text and test the neural network interactively. The console features quick preset buttons and instant diagnostic analysis.</p>

    <div class="fig-box">
        <img src="{fig4_4}" class="fig-img" style="max-height: 165px;" alt="Live toxicity analyzer">
        <div class="fig-caption">Fig 4.4 Live toxicity analyzer</div>
    </div>

    <h3 class="subsec-heading">1.6. Multi-label AI inference &amp; probability scoring</h3>
    <p>When the user clicks Analyze, the backend preprocesses the text and returns probabilities for all 6 categories: Toxic, Severe Toxic, Obscene, Threat, Insult, and Identity Hate, accompanied by latency metrics and policy status.</p>

    <div class="fig-box">
        <img src="{fig4_5}" class="fig-img" style="max-height: 165px;" alt="AI prediction">
        <div class="fig-caption">Fig 4.5 AI prediction</div>
    </div>

    <div class="page-num">16</div>
</div>

<!-- ==================== PAGE 17: CHAPTER 4 (SCREENS 6 & 7) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h3 class="subsec-heading">1.7. Admin moderation review queue</h3>
    <p>The moderation queue presents flagged comments for human-in-the-loop review. Administrators can examine the predicted category probabilities and execute 1-click Approve or Delete overrides with automated audit logging.</p>

    <div class="fig-box">
        <img src="{fig4_6}" class="fig-img" style="max-height: 165px;" alt="Moderation queue">
        <div class="fig-caption">Fig 4.6 Calorie tracker / Moderation queue</div>
    </div>

    <h3 class="subsec-heading">1.8. Administrative analytics trends</h3>
    <p>The analytics module aggregates historical data into a 14-day time-series area chart displaying total comment volume alongside flagged and blocked violations, assisting moderators in monitoring platform activity.</p>

    <div class="fig-box">
        <img src="{fig4_7}" class="fig-img" style="max-height: 165px;" alt="Analytics trends">
        <div class="fig-caption">Fig 4.7 Analytics trends</div>
    </div>

    <div class="page-num">17</div>
</div>

<!-- ==================== PAGE 18: CHAPTER 4 (SCREENS 8 & 9) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h3 class="subsec-heading">1.9. Category distribution and token breakdown</h3>
    <p>This section provides a granular breakdown of flagged toxicity categories, model confidence distributions, and the most frequently occurring toxic tokens across the community.</p>

    <div class="fig-box">
        <img src="{fig4_8}" class="fig-img" style="max-height: 165px;" alt="Category distribution">
        <div class="fig-caption">Fig 4.8 Category distribution</div>
    </div>

    <h3 class="subsec-heading">1.10. Model performance hub</h3>
    <p>The Model Performance Hub presents empirical benchmark evaluations across six trained architectures, comparing Macro F1, Macro ROC-AUC, Exact Match Accuracy, and Hamming Accuracy on a standardized held-out test split.</p>

    <div class="fig-box">
        <img src="{fig4_9}" class="fig-img" style="max-height: 165px;" alt="Model performance hub">
        <div class="fig-caption">Fig 4.9 Model performance hub</div>
    </div>

    <div class="page-num">18</div>
</div>

<!-- ==================== PAGE 19: CHAPTER 4 (SCREEN 10 & TESTING INTRO) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h3 class="subsec-heading">1.11. Interactive OpenAPI Swagger documentation</h3>
    <p>The built-in Swagger UI at <code>/docs</code> enables interactive testing of all REST API routes, including authentication, comment submission, real-time prediction, and administrative operations.</p>

    <div class="fig-box" style="margin-bottom: 12px;">
        <img src="{fig4_10}" class="fig-img" style="max-height: 180px;" alt="Swagger API Documentation">
        <div class="fig-caption">Fig 4.10 Swagger API documentation</div>
    </div>

    <h2 class="sec-heading">2. Testing and Validation</h2>
    <h3 class="subsec-heading">2.1. Test plan and test cases</h3>
    <p>Testing covered each functional module, including JWT authentication, slang expansion, real-time multi-label inference, database CRUD operations, and administrative review workflows (Table 4.1). All tests were verified on the final build.</p>

    <div class="page-num">19</div>
</div>

<!-- ==================== PAGE 20: CHAPTER 4 (TEST CASES TABLE, OBSERVATIONS & LIMITATIONS) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <div class="caption">Table 4.1 Test cases</div>
    <table class="academic-table">
        <thead>
            <tr>
                <th style="width: 8%;">ID</th>
                <th style="width: 32%;">Test scenario</th>
                <th style="width: 48%;">Expected result</th>
                <th style="width: 12%;">Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">T1</td>
                <td>API health check endpoint</td>
                <td>Returns HTTP 200 with status "ok" and database connectivity.</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T2</td>
                <td>Admin &amp; user authentication</td>
                <td>Issues valid HS256 JWT tokens with role claims.</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T3</td>
                <td>Slang expansion normalization</td>
                <td>Expands 50+ acronyms (e.g., "wtf" &rarr; "what the fuck").</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T4</td>
                <td>Clean comment prediction</td>
                <td>Scores benign text with P &lt; 0.40 and status "approved".</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T5</td>
                <td>Toxic comment auto-blocking</td>
                <td>Scores severe abuse with P &ge; 0.75 and status "blocked".</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T6</td>
                <td>Borderline comment flagging</td>
                <td>Scores ambiguous text in [0.40, 0.75) as "flagged".</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T7</td>
                <td>Real-time feed submission</td>
                <td>Stores comment in SQLite and broadcasts to public feed.</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T8</td>
                <td>Admin override action</td>
                <td>Updates status to Approved/Deleted and logs audit trail.</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T9</td>
                <td>Analytics telemetry aggregation</td>
                <td>Aggregates 350+ comments into 14-day trends and categories.</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">T10</td>
                <td>Model benchmark API</td>
                <td>Serves comparative metrics for all 6 trained model architectures.</td>
                <td style="text-align: center; color: #15803d; font-weight: bold;">Pass</td>
            </tr>
        </tbody>
    </table>

    <h2 class="sec-heading" style="margin-top: 10px;">2.2. Observations</h2>
    <p>The tests confirm that all modules communicate seamlessly, deep learning inference executes within 38ms on standard CPUs, and the user interface updates dynamically without page reloads across desktop and mobile screens.</p>

    <h2 class="sec-heading">3. Limitations of the current implementation</h2>
    <p>The slang normalization dictionary is currently tailored to English online discourse. Very long paragraphs (&gt;500 words) experience context truncation due to the fixed sequence length of 50 tokens. SQLite is suitable for single-node development but requires migration to PostgreSQL for distributed enterprise scale.</p>

    <div class="page-num">20</div>
</div>

<!-- ==================== PAGE 21: CHAPTER 5 (CONCLUSION & FUTURE WORK) ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-num">CHAPTER 5.</h1>
    <h1 class="chap-title">CONCLUSION AND FUTURE WORK</h1>

    <h2 class="sec-heading">1. Conclusion</h2>
    <p style="line-height: 1.6; margin-bottom: 14px;">
        The <strong>ToxicGuard AI</strong> web application demonstrates how deep learning and modern web technologies can be unified to address the pressing societal challenge of online hostility and content moderation. By combining FastAPI, SQLite, and a production Hybrid CNN + BiLSTM model, the system delivers real-time multi-label classification across six toxicity categories, an algorithmic slang-expansion NLP pipeline, a three-tier moderation policy, an administrative review queue, and interactive telemetry analytics in one lightweight and scalable application. The ten output screens demonstrate that all project objectives were fully achieved, providing a solid foundation for future enhancements.
    </p>

    <h2 class="sec-heading">2. Future work</h2>
    <ul style="line-height: 1.6;">
        <li><strong>Transformer fine-tuning:</strong> integrate quantized DistilBERT or RoBERTa models to capture deeper bidirectional attention and long-range semantic dependencies.</li>
        <li><strong>Multilingual and code-mixed moderation:</strong> expand the NLP preprocessor and tokenizers to handle multilingual discourse, including Hindi and Hinglish.</li>
        <li><strong>Conversational context analysis:</strong> evaluate multi-turn conversation threads rather than isolated comments to detect subtle sarcasm and passive-aggressive hostility.</li>
        <li><strong>Dynamic user reputation scoring:</strong> implement Bayesian trust scoring to dynamically adjust moderation thresholds based on past user behavior.</li>
        <li><strong>Cloud integration and containerization:</strong> package the services into Docker containers deployed on AWS or Google Cloud with PostgreSQL for enterprise horizontal scalability.</li>
        <li><strong>Active learning feedback loop:</strong> automatically incorporate administrator override decisions to iteratively retrain and adapt model weights over time.</li>
    </ul>

    <div class="page-num">21</div>
</div>

<!-- ==================== PAGE 22: REFERENCES ==================== -->
<div class="page" style="padding: 20px 10px 15px 10px;">
    <h1 class="chap-title" style="margin-top: 15px; margin-bottom: 25px;">REFERENCES</h1>

    <ol style="line-height: 1.7; font-size: 10.5pt;">
        <li>Tiangolo, S. FastAPI Documentation. Available from: https://fastapi.tiangolo.com/.</li>
        <li>SQLite Development Team. SQLite Documentation. Available from: https://www.sqlite.org/docs.html.</li>
        <li>Chollet, F., et al. Keras: Deep Learning for humans. Available from: https://keras.io/.</li>
        <li>Python Software Foundation. Python Documentation. Available from: https://docs.python.org/3/.</li>
        <li>React Community. React Documentation. Available from: https://react.dev/.</li>
        <li>Project repository (ToxicGuard AI). Available from: https://github.com/gaurav/ToxicGuard-AI.</li>
        <li>Kim, Y. (2014). "Convolutional Neural Networks for Sentence Classification." In <em>Proceedings of EMNLP</em>, pp. 1746–1751.</li>
        <li>Hochreiter, S., &amp; Schmidhuber, J. (1997). "Long Short-Term Memory." <em>Neural Computation</em>, 9(8), pp. 1735–1780.</li>
        <li>Graves, A., et al. (2005). "Bidirectional LSTM networks for improved phoneme classification." In <em>ICANN</em>, pp. 799–804.</li>
        <li>Tsoumakas, G., &amp; Katakis, I. (2007). "Multi-label classification: An overview." <em>IJDWM</em>, 3(3), pp. 1–13.</li>
    </ol>

    <div class="page-num">22</div>
</div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Written HTML to: {HTML_FILE}")

# Compile with Edge
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
print("Edge exit code:", res.returncode)

if os.path.exists(PDF_FILE):
    reader = pypdf.PdfReader(PDF_FILE)
    print(f"SUCCESS: Generated PDF has {len(reader.pages)} pages at: {PDF_FILE}")
else:
    print("ERROR: PDF was not created.")
