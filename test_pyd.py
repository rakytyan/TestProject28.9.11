from pydantic import BaseModel, Field
import pytest
import requests

token = 'get your own token'

class MKTU(BaseModel):
    clss: int = Field(alias="class")
    number: int = Field(...)
    name_ru: str = Field(...)
    name_en: str = Field(...)
    name_fr: str = Field(...)

class Suggestion(BaseModel):
    value: str = Field(...)
    unrestricted_value: str = Field()
    data: MKTU = Field(...)

def test_request_success():
    headers = {'Content-Type': 'application/json', 'Accept':'application/json', 'Authorization':'Token ' + token}
    query = {'query': 'рыба'}
    r = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/mktu', headers=headers, json=query)
    # print(r.json())
    assert r.status_code==200

def test_unauthorized_request():
    headers = {'Content-Type': 'application/json', 'Accept':'application/json', 'Authorization':'Token ' + 'XXXXXXXXXX'}
    query = {'query': 'рыба'}
    r = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/mktu', headers=headers, json=query)
    assert r.status_code==403

def test_request_without_query():
    headers = {'Content-Type': 'application/json', 'Accept':'application/json', 'Authorization':'Token ' + token}
    query = {'xyz': ''}
    r = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/mktu', headers=headers, json=query)
    resp = r.json()
    resp = resp['suggestions']
    suggestions = [Suggestion(**x) for x in list(resp)]
    assert r.status_code==200 and len(suggestions)==0

def test_response_structure():
    headers = {'Content-Type': 'application/json', 'Accept':'application/json', 'Authorization':'Token ' + token}
    query = {'query': 'рыба'}
    r = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/mktu', headers=headers, json=query)
    resp = r.json()
    resp = resp['suggestions']
    suggestions = [Suggestion(**x) for x in list(resp)]

def test_response_success():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие', 'data': {'class': '25', 'number': '250159', 'name_ru': 'куртки рыбацкие', 'name_en': 'fishing vests', 'name_fr': 'vestes de pêcheurs'}}, {'value': 'приманки пахучие для охоты и рыбалки', 'unrestricted_value': 'приманки пахучие для охоты и рыбалки', 'data': {'class': '28', 'number': '280194', 'name_ru': 'приманки пахучие для охоты и рыбалки', 'name_en': 'scent lures for hunting or fishing', 'name_fr': 'leurres odorants pour la chasse ou la pêche'}}, {'value': 'рыба неживая', 'unrestricted_value': 'рыба неживая', 'data': {'class': '29', 'number': '290047', 'name_ru': 'рыба неживая', 'name_en': 'fish, not live', 'name_fr': 'poissons non vivants'}}, {'value': 'рыба консервированная', 'unrestricted_value': 'рыба консервированная', 'data': {'class': '29', 'number': '290136', 'name_ru': 'рыба консервированная', 'name_en': 'fish, preserved', 'name_fr': 'poisson conservé'}}, {'value': 'рыба соленая', 'unrestricted_value': 'рыба соленая', 'data': {'class': '29', 'number': '290149', 'name_ru': 'рыба соленая', 'name_en': 'salted fish', 'name_fr': 'poisson saumuré'}}, {'value': 'рыба живая', 'unrestricted_value': 'рыба живая', 'data': {'class': '31', 'number': '310103', 'name_ru': 'рыба живая', 'name_en': 'fish, live', 'name_fr': 'poissons vivants'}}]}
    resp = resp['suggestions']
    suggestions = [Suggestion(**x) for x in list(resp)]
    assert len(suggestions) == 6
    assert suggestions[0].value == 'куртки рыбацкие'
    assert suggestions[0].data.clss == 25
    assert suggestions[0].data.number == 250159
    assert suggestions[0].data.name_fr == 'vestes de pêcheurs'

def test_missing_class():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': { 'number': '250159', 'name_ru': 'куртки рыбацкие', 'name_en': 'fishing vests', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_missing_number():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': { 'class': '25', 'name_ru': 'куртки рыбацкие', 'name_en': 'fishing vests', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_missing_name_ru():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': { 'class': '25', 'number': '250159', 'name_en': 'fishing vests', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_missing_name_en():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': { 'class': '25', 'number': '250159','name_ru': 'куртки рыбацкие', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_incorrect_class():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': {'class': 'class', 'number': '250159', 'name_ru': 'куртки рыбацкие', 'name_en': 'fishing vests', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_incorrect_number():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': {'class': 'class', 'number': '2501590', 'name_ru': 'куртки рыбацкие', 'name_en': 'fishing vests', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_incorrect_name_ru():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': {'class': 'class', 'number': '250159', 'name_ru': 'куртки рыбацкие1', 'name_en': 'fishing vests', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_incorrect_name_en():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': {'class': 'class', 'number': '250159', 'name_ru': 'куртки рыбацкие', 'name_en': '1fishing vests', 'name_fr': 'vestes de pêcheurs'}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]

def test_mising_MTKU():
    resp = {'suggestions': [{'value': 'куртки рыбацкие', 'unrestricted_value': 'куртки рыбацкие','data': {}}]}
    resp = resp['suggestions']
    with pytest.raises(ValueError):
        suggestions = [Suggestion(**x) for x in list(resp)]
