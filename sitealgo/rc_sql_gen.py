# Utility functions to generate SQL statements for REDCap

# expects sql-options to be in this format: {"project_id": 13, "filter" : {'pain_past3backpain': "= 1", 'yrbirth': "< 1931"}}
def gen_count(options):
    query = 'SELECT COUNT(DISTINCT record) FROM redcap_data WHERE project_id='+str(options["project_id"])
    query_end = ''
    filter_logic = options["filter"]
    for field in filter_logic:
        query += ' AND record IN (SELECT DISTINCT record FROM redcap_data WHERE project_id='+str(options["project_id"])+' AND field_name="'+str(field)+'" AND value '+str(filter_logic[field]) 
        query_end += ')'
    return query + query_end

# expects sql-options to be in this format: {"project_id": 13, "filter" : {'pain_past3backpain': "= 1", 'yrbirth': "< 1931"}, "field": "yrbirth"}
def gen_max(options):
    query = 'SELECT MAX(value) FROM redcap_data WHERE project_id='+str(options["project_id"])+' AND field_name="'+str(options["field"])+'"'
    query_end = ''
    filter_logic = options["filter"]
    for field in filter_logic:
        query += ' AND record IN (SELECT DISTINCT record FROM redcap_data WHERE project_id='+str(options["project_id"])+' AND field_name="'+str(field)+'" AND value '+str(filter_logic[field]) 
        query_end += ')'
    return query + query_end

# A map to SQL functions
generator_map = {
    "count": gen_count,
    "max": gen_max    
}