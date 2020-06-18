# Utility functions to generate SQL statements for REDCap

# expects sql-options to be in this format: {"project_id": 13, "filter" : {'pain_past3backpain': "= 1", 'yrbirth': "< 1931"}}
def gen_count(options):

    # Returns the SQL query
    def generate():
        query = 'SELECT COUNT(DISTINCT record) FROM redcap_data WHERE project_id='+str(options["project_id"])
        query_end = ''
        filter_logic = options["filter"]
        for field in filter_logic:
            query += ' AND record IN (SELECT DISTINCT record FROM redcap_data WHERE project_id='+str(options["project_id"])+' AND field_name="'+str(field)+'" AND value '+str(filter_logic[field]) 
            query_end += ')'
        return query + query_end
    
    # Validates options and returns {"valid": True} or {"valid": False, "error": "..."}
    def validate():
        if ("project_id" not in options):
            return {"valid": False, "error": "project_id is missing in sql-options"}
        elif ("filter" not in options):
            return {"valid": False, "error": "filter is missing in sql-options"}
        elif (type(options["project_id"]) != "number"):
            return {"valid": False, "error": "project_id is not a number"}
        else:
            return {"valid": True}

    # return this function in the form {"generate": generate, "validate": validate}
    ret = {
        "generate": generate,
        "validate": validate
    }
    return ret       

# expects sql-options to be in this format: {"project_id": 13, "filter" : {'pain_past3backpain': "= 1", 'yrbirth': "< 1931"}, "field": "yrbirth"}
def gen_max(options):

    def generate():
        query = 'SELECT MAX(value) FROM redcap_data WHERE project_id='+str(options["project_id"])+' AND field_name="'+str(options["field"])+'"'
        query_end = ''
        filter_logic = options["filter"]
        for field in filter_logic:
            query += ' AND record IN (SELECT DISTINCT record FROM redcap_data WHERE project_id='+str(options["project_id"])+' AND field_name="'+str(field)+'" AND value '+str(filter_logic[field]) 
            query_end += ')'
        return query + query_end
    
    def validate():
        if ("project_id" not in options):
            return {"valid": False, "error": "'project_id' is missing in sql-options"}
        elif ("filter" not in options):
            return {"valid": False, "error": "'filter' is missing in sql-options"}
        elif ("field" not in options):
            return {"valid": False, "error": "'field' to pick max from is missing in sql-options"}
        elif (type(options["project_id"]) != "number"):
            return {"valid": False, "error": "project_id is not a number"}
        else:
            return {"valid": True}

    ret = {
        "generate": generate,
        "validate": validate
    }
    return ret 

# A map to SQL functions
generator_map = {
    "count": gen_count,
    "max": gen_max    
}