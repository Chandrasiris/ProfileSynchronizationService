import re
from pathlib import PurePosixPath

def extract_project_name(filename: str) -> str:
    p = PurePosixPath(filename.replace('\\','/'))
    if p.suffix.lower() not in {'.csv','.xlsx'}:
        raise ValueError('Unsupported extension')
    name = re.sub(r'\s+', ' ', p.stem.replace('_',' ')).strip()
    name = re.sub(r'\s+v\d+(?:\.\d+)*$', '', name, flags=re.I)
    name = re.sub(r'(?:^|\s+|\s*-\s*) (?:screening\s+sheet|screening\s+results|screening\s+data|screener|screening)$', '', name, flags=re.I | re.X).strip(' -')
    if not name or len(name)>250 or any(ord(c)<32 for c in name):
        raise ValueError('Invalid project name')
    return name
