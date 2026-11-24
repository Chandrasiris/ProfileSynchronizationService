from uuid import UUID
from .models import Match, MatchStatus

def classify(email: str | None, phone: str | None, emails: set[UUID], phones: set[UUID]) -> Match:
    if not email and not phone: return Match(MatchStatus.INVALID)
    if len(emails)>1 or len(phones)>1: return Match(MatchStatus.CONFLICT)
    if email and phone and (emails or phones) and emails != phones: return Match(MatchStatus.CONFLICT)
    candidates = emails | phones
    if not candidates: return Match(MatchStatus.NEW)
    # Phone-only matches require review, since household numbers may be shared.
    if not emails: return Match(MatchStatus.CONFLICT)
    return Match(MatchStatus.EXISTING, next(iter(candidates)))
