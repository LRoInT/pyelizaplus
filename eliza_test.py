import eliza
import json
eliza=eliza.Eliza()
eliza.load("doctor.txt")
f=open("test/output.json","w",encoding="utf-8")
def key_test():
    ret_dict={}
    for k in eliza.keys:
        ret=eliza.respond(k)
        print(k,ret)
        ret_dict[k]=ret
    return ret_dict
if __name__=="__main__":
    f.write(json.dumps(key_test(),ensure_ascii=False,indent=4))
    print(key_test())

