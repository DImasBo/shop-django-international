import requests
import json

d = {
        "CityName": "київ",
        "Limit": 5
}
data = {
"apiKey": "4055c769b3a5c7de4b96d73e3d9d9cb1",
"modelName": "Address",
"calledMethod": "searchSettlements",
"methodProperties": d,
}
url = 'https://api.novaposhta.ua/v2.0/json/'
r = requests.post(url, data=json.dumps(data))

print(r)
j = r.json()
print(j)
print('--------------------')

data = {
"modelName": "Address",
"calledMethod": "getAreas",
"methodProperties": {},
"apiKey": "4055c769b3a5c7de4b96d73e3d9d9cb1"
}
url = 'https://api.novaposhta.ua/v2.0/json/'
r = requests.post(url, data=json.dumps(data))

print(r)
j = r.json()

with open('t.json','w') as f:
	json.dump(j, f)

for l in j['data']:
	print(l['Description']+' ',l['Ref'])

print('--------------------')

data = {
    "modelName": "AddressGeneral",
    "calledMethod": "getSettlements",
    "methodProperties": {
        "AreaRef": "dcaadb64-4b33-11e4-ab6d-005056801329",
        "Ref": "0e451e40-4b3a-11e4-ab6d-005056801329",
        "RegionRef": "e4ade6ea-4b33-11e4-ab6d-005056801329",
    },
	"apiKey": "4055c769b3a5c7de4b96d73e3d9d9cb1"
}


url = 'https://api.novaposhta.ua/v2.0/json/'
r = requests.post(url, data=json.dumps(data))

print(r)
j = r.json()

with open('t_area.json','w') as f:
	json.dump(j, f)

for l in j['data']:
	print(l['Description']+' ',l['Ref'])


