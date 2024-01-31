
def command_test(file="doctor.txt",test_list):
    file_text=open(file,'r').read().split("\n")
    load_text={}
    for l in fileText:
        l=l.strip()
        if l:
            l.split(":")
            loadText[l[0]]=l[1:]
