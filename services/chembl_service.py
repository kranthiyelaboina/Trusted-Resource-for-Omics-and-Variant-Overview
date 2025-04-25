import requests

def search_chembl(protein_name):
    """Search ChEMBL for targets related to the protein."""
    base_url = "https://www.ebi.ac.uk/chembl/api/data"
    
    # Search for targets by protein name
    url = f"{base_url}/target/search"
    params = {
        "q": protein_name,
        "format": "json",
        "limit": 5
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error querying ChEMBL API: {str(e)}"}

def get_drug_associations(protein_name):
    """Query ChEMBL API for drug associations."""
    try:
        # Using ChEMBL API for drug target information
        # First get the ChEMBL target ID for the protein
        chembl_data = search_chembl(protein_name)
        
        if chembl_data.get("error"):
            return {"error": chembl_data["error"]}
            
        if not chembl_data.get("targets") or len(chembl_data["targets"]) == 0:
            return {"error": "No target information found in ChEMBL"}
        
        target_chembl_id = chembl_data["targets"][0].get("target_chembl_id")
        
        if not target_chembl_id:
            return {"error": "Could not find ChEMBL target ID"}
        
        # Get drugs/compounds that interact with this target
        drugs_url = f"https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id={target_chembl_id}&limit=30&format=json"
        drugs_response = requests.get(drugs_url)
        drugs_response.raise_for_status()
        drugs_data = drugs_response.json()
        
        drug_list = []
        for activity in drugs_data.get("activities", []):
            # Only include entries that have the essential data
            if not activity.get("molecule_chembl_id"):
                continue
                
            drug = {
                "molecule_chembl_id": activity.get("molecule_chembl_id"),
            }
            
            # Only add fields if they have actual data
            if activity.get("molecule_name"):
                drug["molecule_name"] = activity["molecule_name"]
                
            if activity.get("standard_type"):
                drug["activity_type"] = activity["standard_type"]
                
            if activity.get("standard_value") is not None:
                value_str = f"{activity['standard_value']}"
                if activity.get("standard_units"):
                    value_str += f" {activity['standard_units']}"
                drug["activity_value"] = value_str
                
            # Include additional informative fields when available
            if activity.get("target_organism"):
                drug["target_organism"] = activity["target_organism"]
                
            if activity.get("assay_description"):
                drug["assay_description"] = activity["assay_description"]
                
            # Only append if we have more than just the ID
            if len(drug) > 1:
                drug_list.append(drug)
        
        return {
            "target_chembl_id": target_chembl_id,
            "target_name": chembl_data["targets"][0].get("pref_name", ""),
            "drugs": drug_list
        }
    except Exception as e:
        return {"error": f"Error fetching drug association data: {str(e)}"}