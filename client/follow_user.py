import requests

# URL to send the request to
url = "http://127.0.0.1:8000/accounts/user/8/follow"

# JWT token (replace 'your_jwt_token_here' with the actual token)
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNTYyNDAxLCJpYXQiOjE3MzE1NTg4MDEsImp0aSI6ImFhOWQ1ZDBkYzZiOTRiNDBiNzY2YzQ0ZWFkZmMyNTliIiwidXNlcl9pZCI6N30.W7GoXdg54FT9-lGbcFN3Hb9IfgxdkT8JMvb41HepOpc"

# Headers, including the Authorization header with the JWT token
headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, headers=headers)

# Check the response status and content
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code)
