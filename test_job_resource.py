import requests

print(
    requests.post('http://127.0.0.1:8080/api/v2/jobs/', json={
        'team_leader': 1,
        'job': 'JOB',
        'work_size': 18,
        'collaborators': '2, 3, 4',
        'is_finished': False,
    }))

print(requests.get('http://127.0.0.1:8080/api/v2/jobs/').json())

print(requests.get('http://127.0.0.1:8080/api/v2/jobs/3').json())

print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/3'))
