import json
j=json.load(open('doctor.json',encoding="utf-8"))
for k in j["keys"]:
    k1=k
    k=j["keys"][k]
    for d in k["decomps"]:
        if d["parts"][0].startswith("*"):
            print(k1)