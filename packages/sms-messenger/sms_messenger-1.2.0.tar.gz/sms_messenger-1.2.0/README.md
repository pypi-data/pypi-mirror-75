# SMS Messenger

A simple Python package for sending messages over SMS Gateways.

## Description

SMS Messenger is a simple Python package that enables the user to send and read text messages via [SMS Gateways.](https://en.wikipedia.org/wiki/SMS_gateway) This package handles all the sending and reading of emails to SMS addresses. Requires an email to setup.

## Dependencies

[imapclient](https://github.com/mjs/imapclient)  
[pyzmail](https://github.com/aspineux/pyzmail)  
An Email _Preferably Gmail_

## Features

- Simple to use for sending and reading messages
- easy installation
- Lightweight with minimal external dependencies
- Docstrings

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sms-messenger.

```bash
pip install sms_messenger
```

## Usage

```python
import sms_messenger
email = "example@gmail.com"
paswd = "FooBar"
addresses = ['+12003004000@tmomail.net','+15006007000@txt.att.net'] #must specify gateway domain

server = sms_messenger.messageManager(email,paswd) #create a messageManager Object
print(server.getGateways()) #US SMS Gateways
server.sendTextMessage("Hello World!",addresses)

server.sendTextMessage("This is the Body",'tmpEmail@email.com','This is the subject') #works with emails too

replies = server.getTextMessages()
print(replies)

server.delMessagesToSMS(addresses) #Deletes from Sent Folder
```

## Help

__If using gmail, look under the [security tab](https://myaccount.google.com/security) and turn ON Less secure app access.  
![example.png](/img/example.png)  
It must be on for the package to work.__

## Docstring

```
Help on messageManager in module sms_messenger object:

class messageManager(builtins.object)
 |  messageManager(email, paswd, smtp='smtp.gmail.com', port=587)
 |  
 |  A simple class to handle sending and reading text messages via SMS Gateways.
 |  
 |  Dependencies:
 |      imapclient: https://github.com/mjs/imapclient
 |      pyzmail: https://github.com/aspineux/pyzmail
 |  
 |  Attributes:
 |      email: a string containing the email from which the texts will be sent.
 |      paswd: a string containing the password for the email above.
 |      stmp: (optional) a string containing the name of the stmp server.
 |      port: (optional) an int containing the port number to connect to smtp.
 |      SMS_Gateways_US: a dictionary containing the mobile carrier and their respective gateway
 |      GMAIL_FOLDERS: a list containing the respective names of gmail folders
 |      SEARCH_KEYS: a list containing all available search keys
 |  
 |  Methods defined here:
 |  
 |  __init__(self, email, paswd, smtp='smtp.gmail.com', port=587)
 |      Initialize self.
 |      
 |      Note:
 |          If not using gmail, the smtp and port must be specified.
 |  
 |  checkAccess(self)
 |      Attempts to log into the email server
 |      
 |      Returns:
 |          String on success, Nothing otherwise
 |  
 |  delMessagesBySelf(self, folder='[Gmail]/Sent Mail')
 |      Deletes all emails sent.
 |      
 |      Args:
 |          folder: (optional) Folder to be deleted from
 |          
 |      Returns:
 |          String on success, Nothing otherwise
 |  
 |  delMessagesByUIDs(self, UIDs, folder)
 |      Deletes all emails from UID list.
 |      
 |      Args:
 |          UIDs: Python list containing Unique IDs of the emails to be deleted
 |          folder: (optional) Folder to be deleted from
 |          
 |      Returns:
 |          String on success, Nothing otherwise
 |  
 |  delMessagesFromSMS(self, sms_address, folder='INBOX')
 |      Deletes all emails from aspecified sms gateway.
 |      
 |      Args:
 |          sms_address: String containing the sms from which emails will be deleted
 |          folder: (optional) Folder to be deleted from
 |          
 |      Returns:
 |          String on success, Nothing otherwise
 |  
 |  delMessagesToSMS(self, sms_address, folder='[Gmail]/Sent Mail')
 |      Deletes all emails to specified sms gateway.
 |      
 |      Args:
 |          sms_address: List containing the sms to which emails will be deleted
 |          folder: (optional) Folder to be deleted from
 |          
 |      Returns:
 |          Dictionary on success, Nothing otherwise
 |  
 |  getAddressesFromUIDs(self, UIDs, folder, readOnly=False)
 |      Returns the addresses from specified UIDs. 
 |      
 |      Args:
 |          UIDs: List of UIDs
 |          folder: folder from which the UIDs came
 |          readOnly: (optional) Whether or not to mark the messages as read.
 |      
 |      Returns:
 |          a dictionary containing the UID and address as a pair.
 |  
 |  getFolders(self)
 |      Returns all the folders available.
 |      
 |      Returns:
 |          List containing all folders availabe
 |  
 |  getGateways(self)
 |      Returns all the US Mobile Carriers and respective SMS Gateways.
 |      
 |      Returns:
 |          SMS_GATEWAYS_US
 |  
 |  getGmailFolders(self)
 |      Returns all Gmail folders.
 |      
 |      Returns:
 |          GMAIL_FOLDERS
 |  
 |  getMessagesFromUIDs(self, UIDs, folder, readOnly=False)
 |      Returns the parsed message from specified UIDs. 
 |      
 |      Args:
 |          UIDs: List of UIDs
 |          folder: folder from which the UIDs came
 |          readOnly: (optional) Whether or not to mark the messages as read.
 |      
 |      Returns:
 |          a dictionary containing the UID and message as a pair.
 |  
 |  getSearchKeys(self)
 |      Returns all search keys.
 |      
 |      Returns:
 |          SEARCH_KEYS
 |  
 |  getTextMessages(self, newMessagesOnly=False, returnUID=False)
 |      Grabs all recieved messages
 |      
 |      Retrieves all text messsages. Only retrieves the body of the email.
 |      
 |      Args:
 |          newMessagesOnly: (optional) Only retrieve unread messages
 |          returnUID: (option) Whether or not to return the UIDs
 |      
 |      Returns:
 |          Default:
 |              Python Dictionary containing the sms_address and a list of messages as a pair.
 |              Example
 |      
 |              {'+12003004000@tmomail.net': ['Hello','World'], '+15006007000@tmomail.net': ['foo','bar']}
 |              
 |              To get the message as a list just use exampleDict[sms_address]
 |      
 |          returnUID=True:
 |              Python Dictionary containing the sms_address and a dictionary of UID: message as a pair.
 |              example:
 |      
 |              {'+12003004000@tmomail.net': {123: 'Hello', 456: 'World'}}
 |  
 |  getTextMessagesFrom(self, sms_address, newMessagesOnly=False, returnUID=False)
 |      Grabs all messages sent by the sms address.
 |      
 |      Retrieves all text messsages sent by the specified sms address.
 |      Only retrieves the body of the email.
 |      
 |      Args:
 |          sms_address: List of strings containing the specified address.
 |          newMessagesOnly: (optional) Only retrieve unread messages
 |          returnUID: (option) Whether or not to return the UIDs
 |      
 |      Returns:
 |          Default:
 |              Python Dictionary containing the sms_address and a list of messages as a pair.
 |              Example
 |      
 |              {'+12003004000@tmomail.net': ['Hello','World'], '+15006007000@tmomail.net': ['foo','bar']}
 |              
 |              To get the message as a list just use exampleDict[sms_address]
 |      
 |          returnUID=True:
 |              Python Dictionary containing the sms_address and a dictionary of UID: message as a pair.
 |              example:
 |      
 |              {'+12003004000@tmomail.net': {123: 'Hello', 456: 'World'}}
 |  
 |  searchFolder(self, folder, *searchKeys)
 |      Searches the specified folder.
 |      
 |      Searches the folder specified by using searchKeys.
 |      Example:
 |          searchFolder('INBOX','FROM','foobar@email.com')
 |          searchFolder('[Gmail]/All Mail','UNSEEN','SUBJECT','Hello World','FROM','foobar@email.com')
 |          
 |      NOTE:
 |          UIDs are folder specific. A UID from INBOX only applies to INBOX.
 |          
 |      Args:
 |          folder: Folder to search from
 |          *searchKeys: List of search keys to be used
 |          
 |      Returns:
 |          List of UIDs for the specified folder.
 |  
 |  sendTextMessage(self, message, sms_address, subject='I am a bot. Beep Boop.')
 |      Sends text message to specified sms_address.
 |      
 |      Composes an email from the message and subject and sends it to the recipients.
 |      Example:
 |          I am a bot. Beep Boop./ Hello World.
 |      
 |      Args:
 |          sms_address: List of strings containing the addresses to be sent
 |          message: Text message to be sent.
 |          subject: (optional) message to be used on subject line.
 |      
 |      Returns:
 |          String on success, Nothing otherwise.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  GMAIL_FOLDERS = ['INBOX', '[Gmail]/All Mail', '[Gmail]/Drafts', '[Gmai...
 |  
 |  SEARCH_KEYS = ['BEFORE', 'ON', 'SINCE', 'SUBJECT', 'BODY', 'TEXT', 'FR...
 |  
 |  SMS_GATEWAYS_US = {'AT&T': 'txt.att.net', 'Alltel': 'sms.alltelwireles...
```

## License
[MIT](/LICENSE)