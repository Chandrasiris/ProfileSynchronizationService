from sqlalchemy import select
from sqlalchemy.orm import Session
from profile_sync.domain.headers import normalize_header
from profile_sync.domain.models import Mapping
from profile_sync.application.services.mapping import approved_dataset_entries
from .models import MappingRecord

class SqlMappingRepository:
    def __init__(self,engine): self.engine=engine
    def find(self,headers,context):
        keys=[normalize_header(h) for h in headers]
        with Session(self.engine) as session:
            records=session.scalars(select(MappingRecord).where(MappingRecord.NormalizedHeader.in_(keys),MappingRecord.ContextKey.in_(['',context]))).all()
            return {r.NormalizedHeader:Mapping(r.SourceHeader,tuple(r.TargetFields),r.TransformationKey,'dataset') for r in sorted(records,key=lambda r: bool(r.ContextKey))}
    def save_approved(self,mappings,context,approved_by):
        # Existing mappings must be corrected via an explicit future management workflow.
        with Session(self.engine) as session, session.begin():
            for m in approved_dataset_entries(mappings):
                session.add(MappingRecord(SourceHeader=m.source_header,NormalizedHeader=normalize_header(m.source_header),ContextKey=context,TargetFields=list(m.targets),TransformationKey=m.transformation,ApprovedBy=approved_by))
