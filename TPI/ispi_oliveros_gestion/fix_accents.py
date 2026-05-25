import os

bads = {
    'Ã¡': 'á',
    'Ã©': 'é',
    'Ã\xad': 'í',
    'Ã³': 'ó',
    'Ãº': 'ú',
    'Ã±': 'ñ',
    'Ã\x91': 'Ñ',
    'Ã\x93': 'Ó',
    'Â¿': '¿',
    'Ã\x8d': 'Í',
    'Ã\x81': 'Á',
    'Ã\x89': 'É',
    'Ã\x9a': 'Ú'
}

for root, dirs, files in os.walk('templates'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    c = file.read()
            except UnicodeDecodeError:
                continue
            
            changed = False
            for k, v in bads.items():
                if k in c:
                    c = c.replace(k, v)
                    changed = True
            
            if changed:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(c)
                print(f"Fixed {path}")
