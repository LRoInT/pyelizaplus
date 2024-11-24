# 规则快速查询
import eliza
import sys
eliza_obj = eliza.Eliza()

# 获取所有规则
eliza_obj.load_text("doctor.txt")
argv=sys.argv[1:]
f=argv[0]
output=[]
argv.append("")
def find(f):
    if argv[1]=="keys":
        for k in eliza_obj.keys:
            if f in eliza_obj.keys[k].__str__():
                output.append(k)
            if argv[2]=="word":
                if f in k.word:
                    output.append(k)
            elif argv[2]=="weight":
                if f in k.weight:
                    output.append(k)
            elif argv[2]=="decomps":
                if f in eliza_obj.keys[k].decomps:
                    output.append(k)
print(output)


