
def command_test(file="doctor.txt",test_list):
    file_text=open(file,'r').read().split("\n")
    load_text={}
    for l in file_text:
        l=l.strip()
        if l:
            l.split(":")
            load_text[l[0]]=l[1:]
