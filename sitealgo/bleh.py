import redcap 
from csv import reader
import requests

with open('/home/stolet/ham10000/HAM10000_metadata.csv') as read_obj:
    csv_reader = reader(read_obj)

    api_url = "http://localhost/redcap/api/"
    api_token = "936AF3AE86AEB1FDD2CA231EDE7D2D2D"
    project = redcap.Project(api_url, api_token, verify_ssl=False, lazy=False)
    data = project.export_records(records=[])
    print(len(data))
    i = 0
    for row in csv_reader:
        image_id = row[1]
        if image_id == "image_id":
            i += 1
            continue

        fname = "/home/stolet/ham10000/HAM10000_images_part_1/" + image_id + ".jpg"
        data = {
            'token': '936AF3AE86AEB1FDD2CA231EDE7D2D2D',
            'content': 'file',
            'action': 'import',
            'record': str(i),
            'field': 'image',
            'event': '',
            'returnFormat': 'json'
        }
        file_obj = open(fname, 'rb')
        r = requests.post('http://13.64.199.249/redcap/api/',data=data,files={'file':file_obj})
        file_obj.close()
        print('HTTP Status: ' + str(r.status_code))
        
        #fname = "/home/stolet/ham10000/HAM10000_images_part_1/" + image_id + ".jpg"
        #data = {
        #    'token': '936AF3AE86AEB1FDD2CA231EDE7D2D2D',
        #    'content': 'file',
        #    'action': 'import',
        #    'record': str(i),
        #    'field': 'image',
        #    'event': '',
        #    'returnFormat': 'json'
        #}
        #file_obj = open(fname, 'rb')
        #r = requests.post('http://localhost/redcap/api/',data=data,files={'file':file_obj})
        #file_obj.close()
        #print('HTTP Status: ' + str(r.status_code))
        #print(r)
        i += 1
