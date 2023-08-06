# ----------------------------------------------------------------------------------------------------------------------
# SalesForce credential
# ----------------------------------------------------------------------------------------------------------------------

username=''
password=''
security_token=''

#If security_token is unknown, reset the latter from SalesForce to receive new token via email

# salesforce passwords usually expires every 90 days
# when salesforce password is updated, a new security token will be emailed to the user
# when password expires, the scripts still connects to the api but no data will be retrieved

# ----------------------------------------------------------------------------------------------------------------------
# sftp connection to BoardEx
# ----------------------------------------------------------------------------------------------------------------------
# credentials are provided by BoardEx
myHostname = ""
myUsername = ""
myPassword = ""

# ----------------------------------------------------------------------------------------------------------------------
# Upload to sftp
# ----------------------------------------------------------------------------------------------------------------------
# To upload to sftp server set upload_to_sftp = True
# By default the upload_to_sftp is set to false. (The csv files will not be uploaded to the sftp server)

upload_to_sftp = False

# ----------------------------------------------------------------------------------------------------------------------
# log level
# ----------------------------------------------------------------------------------------------------------------------
# Python has 6 log levels: CRITICAL, ERROR, WARNING, INFO, DEBUG and NOTSET
# The default log level is set to CRITICAL if not selected
# If log_level is NOTSET, no logs will be provided

log_level = 'DEBUG'

# ----------------------------------------------------------------------------------------------------------------------
# contact_query - gets the name of the contacts, role and name of their company who does not have a BoardExID
# ----------------------------------------------------------------------------------------------------------------------
query_email = True # if set to False, Email data will be removed from the contact_query

# ----------------------------------------------------------------------------------------------------------------------
# company_query - gets company's name and address which does not have a BoardExID
# ----------------------------------------------------------------------------------------------------------------------
# BoardEx requires the following from salesforce's ACCOUNT table
# ID, Name, BillingCity, BillingCountry FROM Account
# The sql company query "SELECT ID, Name, BoardEx__Client_Organization_ID__c, BillingCity, BillingCountry FROM Account WHERE BoardEx__Client_Organization_ID__c = ''"

company_query = "SELECT ID, Name, BoardEx__Client_Organization_ID__c, BillingCity, BillingCountry FROM Account WHERE BoardEx__Client_Organization_ID__c = ''"

# ----------------------------------------------------------------------------------------------------------------------
# contact_query - gets the name of the contacts, role and name of their company who does not have a BoardExID
# ----------------------------------------------------------------------------------------------------------------------
# BoardEx requires the following from salesforce's Contact table
# ID, FirstName, LastName, Email, Title, Account.Name FROM Contact
# The sql contact query "SELECT ID, FirstName, LastName, BoardEx__Client_Individual_ID__c, Title, Account.Name FROM Contact WHERE BoardEx__Client_Individual_ID__c =''"

contact_query = "SELECT ID, FirstName, LastName, BoardEx__Client_Individual_ID__c,  Email, Title, Account.Name FROM Contact WHERE BoardEx__Client_Individual_ID__c !=''"

# ----------------------------------------------------------------------------------------------------------------------
# UserDetails_query - gets personal data from individuals contacts from salesforce
# ----------------------------------------------------------------------------------------------------------------------
# BoardEx requires the following from salesforce's Contact table
# FirstName, LastName, Email, Title  FROM Contact
# The sql company query "SELECT ID, FirstName, LastName, Email, Title FROM Contact"

UserDetails_query = "SELECT ID, FirstName, LastName, Email, Title FROM Contact"

# ----------------------------------------------------------------------------------------------------------------------
# ContactDetails_query - gets the owner's email address and only their customer's BoardExID if available
# ----------------------------------------------------------------------------------------------------------------------
# BoardEx requires the following from salesforce's Contact table
# email address of the owner who owns the contact and the BoardExID of their customer or client FROM contact
# The sql company query "SELECT Contact.Owner.Email, BoardEx__Client_Individual_ID__c from contact where BoardEx__Client_Individual_ID__c != ''"

ContactDetails_query = "SELECT Contact.Owner.Email, BoardEx__Client_Individual_ID__c from contact where BoardEx__Client_Individual_ID__c != ''"

# ----------------------------------------------------------------------------------------------------------------------
# Local path
# ----------------------------------------------------------------------------------------------------------------------
# This where data will be kept after being downloaded from SalesForce
path_local_temp = ''