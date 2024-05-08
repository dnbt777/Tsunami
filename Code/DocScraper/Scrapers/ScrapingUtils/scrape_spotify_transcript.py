import requests
import base64
import json

# Constants
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
BASE_URL = 'https://api.spotify.com/v1/'

def get_access_token(client_id, client_secret):
    """Authenticate and return the access token."""
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')

def search_podcasts(query, token, limit=10):
    """Search for podcasts using a query and return the results."""
    url = BASE_URL + 'search'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': query,
        'type': 'show',
        'market': 'US',
        'limit': limit
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def main():
    # Authenticate and get access token
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    
    # Search for podcasts
    query = 'technology'
    podcasts = search_podcasts(query, token)
    
    # Display the top 10 podcast results
    for i, show in enumerate(podcasts['shows']['items'], start=1):
        print(f"{i}. {show['name']} - {show['publisher']}")
        print(f"    Link: {show['external_urls']['spotify']}")
        print(f"    Description: {show['description'][:100]}...")  # Show first 100 characters of description

if __name__ == '__main__':
    main()