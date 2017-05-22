# Mailbot-in-Python

This is a cross-platform Mailbot written in Python. It uses inbuilt libraries like smtplib,imaplib for handling all mails.

With this you can filter mails by providing regular expressions and this will generate a beep sound on your system when it will encounter a mail of your type.

To run this for our mailaccount you need to do following steps:
        
        1) Allow imap protocol in your mail settings
        
        2) If you are using gmail make sure you switch on allow access to less secure apps
        
        
This contains a class Mailbot and contains functions for :-
        
        1) Sending Mails.
        
        2) Count Number of unread Mails.
        
        3) Logout.
        
        4)Total number of Mails in your inbox.
        
        5)Filter mails and generate alerts accordingly
        
This mailbot will attach to your mail and help you filter messages accordingly. If no regular expression is not specified then by default it generates alerts for all mails received by you.

To use this mailbot just instantiate the class and specify parameters in the function.

Functions available are:-

        1)logout():- This will logout and stop all the services
        
        2)count_unread_mails():- This will return you an integer specifying the unseen messages in your inbox
        
        3)send_mails(toaddr,message,subject):- need to specify the parameters in the function and will send mail to toaddr
        
        4)attach_to_mail(regular_expression=None,timeout=None):- If no timeout is specified then will run until the program is breaked explicitly. Regular_expression needs to be a string.
        

For linux users to get alert sound on your machine you need to install sox by:- 
         
         sudo apt-get install sox
         
 


