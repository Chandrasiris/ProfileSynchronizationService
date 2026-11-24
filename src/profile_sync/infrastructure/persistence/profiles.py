from sqlalchemy import text
from uuid import UUID

class ProfileLookupRepository:
    def __init__(self, engine): self.engine=engine
    def lookup(self, hashes: list[str], *, phone: bool=False) -> dict[str,set[UUID]]:
        column='PhoneHash' if phone else 'EmailHash'
        query=text(f'''SELECT "Id", "{column}" AS hash FROM "Profiles" WHERE "{column}" = ANY(:hashes) AND "{column}" <> '' ''')
        result={}
        with self.engine.connect() as conn:
            for i in range(0,len(hashes),1000):
                batch=[x for x in hashes[i:i+1000] if x]
                if not batch: continue
                for row in conn.execute(query,{'hashes':batch}).mappings():
                    result.setdefault(row['hash'],set()).add(row['Id'])
        return result
