import json
key=json.load(open("doctor.json",encoding="utf-8"))["keys"]
for i in key:
    print(i)
    i=key[i]
    for d in i["decomps"]:
        for r in d["reasmbs"]:
            print(" ".join(r))
    print("---")