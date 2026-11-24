from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, UniqueConstraint, CheckConstraint, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from uuid import uuid4

class Base(DeclarativeBase): pass

class MappingRecord(Base):
    __tablename__='ProfileFieldsMappingDataset'
    __table_args__=(UniqueConstraint('NormalizedHeader','ContextKey'), CheckConstraint("""jsonb_typeof("TargetFields") = 'array' AND jsonb_array_length("TargetFields") > 0"""))
    Id: Mapped[object]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    SourceHeader: Mapped[str]=mapped_column(String(1000))
    NormalizedHeader: Mapped[str]=mapped_column(String(1000))
    ContextKey: Mapped[str]=mapped_column(String(250),default='')
    TargetFields: Mapped[list]=mapped_column(JSONB)
    TransformationKey: Mapped[str]=mapped_column(String(50))
    ApprovedBy: Mapped[object]=mapped_column(UUID(as_uuid=True))
    CreatedAtUtc: Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now())

class ImportJob(Base):
    __tablename__='ProfileImportJobs'
    Id: Mapped[object]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    OwnerId: Mapped[object]=mapped_column(UUID(as_uuid=True),index=True)
    ProjectName: Mapped[str]=mapped_column(String(250))
    OriginalFileName: Mapped[str]=mapped_column(String(500))
    StorageBlobName: Mapped[str]=mapped_column(String(500))
    FileHash: Mapped[str]=mapped_column(String(64),index=True)
    Status: Mapped[str]=mapped_column(String(50),index=True)
    RowCount: Mapped[int]=mapped_column(Integer,default=0)
    CreatedAtUtc: Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now())
