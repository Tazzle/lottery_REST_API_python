import falcon
import json
import os
import errno
import random
import ticket


class TicketResource(object):
    
    def __init__(self):
        self.ticket_store = '/Users/$UNAME/GitHub_Repos/lottery/tickets/'
        #create folder if not already exists
        try:
            os.makedirs('tickets')
        #ignore error related to folder already existing
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise      


    def on_get(self, req, resp):
        if req.get_param("id"):
            ticket_id = req.get_param("id")
            ticket_value = ticket.get_ticket_from_xml(ticket_id)        
            resp.body = ('Ticket ' + ticket_id + ':' + '\n\n' + str(ticket_value))
            resp.status = falcon.HTTP_200
        else:
            resp.body = resp.body = '{"message": "No ID provided"}'
            resp.status = falcon.HTTP_400

    
    def on_post(self, req, resp):
        #generates new ticket
        if req.get_param_as_int("lines"):
            num_of_lines = req.get_param_as_int("lines")
            if(num_of_lines <= 0):
                resp.body = '{"message": "number of lines should be at least 1"}'
                resp.status = falcon.HTTP_400
            else:
                new_ticket = ticket.Ticket(num_of_lines)
                new_ticket.add_ticket_to_xml()
                resp.body = json.dumps("New ticket generated with " + str(num_of_lines) + " lines, ticket ID = " + str(new_ticket.id))
                resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps("Expects 1 parameter; 'lines")
            resp.status = falcon.HTTP_400

    #test 
    #when working with multiple parameters put url into quotes otherwise only recognises first argument
    #in the shell the ampersand is used for forking processes so does not behave as expected    
    #http PUT "localhost:8000/ticket?lines=3&id=10e477e2-1458-447c-8e83-80c37f024225"        
    def on_put(self, req, resp):
        if req.get_param("id") and req.get_param("lines"):
            ticket_id = req.get_param("id")
            num_of_lines = req.get_param("lines")
            f = open(os.path.join(self.ticket_store, ticket_id + ".html"), 'a')
            if(f):
                new_lines = ticket.generate_lines(num_of_lines)
                for line in new_lines:
                   f.write("<p>" + str(line) + "</p>")
                resp.body = json.dumps("Ticket " + ticket_id + " updated with " + num_of_lines + " lines")
                resp.status = falcon.HTTP_200
                f.close()
            else:
                resp.body = json.dumps("File not found")
                resp.status = falcon.HTTP_404            
        else:
            resp.body = json.dumps("Expects 2 parameters; 'ID' and 'lines'")
            resp.status = falcon.HTTP_400


    #todo:
    #refactor
    #idempotent. semantics. etc.
    #other parts of requirement doc.
           


        
       
        




    