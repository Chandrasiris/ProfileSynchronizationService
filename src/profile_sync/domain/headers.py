import re
import unicodedata

def normalize_header(value: str) -> str:
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKC', value).casefold())

EMAIL = frozenset(map(normalize_header, ['Email','Email Address','Email ID','Contact Email','E-mail']))
PHONE = frozenset(map(normalize_header, ['Phone','Tel','Telephone','Tel No','Phone No','Telephone Number','Phone Number','Mobile','Mobile Number','Cell Phone','Cell Number']))
STANDARD = {normalize_header(x): x for x in ['FirstName','LastName','DOBYear','Gender','Ethnicity','State','City','Zipcode','Country','Industry','JobCategory','Profession','Specialty','Skills','Education','Income','MinIncome','MaxIncome','EmploymentType','Company','CompanySize']}
STANDARD['postalcode'] = 'Zipcode'
STANDARD['yearofbirth'] = 'DOBYear'
ALLOWED = frozenset(STANDARD.values())

def identify_contacts(headers: list[str]) -> dict[str, list[int]]:
    return {'Email': [i for i,h in enumerate(headers) if normalize_header(h) in EMAIL], 'Phone': [i for i,h in enumerate(headers) if normalize_header(h) in PHONE]}
