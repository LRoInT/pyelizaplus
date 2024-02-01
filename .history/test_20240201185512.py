import re 
text="a,b;c.d"
text = re.sub(r'\s*\{}+\s*'.format("."), ' . ', text)
print(text)