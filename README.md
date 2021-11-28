# Ticket-Viewer

This is a Python-based CLI application to connect to Zendesk, fetch tickets from your Zendesk account and view tickets. This repository consists of the following:

* ticket_viewer.py -> the main driver file for the application. 
* credentials.json -> the Zendesk API credentials (URL, username and auth_token) must be configured here. Currently, this json holds dummy values and they need to be replaced with your account credentials (see steps below).
* test_ticket_viewer.py -> the tester file that performs unit tests on the main python application.

Before using this application, please make sure you have created an account on Zendesk to use Zendesk APIs. Also, enable **Token Access** option in the API section and generate an API token. This token will be used by Zendesk authenticate you when you use Ticker-Viewer application to fetch tickets from your Zendesk account and view on CLI. 

Steps to start using the Ticket-Viewer
1. Clone this repository using `git clone https://github.com/NIKHITH-SANNIDHI/Ticket-Viewer.git`
2. Open credentials.json and please make the following modifications:
     1. Replace `<dummy-url>` with your Zendesk account URL. 
     2. Replace `<dummy-email>` with the primary email on you Zendesk account.
     3. Replace `<dummy-key>` with the API token that you've generated in the API section. 
