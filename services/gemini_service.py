import google.generativeai as genai
from flask import current_app
import json

def initialize_gemini():
    """Initialize the Gemini API with the API key."""
    try:
        from config import Config
        genai.configure(api_key=Config.GEMINI_API_KEY)
        return True
    except Exception as e:
        print(f"Error initializing Gemini API: {e}")
        return False

def query_gemini(prompt):
    """Query Gemini AI with a prompt and return the response."""
    try:
        initialize_gemini()
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error querying Gemini API: {e}")
        return None

def refine_protein_query(user_query):
    """Use Gemini to refine and understand a protein query."""
    prompt = f"""
    I'm searching for protein information. The user entered: "{user_query}"
    
    Please analyze this query and provide:
    1. The most likely protein name this refers to
    2. Any common alternative names
    3. Known UniProt IDs if you have them (not required)
    4. A brief description of what this protein does
    
    Format as JSON with keys: "protein_name", "alternative_names", "uniprot_ids", "description"
    """
    
    response = query_gemini(prompt)
    
    try:
        return json.loads(response)
    except (json.JSONDecodeError, TypeError):
        # If Gemini doesn't return valid JSON, return a simple structure
        return {
            "protein_name": user_query,
            "alternative_names": [],
            "uniprot_ids": [],
            "description": "No description provided."
        }

def generate_protein_analysis(protein_name, uniprot_id):
    """Generate detailed analysis about a protein using Gemini."""
    prompt = f"""
    Provide a detailed analysis of the protein {protein_name} (UniProt ID: {uniprot_id}).
    
    Include:
    1. Main biological functions
    2. Associated diseases or medical relevance
    3. Key structural features
    4. Evolutionary significance
    5. Current research importance
    
    Format the response with markdown headers and bullet points. Keep it concise and scientifically accurate.
    """
    
    return query_gemini(prompt)