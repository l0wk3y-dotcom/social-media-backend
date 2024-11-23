import requests

# The URL of your API endpoint
url = 'http://127.0.0.1:8000/accounts/user/users/1/'  # Update with the correct endpoint and ID

# The data you want to update (in this example, we're updating the user profile)
data = {
    "url": "http://127.0.0.1:8000/accounts/user/users/1",
    "user": {
        "username": "normal_user0",
        "first_name": "normal",
        "last_name": "user",
        "password":"DEFAULT"
    },
    "bio": "Software Developer(edited)",
    "profile_picture": "http://127.0.0.1:8000/media/PP/random_profilepic_J87ZkUG.jpeg",
    "website": "http://johndoe.com",
    "DOB": "2024-11-10",
    "banned": False,
    "facebook_link": "https://facebook.com/@kishan",
    "twitter_link": "https://x.com/@krish_jha",
    "instagram_link": "https://instagram.com/@krish_jha",
    "linkedin_link": "https://linkedin.com/@krish_jha"
}
# Profile picture to upload (if any)
files = {
    'profile_picture': open('media/PP/random_profilepic_kdkV3VZ.jpeg', 'rb')  # Replace with the actual file path
}

# Sending the PUT request
response = requests.put(url, data=data, files=files)

# Print response details
if response.status_code == 200:
    print("Profile updated successfully!")
    print(response.json())  # You can see the updated profile in the response
else:
    print(f"Error: {response.status_code}")
    print(response.text)
