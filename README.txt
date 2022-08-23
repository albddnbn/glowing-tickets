Directions for use:

This program was originally intended to be a 'Ticket Response Saver' program, that would allow a technician to store frequently used responses to support tickets.

The technician can then access those responses through the GUI, and use buttons (a button corresponding to each stored response) to copy the response to clipboard.

There is a textbox above where the response buttons are shown on the View Responses window. Type the user's name in this textbox, and it will be inserted into the ticket reply
when the reply is copied to clipboard.
    - When responses are created - the creator will add $ticketowner where they would like the ticket owner's name to be placed in the ticket reply.


*When creating/storing a ticket reply:
    - the title will be inserted into the filename after 'response-', and each response file will have a '.txt' file extension
    - ticket responses are stored in the './responses' directory

    - ticket response goes in textbox below title, please insert '$ticketowner' (without the quotes) where the ticket owners name should be in the response.


The program still has quirks/bugs, and still needs a lot of work  - its definitely a 'beta version'!
    - hoping to 'upgrade' the GUI to tkinter or wxpython
    - create a feature which allows tech to store/choose greetings or signatures to go with the ticket response