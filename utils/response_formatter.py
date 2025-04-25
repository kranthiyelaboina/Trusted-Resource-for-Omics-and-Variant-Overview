def format_protein_response(protein_name, function_data=None, structure_data=None, drug_data=None, interaction_data=None):
    """
    Format the combined protein data response
    """
    response = {
        "protein": protein_name,
    }
    
    # Add function data if available
    if function_data:
        function_error = function_data.get('error')
        response["function"] = function_data if not function_error else {"status": "error", "message": function_error}
    
    # Add structure data if available  
    if structure_data:
        structure_error = structure_data.get('error')
        response["structure"] = structure_data if not structure_error else {"status": "error", "message": structure_error}
    
    # Add drug data if available
    if drug_data:
        drug_error = drug_data.get('error')
        response["drug_associations"] = drug_data if not drug_error else {"status": "error", "message": drug_error}
    
    # Add interaction data if available
    if interaction_data:
        interaction_error = interaction_data.get('error')
        response["interactions"] = interaction_data if not interaction_error else {"status": "error", "message": interaction_error}
    
    return response