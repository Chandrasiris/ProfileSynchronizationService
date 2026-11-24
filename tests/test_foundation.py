from uuid import uuid4
from fastapi.testclient import TestClient
from profile_sync.main import app
from profile_sync.domain.project_name import extract_project_name
from profile_sync.domain.headers import identify_contacts
from profile_sync.domain.matching import classify
from profile_sync.domain.models import MatchStatus, Mapping
from profile_sync.application.services.mapping import resolve, approved_dataset_entries
from profile_sync.infrastructure.file_readers.reader import read_sheet
import pytest

def test_health():
    c=TestClient(app)
    assert c.get('/health/live').status_code==200
    assert c.get('/docs').status_code==404
    assert c.post('/api/v1/profile-imports/inspect').status_code==503

def test_filename(): assert extract_project_name('K12_Teachers_Screening_Sheet_v2.xlsx')=='K12 Teachers'
def test_contacts(): assert identify_contacts(['Email Address','Tel No','Gender'])=={'Email':[0],'Phone':[1]}
def test_csv(): assert read_sheet(b'Email,Gender\na@example.com,X\n','a.csv').rows==[('a@example.com','X')]
def test_duplicate_headers():
    with pytest.raises(ValueError): read_sheet(b'Email,E-mail\na,b','x.csv')
def test_conflict(): assert classify('a','b',{uuid4()},{uuid4()}).status==MatchStatus.CONFLICT

def test_dataset_first():
    class Repo:
        def find(self,headers,context): return {'earnings':Mapping('Earnings',('MinIncome','MaxIncome'),'income_range')}
    class Agent:
        def suggest(self,headers,context,allowed_fields):
            assert headers==['Occupation?']; return [Mapping('Occupation?',('Profession',))]
    class Sanitizer:
        def approve(self,context,headers): assert headers==['Occupation?']
    mapped,unknown=resolve(['Email','Gender','Earnings','Occupation?'],'study',Repo(),Agent(),Sanitizer())
    assert [m.source for m in mapped]==['system','dataset','ai']
    assert not unknown
    assert len(approved_dataset_entries(mapped))==1
