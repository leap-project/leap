# Utility functions to generate SQL statements for REDCap

def gen_select(project_id, select_fields = [],  filter_logic = {}):
    query = 'SELECT * FROM redcap_data WHERE project_id=13 AND record IN (SELECT DISTINCT record FROM redcap_data WHERE (field_name="yrbirth" AND value<1940) OR (field_name="calc_csi" AND value>55) AND project_id=13)'
    return query


def gen_count(selector):
    query = 'SELECT COUNT(DISTINCT record) FROM redcap_data WHERE project_id='+str(selector["project_id"])
    query_end = ''
    filter_logic = selector["filter"]
    for field in filter_logic:
        query += ' AND record IN (SELECT DISTINCT record FROM redcap_data WHERE project_id='+str(selector["project_id"])+' AND field_name="'+str(field)+'" AND value '+str(filter_logic[field]) 
        query_end += ')'
    return query + query_end

#def gen_max(project_id, select_fields = [],  filter_logic = {}):
#    query = 'select * from redcap_data where project_id=13 and record in (select record from redcap_data where project_id=13 and field_name="yrbirth" and value = (select max(value) from redcap_data where project_id=13 and field_name="yrbirth"))'


# A map to SQL functions
generator_map = {
    "count": gen_count,
    "select": gen_select    
}