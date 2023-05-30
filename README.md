


## How to Get Reddit API Credentials
To access Reddit's API, you will need to create an application and get API credentials. Follow these steps to get your API credentials:

1. Go to the Reddit Apps page.

2. Click the "Create App" or "Create Another App" button.

3. Choose the "web app" option.

4. Give your app a name and description.

5. In the "about url" and "redirect uri" fields, enter the URL of the website you want to use the API credentials for. If you don't have a website, you can use http://localhost:8000.

6. Choose the "script" option for the "App Type" field.

7. Click the "Create App" button.

8. On the next page, you will see your "client ID" and "client secret" listed under the name of your app. Make note of these values as you will need them to authenticate with Reddit's API.

9. To authenticate with Reddit's API, you will also need to provide a "User Agent" string in the header of your API requests. You can choose any string you want, but it should include a name or description of your app, as well as contact information for the app developer. For example: