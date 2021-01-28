import json

def openJson(json_path):
    json_data = json.load(open(json_path,'r'))
    data = {}
    for image in json_data['images']:
        data[image['id']] = {'image_info': image, 'parkingSpaces_info': []}
    for ps in json_data['parkingSpaces']:
        data[ps['image_id']]['parkingSpaces_info'].append(ps)
    return json_data, data

def get_image_ids_from_date(json_data, date):
    image_ids = []
    for image in json_data['images']:
        if image['date'] == date:
            image_ids.append(image['id'])
    return image_ids

def copy_statuses(data, json_data, base_image, target_image):
    status_for_centers = {}
    for ps in data[base_image]['parkingSpaces_info']:
        status_for_centers[str(ps['rotatedRect'][0])+'_'+str(ps['rotatedRect'][1])] = ps['status_id']
    for ps in data[target_image]['parkingSpaces_info']:
        ps['status_id'] = status_for_centers[str(ps['rotatedRect'][0])+'_'+str(ps['rotatedRect'][1])]
        json_data['parkingSpaces'][ps['id']-1]['status_id'] = ps['status_id']
    return data, json_data

def saveJson(json_data, json_path):
    json.dump(json_data, open(json_path,'w'))
