import requests
import json

def search_uniprot(query):
    """Search UniProt API for proteins matching the query."""
    # Try a simpler query first with minimal parameters
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"{query} AND organism_id:9606",  # Just search for the protein in humans
        "format": "json",
        "size": 5
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"UniProt API error: {str(e)}")
        
        # Try an alternative approach - direct accession lookup
        if len(query) >= 5 and query[0:2].isalpha():  # Looks like a UniProt accession
            try:
                entry_url = f"https://rest.uniprot.org/uniprotkb/{query}"
                entry_response = requests.get(entry_url)
                if entry_response.status_code == 200:
                    return {"results": [entry_response.json()]}
            except:
                pass
        
        # Try with gene name exact match as a fallback
        try:
            fallback_params = {
                "query": f"gene:{query}",  # Search by gene name
                "format": "json",
                "size": 5
            }
            fallback_response = requests.get(url, fallback_params)
            fallback_response.raise_for_status()
            return fallback_response.json()
        except:
            # Return error if all attempts fail
            return {"error": f"Error querying UniProt API: {str(e)}", "results": []}

def get_protein_function(protein_name):
    """
    Query UniProt API to get protein function information
    """
    try:
        # Use the search function
        uniprot_data = search_uniprot(protein_name)
        
        if uniprot_data.get("error"):
            return {"error": uniprot_data["error"]}
            
        # Process the first result if available
        if uniprot_data.get('results') and len(uniprot_data['results']) > 0:
            protein_data = uniprot_data['results'][0]
            
            # Extract gene names safely
            gene_names = []
            if protein_data.get('genes'):
                genes = protein_data['genes']
                if isinstance(genes, list) and len(genes) > 0:
                    for gene in genes:
                        if isinstance(gene, dict) and gene.get('geneName'):
                            gene_name_list = gene.get('geneName', [])
                            for g in gene_name_list:
                                if isinstance(g, dict) and g.get('value'):
                                    gene_names.append(g['value'])
                                elif isinstance(g, str):
                                    gene_names.append(g)
            
            # Extract function information safely
            function = "Function information not available"
            if protein_data.get('comments'):
                for comment in protein_data.get('comments', []):
                    if isinstance(comment, dict) and comment.get('commentType') == 'FUNCTION':
                        if comment.get('texts') and len(comment['texts']) > 0:
                            if isinstance(comment['texts'][0], dict):
                                function = comment['texts'][0].get('value', function)
            
            # Build function info dictionary with safe extractions
            function_info = {
                'id': protein_data.get('primaryAccession', ''),
                'name': (protein_data.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', '')
                        or protein_data.get('proteinDescription', {}).get('submissionNames', [{}])[0].get('fullName', {}).get('value', '')
                        or protein_data.get('id', '')),
                'function': function,
                'gene_names': gene_names,
                'organism': protein_data.get('organism', {}).get('scientificName', '')
            }
            
            return function_info
        else:
            return {'error': 'No protein information found'}
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_protein_function: {str(e)}\n{error_details}")
        # Catch any other unexpected errors
        return {'error': f"Unexpected error processing UniProt data: {str(e)}"}