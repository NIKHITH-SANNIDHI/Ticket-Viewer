import unittest
from unittest import mock
import ticket_viewer
import json
import requests_mock
from mock import patch
import io


class TestTicketViewer(unittest.TestCase):

    def test_get_creds_json(self):
        result = ticket_viewer.get_creds()
        self.assertIsNotNone(result)

    def test_get_creds_inner_details(self):
        result = ticket_viewer.get_creds()
        self.assertIn("zendesk.com", result['url'])
        self.assertIn("@", result['user'])
        self.assertIsNotNone(result['auth_token'])

    def test_print_menu(self):
        result = ticket_viewer.print_menu()
        self.assertIsNone(result)   
        

    def test_get_requested_data(self):
        creds = ticket_viewer.get_creds()
        
        data = ticket_viewer.get_requested_data(creds, "/api/v2/tickets/11")
        
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/8")['ticket']['requester_id'], 421868146372)    
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/11")['ticket']['subject'], "magna reprehenderit nisi est cillum")    
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/10000")['error'], "RecordNotFound") 
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/0")['error'], "RecordNotFound")    
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/tickets/12345")['description'], "Not found")
        self.assertEqual(ticket_viewer.get_requested_data(creds, "/api/v2/dummy/api")['error'], "InvalidEndpoint")      


    def test_25_tickets(self):
        creds = ticket_viewer.get_creds()
        data = ticket_viewer.get_requested_data(creds, "/api/v2/tickets?page[size]=25")
        self.assertLessEqual(len(data['tickets']), 25)

        if data['meta']['has_more']:
            self.assertIsNotNone(data['meta']['after_cursor']) 
            data = ticket_viewer.get_requested_data(creds, "/api/v2/tickets?page[size]=25&page[after]="+data['meta']['after_cursor'])
            self.assertLessEqual(len(data['tickets']), 25)

    def test_100_tickets(self):
        creds = ticket_viewer.get_creds()
        data = ticket_viewer.get_requested_data(creds, "/api/v2/tickets")
        self.assertLessEqual(len(data['tickets']), 100)



if __name__ == '__main__':
    unittest.main()