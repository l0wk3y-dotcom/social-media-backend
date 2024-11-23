import requests

# Define the endpoint URL
url = 'http://127.0.0.1:8000/accounts/user/7/picture'

# Open the image file in binary mode
with open('/home/lowkey/projects/EcommerceAPI/client/random_profilepic.jpeg', 'rb') as image_file:
    # Create the payload with the image
    files = {'image': image_file}
    
    # Send a POST request with the image file
    response = requests.post(url, files=files)

# Check the response
print(response.status_code)
print(response.json())  # This will show the response data if it's in JSON format
