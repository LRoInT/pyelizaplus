import re 
text="a,b;c.d"
text = re.sub(r'\s*\.+\s*', ' . ', text)
text = re.sub(r'\s*,+\s*', ' , ', text)
text = re.sub(r'\s*;+\s*', ' ; ', text)