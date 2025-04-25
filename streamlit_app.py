import streamlit as st
import requests
import json
import pandas as pd
import py3Dmol
from stmol import showmol
import streamlit.components.v1 as components

# Configure page
st.set_page_config(page_title="AminoVerse", page_icon="🧬", layout="wide")

# API base URL - update this when deployed
API_BASE_URL = "http://localhost:5000/api"

# Functions for API interactions
def refine_query(query):
    """Use the backend API to refine a protein query using Gemini."""
    try:
        response = requests.post(f"{API_BASE_URL}/refine-query", json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error refining query: {e}")
        return {"protein_name": query, "alternative_names": [], "description": "Could not refine query"}

def get_protein_info(protein_name):
    """Get basic protein information from the backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}/protein/{protein_name}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting protein info: {e}")
        return {"error": str(e)}

def get_protein_structure(protein_name):
    """Get protein 3D structure data from the backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}/protein/{protein_name}/structure")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting protein structure: {e}")
        return {"error": str(e)}

def get_protein_analysis(protein_name):
    """Get AI-generated protein analysis from the backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}/protein/{protein_name}/analysis")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting protein analysis: {e}")
        return {"error": str(e)}

def get_drug_associations(protein_name):
    """Get drug associations from the backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}/protein/{protein_name}/drugs")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting drug associations: {e}")
        return {"error": str(e)}

def send_chat_message(messages):
    """Send a chat message to the backend conversation API."""
    try:
        response = requests.post(f"{API_BASE_URL}/conversation", json={"messages": messages})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error in chat: {e}")
        return {"response": f"Error: {str(e)}"}

def display_protein_structure(pdb_data):
    """Display protein structure using py3Dmol with direct HTML rendering."""
    if not pdb_data:
        return
    
    view = py3Dmol.view(width=700, height=500)
    view.addModel(pdb_data, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    view.spin(True)
    # Render in Streamlit using components
    st.components.v1.html(view._make_html(), height=500, scrolling=False)

# Initialize session state for chat
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
    
if "current_protein" not in st.session_state:
    st.session_state.current_protein = None

# App UI with tabs for Search and Chat
tab1, tab2 = st.tabs(["Protein Explorer", "Protein Chat"])

# Tab 1: Protein Explorer
with tab1:
    st.title("🧬 AminoVerse: Protein Explorer")
    st.markdown("### Enter a protein name to explore its structure and information")

    # User input
    protein_query = st.text_input("Protein Name (e.g., Insulin, p53, EGFR)", "")

    if st.button("Search") and protein_query:
        with st.spinner(f"Searching for {protein_query}..."):
            # Step 1: Use backend to refine the search
            refined_data = refine_query(protein_query)
            refined_query = refined_data.get("protein_name", protein_query)
            
            st.session_state.current_protein = refined_query
            
            st.markdown(f"### AI suggests searching for: *{refined_query}*")
            
            with st.expander("AI Analysis"):
                st.markdown(f"**Description**: {refined_data.get('description', 'No description available.')}")
                if refined_data.get('alternative_names'):
                    st.markdown(f"**Alternative names**: {', '.join(refined_data.get('alternative_names'))}")
            
            # Step 2: Get protein info
            protein_info = get_protein_info(refined_query)
            
            if "error" not in protein_info or not protein_info["error"]:
                st.subheader("Protein Information")
                
                function_data = protein_info.get("function", {})
                
                protein_details = {
                    "UniProt ID": function_data.get("id", "Unknown"),
                    "Protein Name": function_data.get("name", "Unknown"),
                    "Gene Names": ", ".join(function_data.get("gene_names", [])),
                    "Organism": function_data.get("organism", "Unknown"),
                    "Function": function_data.get("function", "Function information not available")
                }
                
                # Display protein info in a nice format
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**UniProt ID**: {protein_details['UniProt ID']}")
                    st.markdown(f"**Protein Name**: {protein_details['Protein Name']}")
                    st.markdown(f"**Gene Names**: {protein_details['Gene Names']}")
                
                with col2:
                    st.markdown(f"**Organism**: {protein_details['Organism']}")
                
                st.markdown("**Function Description**:")
                st.markdown(protein_details['Function'])
                
                # Step 3: Get and display protein structure
                st.subheader("Protein 3D Structure")
                
                with st.spinner("Loading 3D protein structure..."):
                    structure_data = get_protein_structure(refined_query)
                    
                    if "error" not in structure_data:
                        # Check if we have PDB data
                        pdb_data = structure_data.get("pdb_data", {}).get("pdb_data")
                        
                        if pdb_data:
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                display_protein_structure(pdb_data)
                            
                            with col2:
                                st.markdown("### Structure Metadata")
                                st.markdown(f"**UniProt ID:** {structure_data.get('uniprot_id', 'Unknown')}")
                                
                                # Get metadata from the first item if it's a list
                                metadata = structure_data.get("structure_metadata", [])
                                if isinstance(metadata, list) and len(metadata) > 0:
                                    metadata = metadata[0]
                                    
                                    if "confidenceAvgDistance" in metadata:
                                        confidence = float(metadata["confidenceAvgDistance"])
                                        st.markdown(f"**Model Confidence:** {confidence:.2f}")
                                        
                                        # Color coding for confidence
                                        if confidence > 0.9:
                                            st.markdown("🟢 **High confidence**")
                                        elif confidence > 0.7:
                                            st.markdown("🟡 **Medium confidence**")
                                        else:
                                            st.markdown("🔴 **Low confidence**")
                        else:
                            st.error("Could not retrieve 3D structure data")
                    else:
                        st.error(f"Error loading structure: {structure_data.get('error', 'Unknown error')}")
                
                # Step 4: Get and display protein analysis
                st.subheader("Protein Analysis")
                
                with st.spinner("Loading AI-generated protein analysis..."):
                    analysis_data = get_protein_analysis(refined_query)
                    
                    if "error" not in analysis_data:
                        st.markdown(analysis_data.get("analysis", "No analysis available"))
                    else:
                        st.error(f"Error loading analysis: {analysis_data.get('error', 'Unknown error')}")
                
                # Step 5: Get and display drug associations
                st.subheader("Drug Associations")
                
                with st.spinner("Loading drug information..."):
                    drug_data = get_drug_associations(refined_query)
                    
                    if "error" not in drug_data:
                        drug_associations = drug_data.get("drug_associations", {})
                        
                        if "drugs" in drug_associations and drug_associations["drugs"]:
                            drugs = drug_associations["drugs"]
                            
                            # Create a dataframe for display
                            drug_df = pd.DataFrame(drugs)
                            st.dataframe(drug_df)
                        else:
                            st.info("No drug associations found for this protein")
                    else:
                        st.error(f"Error loading drug information: {drug_data.get('error', 'Unknown error')}")
            
            else:
                st.error(f"Error: {protein_info.get('error', 'No protein information found')}")

# Tab 2: Protein Chat
with tab2:
    st.title("💬 AminoVerse: Protein Chat")
    
    # Display current protein context if any
    if st.session_state.current_protein:
        st.info(f"Currently exploring: **{st.session_state.current_protein}**. Ask me anything about this protein!")
    else:
        st.info("Search for a protein first in the 'Protein Explorer' tab, or ask general protein biology questions here!")
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about proteins..."):
        # Display user message
        st.chat_message("user").write(prompt)
        
        # Add to chat history
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Prepare messages for API - just the content
        messages_content = [msg["content"] for msg in st.session_state.chat_messages]
        
        # Get response from backend
        with st.spinner("Thinking..."):
            response = send_chat_message(messages_content)
            
            if "response" in response:
                # Display assistant response
                st.chat_message("assistant").write(response["response"])
                
                # Add to chat history
                st.session_state.chat_messages.append({"role": "assistant", "content": response["response"]})
            else:
                st.error("Error: Could not get a response from the chatbot")

# Footer
st.markdown("---")
st.markdown("### About AminoVerse")
st.markdown("""
This application integrates multiple protein databases and AI tools to provide a comprehensive view of protein structures and functions:

- **Data sources**: UniProt, AlphaFold DB, ChEMBL
- **Visualization**: py3Dmol
- **AI assistance**: Google Gemini

Created for Mahendra University Hackathon
""")