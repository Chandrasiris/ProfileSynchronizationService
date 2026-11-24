from profile_sync.domain.headers import ALLOWED, STANDARD, normalize_header, identify_contacts
from profile_sync.domain.models import Mapping
from profile_sync.application.ports.contracts import MappingRepository, FieldMappingAgent, MetadataSanitizer

TRANSFORMS = {'identity','birth_year','income_range','postal_code'}

def validate_mapping(m: Mapping) -> None:
    if not m.targets or not set(m.targets) <= ALLOWED or m.transformation not in TRANSFORMS:
        raise ValueError('Invalid mapping')
    if m.transformation == 'income_range':
        if set(m.targets) != {'MinIncome','MaxIncome'}: raise ValueError('Invalid income mapping')
    elif len(m.targets) != 1: raise ValueError('Expected single target')
    if m.transformation == 'birth_year' and m.targets != ('DOBYear',): raise ValueError('Invalid birth year target')
    if m.transformation == 'postal_code' and m.targets != ('Zipcode',): raise ValueError('Invalid postal target')

def resolve(headers: list[str], context: str, repo: MappingRepository, agent: FieldMappingAgent, sanitizer: MetadataSanitizer) -> tuple[list[Mapping], list[str]]:
    contacts = identify_contacts(headers)
    skip = set(contacts['Email'] + contacts['Phone'])
    result, pending = [], []
    for i,h in enumerate(headers):
        if i in skip: continue
        field = STANDARD.get(normalize_header(h))
        if field: result.append(Mapping(h,(field,),source='system'))
        else: pending.append(h)
    known = repo.find(pending,context) if pending else {}
    unknown = []
    for h in pending:
        m = known.get(normalize_header(h))
        if m:
            validate_mapping(m)
            result.append(Mapping(h,m.targets,m.transformation,'dataset'))
        else: unknown.append(h)
    if unknown:
        sanitizer.approve(context,unknown)
        seen = set()
        for m in agent.suggest(unknown, context, sorted(ALLOWED)):
            validate_mapping(m)
            if m.source_header not in unknown or m.source_header in seen: raise ValueError('Unexpected agent header')
            seen.add(m.source_header)
            result.append(Mapping(m.source_header,m.targets,m.transformation,'ai'))
        unknown = [h for h in unknown if h not in seen]
    return result, unknown

def approved_dataset_entries(mappings: list[Mapping]) -> list[Mapping]:
    result = []
    for m in mappings:
        if not m.targets or m.source in {'system','dataset'}: continue
        validate_mapping(m)
        if identify_contacts([m.source_header]) != {'Email': [], 'Phone': []}: raise ValueError('Contact mapping is system-owned')
        result.append(m)
    return result
