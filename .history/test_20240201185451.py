import re 
text="a,b;c.d"
text = re.sub(r'\s*\{}+\s*'.format("."), ' . ', text)
text = re.sub(r'\s*,+\s*', ' , ', text)
text = re.sub(r'\s*;+\s*', ' ; ', text)
print(text)