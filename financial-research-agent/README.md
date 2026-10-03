# 📊 Financial Research & Reasoning Agent

A lightweight financial research assistant that allows users to upload a financial report in PDF format and ask questions about its contents.

The system extracts text and tables from the report, converts the content into a structured knowledge bundle, indexes it using vector search, and uses Gemini to generate answers grounded in the retrieved evidence.

## 🚀 Features

* 📄 Upload financial reports in PDF format
* 📝 Extract text page by page
* 📊 Extract tables from financial reports
* 🗂️ Create an OKF-style knowledge bundle
* 🔎 Semantic search using ChromaDB
* 🤖 Generate answers using Google Gemini
* 📚 Provide source references for retrieved information
* 🔄 Retry temporary Gemini API failures
* 💻 Simple Streamlit interface

## 🏗️ Architecture

```text
                    Financial PDF
                         │
                         ▼
              ┌─────────────────────┐
              │   PDF Processing    │
              │                     │
              │ Text + Tables       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   OKF Knowledge     │
              │      Bundle         │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │      ChromaDB       │
              │   Vector Retrieval  │
              └──────────┬──────────┘
                         │
                  Relevant Evidence
                         │
                         ▼
              ┌─────────────────────┐
              │       Gemini        │
              │   Research Agent    │
              └──────────┬──────────┘
                         │
                         ▼
                  Answer + Source
```

## 🔄 How It Works

### 1. Upload a PDF

The user uploads a financial report through the Streamlit interface.

### 2. Extract report content

The application extracts:

* Text from each page
* Tables from the report

### 3. Create knowledge bundle

The extracted information is organized into an OKF-style knowledge structure.

Example:

```text
knowledge/
└── <report_id>/
    ├── index.md
    ├── report.md
    ├── pages/
    │   ├── page-001.md
    │   ├── page-002.md
    │   └── ...
    └── tables/
        ├── page-001-table-001.md
        └── ...
```

### 4. Build the RAG index

The knowledge bundle is split into chunks.

Each chunk is converted into an embedding using Gemini and stored in ChromaDB.

### 5. Retrieve relevant evidence

When the user asks a question, the question is embedded and compared with the indexed report content.

The most relevant chunks are retrieved.

### 6. Generate the answer

Gemini receives:

* The user's question
* Retrieved evidence
* Source information

The model is instructed to answer using only the supplied evidence.

## 💬 Example

A user can upload a financial statement and ask:

```text
What is the net income for the year ended September 30, 2021?
```

The system retrieves the relevant section of the report and generates an evidence-grounded answer with the source page.

Example response:

```text
The net income was $945.

Source:
Sample-Financial-Statements-1.pdf - Page 2
```

## 🛠️ Tech Stack

| Technology    | Purpose                          |
| ------------- | -------------------------------- |
| Python        | Core application                 |
| Streamlit     | User interface                   |
| PyMuPDF       | PDF text extraction              |
| pdfplumber    | Table extraction                 |
| Google Gemini | Embeddings and answer generation |
| ChromaDB      | Vector database                  |
| python-dotenv | Environment variable management  |

## 📁 Project Structure

```text
financial-research-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py
│   ├── table_extractor.py
│   ├── okf_generator.py
│   ├── retriever.py
│   ├── research_agent.py
│   └── gemini_client.py
│
├── data/
│   ├── uploads/
│   └── chroma/
│
└── knowledge/
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/financial-research-agent.git
cd financial-research-agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Do **not** commit the `.env` file to GitHub.

### 5. Run the application

```powershell
python -m streamlit run app.py
```

The Streamlit application will open in your browser.

## 🔐 Environment & Git

The following files and directories should not be uploaded to GitHub:

```text
.env
.venv/
__pycache__/
data/chroma/
knowledge/
data/uploads/
```

These are excluded using `.gitignore`.

The `requirements.txt` file should be committed instead of the virtual environment.

## 🧠 Retrieval-Augmented Generation

This project uses a simple RAG pipeline:

```text
PDF
 ↓
Text + Tables
 ↓
Knowledge Bundle
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Similarity Search
 ↓
Relevant Evidence
 ↓
Gemini
 ↓
Answer
```

This allows the model to answer questions based on the uploaded report instead of relying only on its general knowledge.

## ⚠️ Current Limitations

This project intentionally focuses on a small and understandable MVP.

Current limitations include:

* Only PDF documents are supported
* Scanned PDFs requiring OCR are not supported
* Primarily designed for single-report analysis
* Retrieval quality depends on the extracted PDF content
* Complex financial calculations are not handled by a dedicated calculation engine
* Table extraction may not perfectly preserve complex PDF layouts

## 🔮 Possible Future Improvements

Potential improvements include:

* OCR support for scanned documents
* Better table extraction
* Multi-document analysis
* Improved retrieval strategies
* More advanced financial calculations
* Better source highlighting
* Evaluation using financial QA datasets

These are intentionally outside the current MVP scope.

## 🎯 Project Goal

The goal of this project is to demonstrate a practical **Retrieval-Augmented Generation (RAG) system for financial research**.

The project focuses on the complete pipeline:

```text
Document Processing
        ↓
Knowledge Representation
        ↓
Vector Retrieval
        ↓
Evidence-Grounded Generation
```

Rather than building a large multi-agent system, this project prioritizes a simple architecture that is easier to understand, test, and extend.

## 📜 License

This project is intended for educational and portfolio purposes.
