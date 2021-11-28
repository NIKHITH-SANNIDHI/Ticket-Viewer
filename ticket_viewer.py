import requests
import json
from tabulate import tabulate

def get_creds():
    try:
        creds=None
        with open('credentials.json') as f:
            creds = json.load(f)
        if creds['url']==None or creds['user']==None or creds['auth_token']==None:
            print("One or more values in the credentials.json is missing")    
    except:
        print("Error while reading credentials.json")
    return creds

def print_menu():
    print("\nSelect view options:")
    print("* Press 1  to view all tickets")
    print("* Press 2  to view a ticket")
    print("* Press 3  to list 25 tickets per page")
    print("Type quit to exit")


def get_requested_data(creds, api_url):

    url = creds['url'] + api_url
    user = creds['user']
    pwd = creds['auth_token']

    response = requests.get(url, auth=(user, pwd))
    
    data = response.json()

    if response.status_code != 200:
        if data['error']=='RecordNotFound':
            print("Given ticket ID is not found.")
        else:    
            print('Error while making GET request: ', data['error'])
    
    #print(data)
    return data


def display_a_ticket(creds):
    ticket_id = input("Enter ticket number:")
    try:
        data = get_requested_data(creds, "/api/v2/tickets/" + ticket_id)
        display_tabulated_format([data['ticket']])
    except:
        return

def display_all_tickets(creds):
    try:
        data = get_requested_data(creds, "/api/v2/tickets")
        display_tabulated_format(data['tickets'])
    except:
        return    
    
def display_tabulated_format(tickets):
    table =[]
    for ticket in tickets:
        row = [ticket['id'], ticket['requester_id'], ticket['assignee_id'], ticket['status'], ticket['subject']]
        table.append(row)
    print(tabulate(table, headers=["Ticket ID", "Requester ID", "Assignee ID", "Status", "Subject"]))

def display_25_tickets(creds):
    data = get_requested_data(creds, "/api/v2/tickets?page[size]=25")
    display_tabulated_format(data['tickets'])

    #print(len(data))
    #print(len(data['tickets']))

    start_counter=0
    
    
    while True:
        nav_string = ""

        #Showing the 'previous' option only if user is not on the first page 
        if start_counter != 0:
            nav_string = "previous page (p)"

        #Showing the 'next' option only if there are more pages available. 
        if data['meta']['has_more']:
            if nav_string !="":
                nav_string = nav_string + " or next page (n)"
            else:
                nav_string = "next page (n)"                

        #Always show return to main menu option
        nav_string = nav_string + " or return to main menu (r)?"
    
        navigate = input("\nDo you want to navigate to " + nav_string + " Enter the letter given in the parenthesis: ")

        if navigate == 'p' and start_counter != 0:
            data = get_requested_data(creds, "/api/v2/tickets.json?page[size]=25&page[before]="+data['meta']['before_cursor'])
            display_tabulated_format(data['tickets']) 
            start_counter = 0 if start_counter<25 else start_counter - 25

        elif navigate == 'n' and data['meta']['has_more']:
            data = get_requested_data(creds, "/api/v2/tickets.json?page[size]=25&page[after]="+data['meta']['after_cursor'])
            display_tabulated_format(data['tickets'])
            start_counter = start_counter + 25
        
        elif navigate == 'r':
            return    
        
        else:    
            print("Invalid input.")


if __name__ == "__main__":

    try:
        #Loading required credentials to connect to Zendesk API
        creds = get_creds()

        print("Hi there!")
        print("Welcome to the ticket viewer")
        print("-----------------------------")

        #user_option = input("Type 'menu' to view options or 'quit' (or any random input) to exit\n")

        user_value = True #if user_option == "menu" else  False


        while user_value:
            print_menu()
            user_input = input()

            if(user_input=="1"):
                display_all_tickets(creds)
            elif(user_input=="2"):
                display_a_ticket(creds)
            elif(user_input=="3"):
                display_25_tickets(creds)
            elif(user_input=="quit"):
                break
            else:
                print("Invalid input. Please re-enter a valid input.")    
    except:
        print("Ticket Viewer has ran into an error.")

    print("Thank you for using the ticket viewer. Goodbye.")