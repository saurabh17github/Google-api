import requests
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View

# Step 1: Initialize Google Calendar
class GoogleCalendarInitView(View):
    def get(self, request):
        # Step 1: Perform initialization steps here
        # You can use the provided credentials to authenticate with Google Calendar API
        # Implement the necessary code to start step 1 of the OAuth process

        # Redirect the user to the consent screen
        client_id = 'YOUR_CLIENT_ID'
        redirect_uri = 'http://localhost:8000/google/calendar/redirect/'  # Replace with your actual redirect URI
        scope = 'https://www.googleapis.com/auth/calendar.readonly'

        consent_url = f'https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code'
        return redirect(consent_url)

# Step 2: Handle redirect and retrieve access_token
class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Step 2: Handle redirect request sent by 'need to implement mechanism'
        # Implement the necessary code to handle the redirect and retrieve the authorization code
        
        authorization_code = request.GET.get('code')

        # Exchange the authorization code for an access token
        token_url = 'https://oauth2.googleapis.com/token'
        client_id = '983546603378-u39hccg8onl5tjp9b879tg2p34778ba6.apps.googleusercontent.com'
        client_secret = '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'
        redirect_uri = 'http://localhost:8000/google/calendar/redirect/'  # Replace with your actual redirect URI
        grant_type = 'authorization_code'

        data = {
            'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type,
        }
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            access_token = response.json().get('access_token')

            # Store the access_token in the session
            request.session['access_token'] = access_token

            # Redirect or return a response as per your application's needs
            return redirect('calendar-home')
        else:
            return HttpResponse('Failed to retrieve access token.')

# Home view to demonstrate access token usage
class CalendarHomeView(View):
    def get(self, request):
        # Retrieve the access_token from the session
        access_token = request.session.get('access_token')

        # Use the access_token to make API requests or perform other actions
        if access_token:
            # Example: Use the access_token to make a GET request to Google Calendar API
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get('https://www.googleapis.com/calendar/v3/calendars/primary/events', headers=headers)

            if response.status_code == 200:
                # Successful API request
                events = response.json()['items']
                return HttpResponse(f'Retrieved {len(events)} events from Google Calendar.')
            else:
                return HttpResponse(f'Failed to retrieve events. Error: {response.content}')

        else:
            return HttpResponse('Access Token not found. Please authenticate first.')
