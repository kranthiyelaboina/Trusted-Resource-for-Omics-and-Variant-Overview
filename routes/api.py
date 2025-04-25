from flask import Blueprint, request, jsonify
from services.uniprot_service import get_protein_function, search_uniprot
from services.alphafold_service import get_alphafold_structure, get_alphafold_pdb
from services.chembl_service import search_chembl, get_drug_associations
# from services.protein_interactions_service import get_protein_interactions
from services.gemini_service import refine_protein_query, generate_protein_analysis
from utils.response_formatter import format_protein_response

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def api_index():
    """API root endpoint."""
    return jsonify({
        "status": "online",
        "message": "AminoVerse API v1.0",
        "endpoints": {
            "GET /api/protein/{protein_name}": "Get basic protein information",
            "GET /api/protein/{protein_name}/analysis": "Get AI-generated protein analysis",
            "GET /api/protein/{protein_name}/structure": "Get protein 3D structure data",
            "GET /api/protein/{protein_name}/drugs": "Get drug associations",
            "POST /api/refine-query": "Refine a protein query using AI"
        }
    })

@api_bp.route('/protein/<protein_name>', methods=['GET'])
def get_protein_info(protein_name):
    """
    Get comprehensive information about a protein or gene
    """
    try:
        # Get biological function from UniProt
        function_data = get_protein_function(protein_name)
        
        # Format the response - only basic info at this endpoint
        response = {
            "protein": protein_name,
            "function": function_data
        }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500

@api_bp.route('/protein/<protein_name>/structure', methods=['GET'])
def get_protein_structure_data(protein_name):
    """
    Get structure information for a protein
    """
    try:
        # First get UniProt ID
        uniprot_data = search_uniprot(protein_name)
        
        if uniprot_data.get("error") or not uniprot_data.get("results"):
            return jsonify({"error": "Could not find protein in UniProt"}), 404
            
        uniprot_id = uniprot_data["results"][0].get("primaryAccession")
        
        if not uniprot_id:
            return jsonify({"error": "Could not determine UniProt ID"}), 404
        
        # Get AlphaFold structure
        structure_data = get_alphafold_structure(uniprot_id)
        
        # Fix here: Check if structure_data is a list and handle appropriately
        if structure_data:
            # Check if it's a dictionary with an error
            if isinstance(structure_data, dict) and structure_data.get("error"):
                response = {
                    "protein_name": protein_name,
                    "uniprot_id": uniprot_id,
                    "error": structure_data.get("error")
                }
            # If it's a list (normal AlphaFold response format)
            elif isinstance(structure_data, list):
                pdb_data = get_alphafold_pdb(structure_data)
                response = {
                    "protein_name": protein_name,
                    "uniprot_id": uniprot_id,
                    "structure_metadata": structure_data,
                    "pdb_data": pdb_data
                }
            else:
                response = {
                    "protein_name": protein_name,
                    "uniprot_id": uniprot_id,
                    "error": "Unexpected structure data format"
                }
        else:
            response = {
                "protein_name": protein_name,
                "uniprot_id": uniprot_id,
                "error": "No structure available"
            }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500

@api_bp.route('/protein/<protein_name>/drugs', methods=['GET'])
def get_protein_drug_data(protein_name):
    """
    Get drug association information for a protein
    """
    try:
        # Get drug associations
        drug_data = get_drug_associations(protein_name)
        
        response = {
            "protein_name": protein_name,
            "drug_associations": drug_data
        }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500

@api_bp.route('/protein/<protein_name>/analysis', methods=['GET'])
def get_protein_analysis(protein_name):
    """
    Get AI-generated analysis for a protein
    """
    try:
        # First get UniProt ID
        uniprot_data = search_uniprot(protein_name)
        
        if uniprot_data.get("error") or not uniprot_data.get("results"):
            return jsonify({"error": "Could not find protein in UniProt"}), 404
            
        uniprot_id = uniprot_data["results"][0].get("primaryAccession")
        protein_name = uniprot_data["results"][0].get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", protein_name)
        
        if not uniprot_id:
            return jsonify({"error": "Could not determine UniProt ID"}), 404
        
        # Generate analysis
        analysis = generate_protein_analysis(protein_name, uniprot_id)
        
        response = {
            "protein_name": protein_name,
            "uniprot_id": uniprot_id,
            "analysis": analysis
        }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500

@api_bp.route('/refine-query', methods=['POST'])
def refine_query():
    """
    Use Gemini AI to refine a protein query
    """
    try:
        data = request.json
        
        if not data or not data.get("query"):
            return jsonify({"error": "Missing 'query' field in request"}), 400
            
        query = data["query"]
        
        # Use Gemini to refine the query
        refined = refine_protein_query(query)
        
        return jsonify(refined)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500

@api_bp.route('/conversation', methods=['POST'])
def conversation():
    """
    Handle a conversational query about proteins
    """
    try:
        data = request.json
        
        if not data or not data.get("messages"):
            return jsonify({"error": "Missing 'messages' field in request"}), 400
        
        # Format the conversation for Gemini
        messages = data["messages"]
        current_query = messages[-1] if messages else ""
        conversation_history = "\n".join([f"User: {msg}" if i % 2 == 0 else f"Assistant: {msg}" for i, msg in enumerate(messages[:-1])]) if len(messages) > 1 else ""
        
        # Build the prompt with conversation context
        if conversation_history:
            prompt = f"""
            I am an AI assistant specializing in protein biology. 
            
            Previous conversation:
            {conversation_history}
            
            User's latest question: {current_query}
            
            Provide a helpful, scientifically accurate response about this protein or biology question.
            """
        else:
            prompt = f"""
            I am an AI assistant specializing in protein biology. 
            
            User's question: {current_query}
            
            Provide a helpful, scientifically accurate response about this protein or biology question.
            """
        
        # Get response from Gemini
        from services.gemini_service import query_gemini
        response = query_gemini(prompt)
        
        return jsonify({
            "response": response
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500