import json

dic={
    'remote_server_address':'45.77.124.235',
    'remote_server_port':8888
}

fn='config.json'
with open(fn,'w') as f:
    json.dump(dic,f,indent='')

with open(fn,'r') as f:
    r=json.load(f)
    print(r)
