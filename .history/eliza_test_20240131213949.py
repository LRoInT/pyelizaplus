import eliza
def command_test(file="doctor.txt",test_list=["pre","post","synon","key"]):
    el=eliza.Eliza()
    el.load(file)
    file_text=open(file,'r').read().split("\n")
    load_text={}
    ret=[]
    for l in file_text:
        l=l.strip()
        if l:
            l=l.split(":")
            if l[0] in load_text:
                load_text[l[0]].append(l[1:])
            else:
                load_text[l[0]]=[l[1]]
    print(load_text)
    for t in test_list:
        for i in load_text[t]:
            print(i)
            ret.append(el.respond(i))
    return ret

if __name__=="__main__":
    print(command_test())

