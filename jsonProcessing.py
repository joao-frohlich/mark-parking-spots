import json

def openJson(json_path):
    json_data = json.load(open(json_path,'r'))
    data = {}
    for image in json_data['images']:
        data[image['id']] = {'image_info': image, 'parkingSpaces_info': []}
    for ps in json_data['parkingSpaces']:
        data[ps['image_id']]['parkingSpaces_info'].append(ps)
    return json_data, data


def saveJson(json_data, json_path):
    json.dump(json_data, open(json_path,'w'))
