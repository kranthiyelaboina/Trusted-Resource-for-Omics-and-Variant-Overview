```markdown
# TROVO: Trusted Resource for Omics and Variant Overview

![TROVO Banner](https://via.placeholder.com/1200x300/2D9951/FFFFFF?text=TROVO)

**TROVO** is an intelligent platform that delivers comprehensive biological insights into human proteins — including structure, function, disease associations, and molecular interactions — through seamless, conversational exploration.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [About](#-about)

---

## 🔭 Overview

TROVO integrates data from multiple protein databases and leverages AI to provide researchers, students, and professionals with comprehensive insights about proteins in an intuitive interface. The platform combines traditional search-based exploration with a conversational AI assistant to make protein biology more accessible.

---

## ✨ Features

### 🔍 Protein Explorer

- **Smart Search**: Input any protein name or synonym and get refined search results
- **Comprehensive Information**: View detailed protein information from UniProt
- **3D Structure Visualization**: Interactive 3D models of protein structures from AlphaFold
- **AI-Generated Analysis**: Get AI-powered insights about protein function and properties
- **Drug Associations**: Discover drugs and compounds that interact with the selected protein

### 💬 Protein Chat

- **Conversational AI**: Ask questions about proteins in natural language
- **Context-Aware Responses**: The AI assistant considers your currently selected protein
- **Educational Insights**: Get detailed explanations about protein biology concepts
- **Interactive UI**: Smooth typing animations and intuitive chat interface

### 📋 Session Management

- **Multi-Tab Interface**: Create and manage multiple protein search tabs
- **Session Persistence**: Seamlessly switch between different protein searches
- **Custom Naming**: Rename tabs for better organization

---

## 🛠️ Technology Stack

### Backend

- Python 3.9+
- Flask
- Flask-CORS
- Google Generative AI (Gemini API)

### Frontend

- HTML5 / CSS3 / JavaScript
- 3Dmol.js

### Data Sources

- UniProt
- AlphaFold DB
- ChEMBL

### Deployment

- Vercel

---

## 📥 Installation

### Prerequisites

- Python 3.9 or higher
- Node.js and npm (optional, for development)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TROVO.git
   cd TROVO
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```
   # Create a .env file with the following variables
   GEMINI_API_KEY=your_gemini_api_key
   SECRET_KEY=your_secret_key
   FLASK_DEBUG=True
   ```

5. **Run the application**
   ```bash
   # For Flask web interface
   python app.py

   # For Streamlit interface
   streamlit run streamlit_app.py
   ```

---

## 🚀 Usage

### Web Interface

1. **Search for Proteins**
   - Navigate to the "Protein Explorer" tab
   - Enter a protein name (e.g., "Insulin", "TP53", "EGFR")
   - View detailed protein information

2. **Chat with the AI Assistant**
   - Navigate to the "Protein Chat" tab
   - Ask questions about proteins or biology in general
   - Context is applied if you've selected a protein

3. **Manage Multiple Searches**
   - Use sidebar to switch between searches
   - Create new tabs and rename them as needed

---

## 📚 API Reference

| Endpoint                                      | Method | Description                               |
|----------------------------------------------|--------|-------------------------------------------|
| `/api/protein/{protein_name}`                | GET    | Get basic protein information             |
| `/api/protein/{protein_name}/analysis`       | GET    | Get AI-generated protein analysis         |
| `/api/protein/{protein_name}/structure`      | GET    | Get protein 3D structure data             |
| `/api/protein/{protein_name}/drugs`          | GET    | Get drug associations                     |
| `/api/refine-query`                          | POST   | Refine a protein query using AI           |
| `/api/conversation`                          | POST   | Process a chat conversation about protein |

### Example (Python)
```python
import requests

# Get protein information
response = requests.get("https://amino-verse-backend1.vercel.app/api/protein/insulin")
data = response.json()
print(data)
```

---

## 📁 Project Structure

```
Amino_Verse/
├── app.py                      # Main Flask app
├── config.py                   # Configurations
├── index.html                  # Web UI
├── requirements.txt            # Dependencies
├── scripts.js                  # JS frontend logic
├── streamlit_app.py            # Streamlit app
├── styles.css                  # CSS styles
├── vercel.json                 # Vercel deployment settings
├── models/                     # Data models (if any)
├── routes/                     # API routes
│   ├── __init__.py
│   └── api.py
├── services/                   # Data service integrations
│   ├── __init__.py
│   ├── alphafold_service.py
│   ├── chembl_service.py
│   ├── gemini_service.py
│   └── uniprot_service.py
└── utils/                      # Utilities
    ├── __init__.py
    └── response_formatter.py
```

---

## 🤝 Contributing

We welcome contributions from the community!

1. Fork the repo
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more info.

---

## 🏫 About

Built with ❤️ for the Mahendra University Hackathon by [Your Team Name].

For questions or support, please [open an issue](https://github.com/yourusername/TROVO/issues).
```

Let me know if you'd like me to auto-fill things like your GitHub username, team name, or provide a custom banner image.
