---

# TROVO: Trusted Resource for Omics and Variant Overview

TROVO is an intelligent platform that delivers comprehensive biological insights into human proteins — including structure, function, disease associations, and molecular interactions — through a seamless, conversational interface.

## Table of Contents

- Overview  
- Features  
- Technology Stack  
- Installation  
- Usage  
- API Reference  
- Project Structure  
- Contributing  
- License  
- About  

---

## Overview

TROVO integrates data from multiple protein databases and uses AI to help users explore proteins easily. It supports both traditional search-based exploration and a conversational assistant for intuitive learning and discovery.

---

## Features

### Protein Explorer

- Search proteins by name or synonym
- Get detailed information from UniProt
- View 3D protein structures using AlphaFold data
- Receive AI-generated insights about the protein
- See related drug and compound associations (from ChEMBL)

### Protein Chat

- Ask questions in natural language
- AI assistant responds using protein context
- Useful for learning protein biology concepts
- Interactive, clean chat UI

### Session Management

- Manage multiple protein search tabs
- Switch between sessions with ease
- Rename tabs for better organization

---

## Technology Stack

### Backend

- Python 3.9+
- Flask (Web Framework)
- Flask-CORS
- Google Gemini API (Generative AI)

### Frontend

- HTML / CSS / JavaScript
- 3Dmol.js (for 3D structure)

### Data Sources

- UniProt
- AlphaFold DB
- ChEMBL

### Deployment

- Vercel

---

## Installation

### Requirements

- Python 3.9+
- Node.js and npm (optional)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/TROVO.git
   cd TROVO
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables:
   Create a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   SECRET_KEY=your_secret_key
   FLASK_DEBUG=True
   ```

5. Run the application:
   ```
   # For Flask
   python app.py

   # Optional Streamlit version
   streamlit run streamlit_app.py
   ```

---

## Usage

1. Open the web interface.
2. Use the "Protein Explorer" to search for a protein (e.g., "TP53").
3. Use "Protein Chat" to ask questions related to the selected protein.
4. Open multiple tabs to compare or explore different proteins.
5. Rename tabs for better organization.

---

## API Reference

| Endpoint                                  | Method | Description                                 |
|------------------------------------------|--------|---------------------------------------------|
| `/api/protein/{protein_name}`            | GET    | Get basic protein data                      |
| `/api/protein/{protein_name}/analysis`   | GET    | AI-generated analysis of the protein        |
| `/api/protein/{protein_name}/structure`  | GET    | Get 3D structure info                       |
| `/api/protein/{protein_name}/drugs`      | GET    | List drugs associated with the protein      |
| `/api/refine-query`                      | POST   | Refine a protein search query using AI      |
| `/api/conversation`                      | POST   | Ask a question to the protein chatbot       |

### Example

```python
import requests

response = requests.get("https://amino-verse-backend1.vercel.app/api/protein/insulin")
print(response.json())
```

---

## Project Structure

```
Amino_Verse/
├── app.py
├── config.py
├── index.html
├── requirements.txt
├── scripts.js
├── streamlit_app.py
├── styles.css
├── vercel.json
├── models/
├── routes/
│   ├── __init__.py
│   └── api.py
├── services/
│   ├── alphafold_service.py
│   ├── chembl_service.py
│   ├── gemini_service.py
│   └── uniprot_service.py
└── utils/
    └── response_formatter.py
```

---

## Contributing

1. Fork the repository.
2. Create a branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to your branch: `git push origin feature-name`
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## About

Created for Mahendra University Hackathon.  
Built by [Your Team Name].

If you have any questions or need support, open an issue at:  
https://github.com/yourusername/TROVO/issues

---

Let me know if you’d like this automatically saved in a `README.md` file or if you want a shortened version too.
