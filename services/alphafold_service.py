import requests

def get_alphafold_structure(uniprot_id):
    """Get AlphaFold protein structure by UniProt ID."""
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return {"error": "Protein structure not found in AlphaFold database"}
        response.raise_for_status()
        data = response.json()
        return data  # This could be a list, as shown by the error
    except requests.exceptions.RequestException as e:
        return {"error": f"Error querying AlphaFold API: {str(e)}"}

def get_alphafold_pdb(alphafold_data):
    """Download PDB structure from AlphaFold using the PDB URL from the data."""
    if not alphafold_data:
        return {"error": "No AlphaFold data provided"}
        
    try:
        # Handle case where alphafold_data is a list
        if isinstance(alphafold_data, list) and len(alphafold_data) > 0:
            pdb_url = alphafold_data[0].get("pdbUrl")
            if not pdb_url:
                return {"error": "No PDB URL available in AlphaFold data"}
                
            response = requests.get(pdb_url)
            response.raise_for_status()
            return {"pdb_data": response.text}
        else:
            return {"error": "Invalid AlphaFold data structure"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching AlphaFold PDB: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error processing AlphaFold data: {str(e)}"}