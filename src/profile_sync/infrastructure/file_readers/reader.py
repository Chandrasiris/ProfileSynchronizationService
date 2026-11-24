import csv
import io
import zipfile
from dataclasses import dataclass
from pathlib import PurePosixPath
from openpyxl import load_workbook
from profile_sync.domain.headers import normalize_header

@dataclass
class Sheet:
    headers: list[str]
    rows: list[tuple[str,...]]

def read_sheet(data: bytes, filename: str, max_bytes: int=10*1024*1024, max_rows: int=10000, max_columns: int=200) -> Sheet:
    if not data or len(data)>max_bytes: raise ValueError('Invalid file size')
    ext = PurePosixPath(filename).suffix.lower()
    book = None
    if ext == '.csv':
        rows = csv.reader(io.StringIO(data.decode('utf-8-sig')), strict=True)
    elif ext == '.xlsx':
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries=archive.infolist()
            if len(entries)>2000 or sum(x.file_size for x in entries)>max_bytes*10: raise ValueError('Unsafe workbook size')
            if any('vbaproject' in x.filename.lower() for x in entries): raise ValueError('Macros prohibited')
        book=load_workbook(io.BytesIO(data), read_only=True, data_only=False, keep_links=False)
        if len(book.worksheets)!=1:
            book.close(); raise ValueError('Select a single worksheet before importing')
        ws=book.worksheets[0]
        if (ws.max_column or 0)>max_columns or (ws.max_row or 0)>max_rows+1:
            book.close(); raise ValueError('Workbook dimensions exceed limits')
        def values():
            for row in ws.iter_rows():
                if any(c.data_type=='f' for c in row): raise ValueError('Formulas prohibited')
                yield [c.value for c in row]
        rows=values()
    else: raise ValueError('Unsupported file type')
    try:
        headers=[str(x or '').strip() for x in next(rows, [])]
        normalized=[normalize_header(h) for h in headers]
        if not headers or len(headers)>max_columns or not all(normalized) or len(set(normalized))!=len(headers): raise ValueError('Invalid or duplicate headers')
        result=[]
        for i,row in enumerate(rows):
            if i>=max_rows or len(row)!=len(headers): raise ValueError('Row limit or inconsistent width')
            values=tuple('' if x is None else str(x).strip() for x in row)
            if any(len(x)>10000 for x in values): raise ValueError('Cell too long')
            if any(values): result.append(values)
        return Sheet(headers,result)
    finally:
        if book: book.close()
