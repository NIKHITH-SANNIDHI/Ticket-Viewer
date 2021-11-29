# Ticket-Viewer

This is a Python-based CLI application to connect to Zendesk, fetch tickets from your Zendesk account and view tickets. This repository consists of the following:

## File descriptions

* ticket_viewer.py -> the main driver file for the application. 
* credentials.json -> the Zendesk API credentials (URL, username and auth_token) must be configured here. Currently, this json holds dummy values and they need to be replaced with your account credentials (see steps below).
* test_ticket_viewer.py -> the tester file that performs unit tests on the main python application.

Before using this application, please make sure you have created an account on Zendesk to use Zendesk APIs. Also, enable **Token Access** option in the API section and generate an API token. This token will be used by Zendesk authenticate you when you use Ticker-Viewer application to fetch tickets from your Zendesk account and view on CLI. 

## Initial Configuration
Things to set-up using the Ticket-Viewer
1. Clone this repository using `git clone https://github.com/NIKHITH-SANNIDHI/Ticket-Viewer.git`
2. Open credentials.json and please make the following modifications:
     1. Replace `<dummy-url>` with your Zendesk account URL. 
     2. Replace `<dummy-email>` with the primary email on you Zendesk account.
     3. Replace `<dummy-key>` with the API token that you've generated in the API section. 
3. Ensure you have the following python packages installed on your system to run the Ticket-Viewer application:
     1. requests (to make API calls)
     2. json (to hande JSON data)
     3. tabulate (to display the data in a tabulated form)


That's all! If you want to perform unit tests on the Ticket-Viewer python code, you need to use the test_ticket_viewer.py. Before running this file, please ensure you have the following python packages installed on your system:
1. unittest (for running unit tests)
2. requests_mock (
3. mock

## Running the application locally
Once the initial configuration is done, your system is now ready to run the Ticket-Viewer. To run the application, open a command prompt in the directory you cloned this repository and run the following command:
`python3 ticket_viewer.py`

You will see a welcome message. Type 'menu' to continue and you will find various options to view your Zendesk tickets. A screenshot of the options are given below:

![image](https://user-images.githubusercontent.com/15651310/143792127-92a9ba63-56aa-4843-b041-e3705ff46dd3.png)

## Application Features
This CLI application meets the requirements of the following features:
1. **Make connection with Zendesk API:** With help of the Zendesk credentials configured in the credentials.json, the application connects to your Zendesk account using Zendesk API
2. **Fetches ticket data:** The application makes various GET API calls to fetch the ticket data from Zendesk. 
3. **Displays all tickets:** When user inputs option 1, the code makes a GET API call to get all the tickets and displays in a tabulated form. As given in [Zendesk API documentation](https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/#list-tickets), the API returns 100 tickets at the maximum and so a maximum of 100 tickets will be displayed in the table.
4. Displays a ticket: When user inputs option 2, the user is prompted to enter a ticket ID. The code makes a GET API call using the given ticket ID and displays the ticket in a tabulated form.  
5. Paging through tickets: When user inputs option 3, the code makes a GET API call to fetch first 25 tickets and display in a tabulated form. The user is prompted to enter an option to navigate to next or previous pages or return back to the main menu. As per requirements and for simplicity reasons, the user can view 'blocks of 25 tickets' at a time when using this option.

Everytime the menu is displayed, the user always have a the option to quit the application by just typing 'quit'.


## Application Design
All the concerns related to the application are separated into just 3 files which enhances usability. The **credentials.json** is like a configuration file where the user will modify the secrets with their own's to make the application work for the user. The **ticket_viewer.py** is the main file that should run for the application to work. The code in this file is separated by various functions dealing with a specific concern (See code comments for more details). 
I also considered the MVC approach for my project but since I am using command prompt to interact with the user (no need of UI logic), less data (around 100 tickets so no need of database), I believed developing a python file to run the application makes it very simple to understand and easy to run. 

The program is designed such that every repitative concern is handled by specific function. Upon starting the code, the application greets you with a welcome message and gives you an option to proceed forward to the menu. The purpose of each function and API used (if applicable) is tabulated below. 

| Function | Purpose | API used  |
| ---- | ---- | ---- |
| `display_all_tickets()` | Display all tickets in a list | `/api/v2/tickets/` |
| `display_a_ticket()` | Display a ticket with ticket ID | `/api/v2/tickets/{ticket-id}` |
| `display_25_tickets()` | Display 25 tickets at a time with paging option | `/api/v2/tickets?page[size]=25` |
| `get_requested_data()` | Makes a GET API call for the given URL and returns json response | _Not Applicable_ |
| `print_menu()` | Display menu options | _Not Applicable_ |
| `get_creds()` | Load the credentials.json comprising of required secrets to connect to Zendesk | _Not Applicable_ |

As the first three functions needs to make an GET API call, the program logic dealing with making GET calls and handling error responses are moved to `get_requested_data()`

For handling the ticket data, I thought of two options:
1. Make one GET all tickets API call, cache the data and display the data based on the user option.
2. Make GET API calls without caching the data and display the response data in a tabulated form.

I think the caching option looks great, especially when dealing with large amount of tickets. But our project deals with less tickets (100 tickets as given in the tickets.json). Keeping in mind of simplicity and the scale of this task, I believed that using the caching option for less tickets will be an memory overhead and making Zendesk API for every feature will be optimal. The response time is very quick as there are less tickets for this project. Hence, I decided to go with the second option. Fortunately, Zendesk offers APIs to satisfy the three main requirements (displaying all, one and 25 tickets with paging option) and I make the appropriate API call when user enters an option. As I am making the API call for every option, I need not store the ticket data at all. This eliminates the memory overhead of storing 100 tickets and also synchornization concerns if the data in Zendesk gets updated. So, the displayed data is always real-time and latest.


The unit testing framework is implmented in a separate file that independantly tests the code in ticket_viewer.py. 


## Application Screenshots

**Application output when user inputs option 1:**
![image](https://user-images.githubusercontent.com/15651310/143793683-16e3243d-b07c-4378-a818-eade5c0d13c3.png)


**Application output when user inputs option 2 and inputs a ticket ID:**
![image](https://user-images.githubusercontent.com/15651310/143793706-f1b5e7f1-6828-4384-af97-742c207c6031.png)

**Application output when user inputs option 3:**
![image](https://user-images.githubusercontent.com/15651310/143793826-53aac636-4382-4e80-8f8e-2d279408ef26.png)


