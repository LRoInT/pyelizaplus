import timeit
import json
import re

s="""load = json.load(open("doctor.json", "r", encoding="utf-8"))
gPats = load["gPats"]
"""
t1="""
keys = list(
map(lambda x: re.compile(x[0], re.IGNORECASE), gPats)
)"""

t2="""
keys = [re.compile(x[0], re.IGNORECASE) for x in gPats ] """
exec(s)
r=[]
def f1():
    t = timeit.Timer(lambda:exec(t2)).timeit(number=1000)
    t3 = timeit.Timer(lambda:exec(t1)).timeit(number=1000)
    r.append("t1"if t3<t else "t2")
for i in range(100):
    f1()
if r.count("t1")>r.count("t2"):
    print("t1")
elif r.count("t1")<r.count("t2"):
    print("t2")
else:
    print("same")