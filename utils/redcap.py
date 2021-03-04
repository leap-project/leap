import requests

def export_records(ids, fields, url, token):
    data = {
        'token': token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    
    i = 0
    for id in ids:
        key = "records[" + str(i) + "]"
        data[key] = id
        i += 1

    i = 0
    for field in fields:
        key = "fields[" + str(i) + "]"
        data[key] = field
        i += 1

    r = requests.post(url, data=data)
    return r.json()



def export_file(record_id, field, url, token) :
   data = {'token': token,
           'content': 'file',
           'action': 'export',
           'record': record_id,
           'field': field,
           'event': '',
           'returnFormat': 'json'}
   r = requests.post(url, data=data)

   return r.content, r.headers
