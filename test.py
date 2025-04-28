import requests

# Your Flask server URL
url = "http://localhost:5000/chat"

# Message you want to send
data = {
    "message": "Hello, how are you?"
}

# Send a POST request
response = requests.post(url, json=data)

# Print the server response
if response.status_code == 200:
    print("Response:", response.json()['response'])
else:
    print("Error:", response.status_code, response.text)
