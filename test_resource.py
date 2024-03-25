import requests

print(
    requests.post('http://127.0.0.1:8080/api/v2/users/', json={
        'name': 'Sonya',
        'surname': 'Red',
        'age': 18,
        'position': 'biologist',
        'speciality': 'pathologist',
        'address': 'module 2',
        'email': '123@q.com',
        'hashed_password': '321'
    }))

print(requests.get('http://127.0.0.1:8080/api/v2/users/').json())

print(requests.get('http://127.0.0.1:8080/api/v2/users/3').json())

print(requests.delete('http://127.0.0.1:8080/api/v2/users/3'))
