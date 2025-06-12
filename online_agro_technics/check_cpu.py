import requests

username = 'playstationgabi'
token = 'bab99c8f82ee166c7fdb7e94a999906ba5da3533'

response = requests.get(
    f'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/',
    headers={'Authorization': f'Token {token}'}
)

if response.status_code == 200:
    print('✅ CPU quota info:')
    print(response.json())
else:
    print(f'❌ Got unexpected status code {response.status_code}: {response.text}')
