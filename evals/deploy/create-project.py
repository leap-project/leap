import requests
import json
import pandas

def create_project(url, super_token):
    record = [{
        'project_title': 'ham10000', 
        'purpose': '0',
        'purpose_other': '',
        'project_notes': ''}]
    
    data = json.dumps(record)

    fields = {
        'token': super_token,
        'content': 'project',
        'format': 'json',
        'data': data,
    }
    r = requests.post(url, data=fields)
    
    print(r.status_code)
    print(r.text)

    return r.text

def add_fields_to_project(url, token):
    dictionary = [{"field_name":"record_id","form_name":"ham","section_header":"","field_type":"text","field_label":"record_id","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"y","branching_logic":"","required_field":"y","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""}, 
                  {"field_name":"image_id","form_name":"ham","section_header":"","field_type":"text","field_label":"image_id","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"","branching_logic":"","required_field":"","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""}, 
                  {"field_name":"lesion_id","form_name":"ham","section_header":"","field_type":"text","field_label":"lesion_id","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"","branching_logic":"","required_field":"","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""}, 
                  {"field_name":"dx","form_name":"ham","section_header":"","field_type":"text","field_label":"dx","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"","branching_logic":"","required_field":"","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""}, 
                  {"field_name":"dx_type","form_name":"ham","section_header":"","field_type":"text","field_label":"dx_type","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"","branching_logic":"","required_field":"","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""}, 
                  {"field_name":"age","form_name":"ham","section_header":"","field_type":"text","field_label":"age","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"","branching_logic":"","required_field":"","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""},
                  {"field_name":"sex","form_name":"ham","section_header":"","field_type":"text","field_label":"sex","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"","branching_logic":"","required_field":"","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""},
                  {"field_name":"localization","form_name":"ham","section_header":"","field_type":"text","field_label":"localization","select_choices_or_calculations":"","field_note":"","text_validation_type_or_show_slider_number":"","text_validation_min":"","text_validation_max":"","identifier":"","branching_logic":"","required_field":"","custom_alignment":"","question_number":"","matrix_group_name":"","matrix_ranking":"","field_annotation":""}] 
   
    data = json.dumps(dictionary)
    metadata = {
        'token': token,
        'content': 'metadata',
        'format': 'json',
        'data': data,
        'returnFormat': 'json',
    }

    r = requests.post(url, data=metadata)
    print('HTTP Status: ' + str(r.status_code))
    print(r.text)

def add_data_to_project(url, token):
    data = pandas.read_csv("~/ham10000/HAM10000_metadata.csv")
    records = []
    for index, row in data.iterrows():
        record = {
            "record_id": str(row['record_id']),
            "image_id": row['image_id'],
            "lesion_id": row['lesion_id'],
            "dx": row['dx'],
            "dx_type": row['dx_type'],
            "age": str(row['age']),
            "sex": row['sex'],
            "localization": row['localization'],
        }
        records.append(record) 
    
    data = json.dumps(records)

    fields = {
        'token': token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'data': data,
    }

    r = requests.post(url, data=fields)
    print('HTTP Status: ' + str(r.status_code))
    print(r.text)

if __name__ == "__main__":
    url = 'http://localhost/redcap/api/'
    super_token = "FEJRQVHQ3993BYQ50KMXZ0XFQH17V3X5P5STELNZ2DE243EUKJDY4T2O12GZ5555"
    token = project_token = create_project(url, super_token)
    add_fields_to_project(url, token) 
    add_data_to_project(url, token)
    with open("token", "w") as f:
        f.write(token)
    
