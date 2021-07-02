import requests
from bs4 import BeautifulSoup
import re
import json

def dict_clean(items):
    result = {}
    for key, value in items:
        if value is None:
            value = '0'
        result[key] = value
    return result

def get_nlist(element: str):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177'}
    url = 'https://www.misprofesores.com/escuelas/{}'.format(element)
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text,'html.parser')
    pattern = re.compile("var dataSet = .")
    script = soup.find_all('script', text=pattern)
    m = re.search("var dataSet = (.+)", str(script))
    if m:
        found = m.group()
    extract = re.search("\[.+\]", found)[0]
    splited = json.loads(extract, object_pairs_hook=dict_clean)
    return splited

urls = ['ESFM-IPN_1691', 'IPN-ESFM_3415']
aux =[]
for element in urls:
    aux+=get_nlist(element)

def normal(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

complete = [{k: normal(v).upper() for k, v in element.items()} for element in aux]

for element in complete:
    try:
        del element['d']
    except KeyError:
        pass
#complete
