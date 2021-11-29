import unittest
import json
import ticket_viewer
import io
import requests

class TestTicketViewer(unittest.TestCase):

    #Test get_creds()
    def test_get_creds_json(self):
        result = ticket_viewer.get_creds()
        self.assertIsNotNone(result)

    #Test if valid details are configured in credentials.json
    def test_get_creds_inner_details(self):
        result = ticket_viewer.get_creds()
        self.assertIn("zendesk.com", result['url'])
        self.assertIn("@", result['user'])
        self.assertIsNotNone(result['auth_token'])

    #Test print menu is not returning anything
    def test_print_menu(self):
        result = ticket_viewer.print_menu()
        self.assertIsNone(result)   
        
    #Test if Zendesk APIs are working
    def test_api_working(self):
        creds = ticket_viewer.get_creds()

        response = requests.get(creds['url']+ "/api/v2/tickets", auth=(creds['user'], creds['auth_token']))
        self.assertEqual(response.status_code,200)

        response = requests.get(creds['url']+ "/api/v2/tickets/5", auth=(creds['user'], creds['auth_token']))
        self.assertEqual(response.status_code,200)
        
        response = requests.get(creds['url']+ "/api/v2/tickets?page[size]=25", auth=(creds['user'], creds['auth_token']))
        self.assertEqual(response.status_code,200)


    #Test if the returned data is correct.
    def test_get_requested_data(self):
        creds = ticket_viewer.get_creds()

        #Commenting the below as the reviewer's data will differ
        #self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/8")['ticket']['requester_id'], 421868146372)    
        #self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/11")['ticket']['subject'], "magna reprehenderit nisi est cillum")    
        #If you want to test the above at your end, please uncomment the above two statements, update the requester ID and subject from your Zendesk data. The given values are from the data at end
        
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/100000000000000")['error'], "RecordNotFound") 
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/0")['error'], "RecordNotFound")    
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/1234567890123456789")['description'], "Not found")
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/dummy/api")['error'], "InvalidEndpoint")      

    #Test if paging API is return less than or equal to 25 tickets
    def test_25_tickets(self):
        creds = ticket_viewer.get_creds()
        data = ticket_viewer.get_requested_data(creds, "/api/v2/tickets?page[size]=25")
        self.assertLessEqual(len(data['tickets']), 25)

        if data['meta']['has_more']:
            self.assertIsNotNone(data['meta']['after_cursor']) 
            data = ticket_viewer.get_requested_data(creds, "/api/v2/tickets?page[size]=25&page[after]="+data['meta']['after_cursor'])
            self.assertLessEqual(len(data['tickets']), 25)

    #Test if GET all tickets API is return less than or equal to 100 tickets
    def test_100_tickets(self):
        creds = ticket_viewer.get_creds()
        data = ticket_viewer.get_requested_data(creds, "/api/v2/tickets")
        self.assertLessEqual(len(data['tickets']), 100)

if __name__ == '__main__':
    unittest.main()