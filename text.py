import os
from pprint import pprint

for file in os.listdir('deprecated'):
    template=[
'{% extends "base.html" %}\n',
 '{% block title %}title{% endblock %}\n',
 '{% block content %}\n',
]
    with open(f"deprecated/{file}", 'r') as of, open(f'blocktemplates/{file}', 'w') as nf:
        lines = of.readlines()
        try: 
            con = (lines[lines.index('<body>\n')+1 : lines.index('</body>\n')])
            template.extend(con)
            template.append( '\n{% endblock %}')
            nf.writelines(template)
        except Exception as e:
            print(file)
            print(e)
