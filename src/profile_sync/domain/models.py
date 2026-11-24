from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

class MatchStatus(StrEnum):
    EXISTING = 'existing'
    NEW = 'new'
    CONFLICT = 'conflict'
    INVALID = 'invalid'
    DUPLICATE = 'duplicate'

class JobStatus(StrEnum):
    UPLOADED = 'uploaded'
    AWAITING_TAG_APPROVAL = 'awaiting_tag_approval'
    AWAITING_MAPPING_APPROVAL = 'awaiting_mapping_approval'
    AWAITING_SYNC_CONFIRMATION = 'awaiting_sync_confirmation'
    COMPLETED = 'completed'
    FAILED = 'failed'

@dataclass(frozen=True)
class Mapping:
    source_header: str
    targets: tuple[str, ...]
    transformation: str = 'identity'
    source: str = 'manual'

@dataclass(frozen=True)
class Match:
    status: MatchStatus
    profile_id: UUID | None = None
