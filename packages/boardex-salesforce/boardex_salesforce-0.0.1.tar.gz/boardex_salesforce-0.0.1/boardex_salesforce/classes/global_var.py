"""
Copyright 2020 BoardEx

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# ----------------------------------------------------------------------------------------------------------------------
# library import
# ----------------------------------------------------------------------------------------------------------------------

from datetime import date                                   # current date
from datetime import datetime
import time
import os, shutil                                           # Manipulates OS folder
import pprint                                               # Displays output more clearly
from boardex_salesforce.config import username, password, security_token, myHostname, myPassword, myUsername, path_local_temp, log_level, company_query, contact_query, UserDetails_query, upload_to_sftp, query_email, ContactDetails_query
from datetime import date                                   # current date
import pysftp                                               # sftp connection
from tqdm import tqdm                                       # progress bar
import pandas as pd
import csv
from simple_salesforce import Salesforce
import random, string
import logging                                              # "logs log"
import shutil




# ----------------------------------------------------------------------------------------------------------------------
# current date
# ----------------------------------------------------------------------------------------------------------------------

currentDate = str(datetime.today().strftime('%Y%m%d')) # creates current date (yyyymmdd) for csv file name


# ----------------------------------------------------------------------------------------------------------------------
# Local path
# ----------------------------------------------------------------------------------------------------------------------
local_split_folder = 'split_csv_files'
path_local_split_csv_files = local_split_folder
moved_combined_company_cvs_filepath = path_local_split_csv_files +'\\'+currentDate+"_company_combined_csv.csv"
moved_combined_contact_cvs_filepath = path_local_split_csv_files+'\\'+currentDate+"_contact_combined_csv.csv"

combined_company_cvs_filepath = currentDate+"_company_combined_csv.csv"
combined_contact_cvs_filepath = currentDate+"_contact_combined_csv.csv"


# ----------------------------------------------------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------------------------------------------------
create_folder_mode = 777
counter = 0                                 # counts the number files to be uploaded to BoardEx sftp server
array_remote_contact_csv_files = []
array_remote_company_csv_files = []

# ----------------------------------------------------------------------------------------------------------------------
# Name for local folder
# ----------------------------------------------------------------------------------------------------------------------
folder_archive_name = 'archive'                 # folder's name for archive on server
folder_log_name = 'log'                         # folder's name for log on server
folder_upload_name = 'upload'
folder_download_name = 'download'

# ----------------------------------------------------------------------------------------------------------------------
# BoardEx sftp path
# ----------------------------------------------------------------------------------------------------------------------
path_remote_log = 'log'                        # remote temporary path for logs
path_remote_archive = 'archive'                  # path for archive folder

# ----------------------------------------------------------------------------------------------------------------------
# save as locally
# ----------------------------------------------------------------------------------------------------------------------
randomAlphaNumeric = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # creates 6 random characters

boardex_log ='_BoardEx_sftp.log'
fileExtention = '.csv'

save_BoardExFile_contact = '_Contacts_IN'
save_BoardExFileType_company = '_Company_IN'
save_BoardExFileType_ContactDetails = '_ContactDetails_I_PRD'
save_BoardExFileType_UserDetails = '_UserDetails_I_PRD'


split_company_output_filename = 'company_split_%s.csv'
split_contact_output_filename = 'Contacts_split_%s.csv'

save_company_as = currentDate + save_BoardExFileType_company + fileExtention
save_company_to = path_local_temp  + folder_download_name +'//'+save_company_as

save_contact_as = currentDate + save_BoardExFile_contact + fileExtention
save_contact_to = path_local_temp  +folder_download_name +'//'+ save_contact_as

save_ContactDetails_as = currentDate + save_BoardExFileType_ContactDetails + fileExtention
save_ContactDetails_to = path_local_temp +folder_download_name +'//'+ save_ContactDetails_as

save_UserDetails_as = currentDate + save_BoardExFileType_UserDetails + fileExtention
save_UserDetails_to = path_local_temp + folder_download_name +'//'+save_UserDetails_as

# ----------------------------------------------------------------------------------------------------------------------
# save as on sftp
# ----------------------------------------------------------------------------------------------------------------------

remote_path_company = '\\'+ save_company_as
remote_path_contact = '\\'+ save_contact_as
remote_path_ContactDetails = '\\'+ save_ContactDetails_as
remote_path_UserDetails = '\\'+ save_UserDetails_as


# ----------------------------------------------------------------------------------------------------------------------
# search file name containing a string
# ----------------------------------------------------------------------------------------------------------------------
search_company ='Company'
search_contact = 'Contacts'
search_logs = ".log"
search_split_contact = 'Contacts_split'
search_split_company = 'company_split'
search_split_csv = 'split'
search_out = 'OUT'

# ----------------------------------------------------------------------------------------------------------------------
# CSV encorder
# ----------------------------------------------------------------------------------------------------------------------
encoder = 'utf-8-sig'
# ----------------------------------------------------------------------------------------------------------------------
# CSV delimiter
# ----------------------------------------------------------------------------------------------------------------------
delimiter = '|'
# ----------------------------------------------------------------------------------------------------------------------
# CSV row limit
# ----------------------------------------------------------------------------------------------------------------------
row_limit1= 10000

# ----------------------------------------------------------------------------------------------------------------------
# initialise array variable.
# ----------------------------------------------------------------------------------------------------------------------
array_company = []                              # list of company csv files
array_contact = []                              # list of contact csv files
array_csv_only = []                             # list of all csv files
array_company_for_upload = []                   # list of company's data. Data of one csv file into an array.
array_contact_for_upload = []                   # list of contacts's data. Data of one csv file into an array.

# ----------------------------------------------------------------------------------------------------------------------
# variable for today's date for logs ONLY
# ----------------------------------------------------------------------------------------------------------------------
today = date.today()                            # today's date
dateformat = "%Y-%b-%d"
# ----------------------------------------------------------------------------------------------------------------------
#  creates a local temp folder
# ----------------------------------------------------------------------------------------------------------------------
if path_local_temp:
    #path_local_temp is empty
    try:
        if not os.path.exists(path_local_temp):
            #create directory
            os.makedirs(path_local_temp)
    except Exception as e:
        raise e

# ----------------------------------------------------------------------------------------------------------------------
#  Create log file
# ----------------------------------------------------------------------------------------------------------------------

if log_level == 'NOTSET':
    set_log_level = 0 # NOTSET
elif  log_level == 'DEBUG':
    set_log_level = 10 # Debug
elif log_level == 'INFO':
    set_log_level = 20  # INFO
elif  log_level == 'WARNING':
    set_log_level = 30 # WARNING
elif log_level == 'ERROR':
    set_log_level = 40  # ERROR
elif  log_level == 'CRITICAL':
    set_log_level = 50 # CRITICAL
else:
    set_log_level = 50  # CRITICAL


#def getlog(set_log_level)
logger = logging.getLogger(__name__)
logger.setLevel(set_log_level)

date_formatted = today.strftime(dateformat)
# create a file handler
log_filename = str(path_local_temp) + '\\' + str(date_formatted) + str(boardex_log)

try:
    if path_local_temp:
        # path_local_temp is empty
        handler = logging.FileHandler(log_filename)
    else:
        log_filename = str(date_formatted) + str(boardex_log)
        handler = logging.FileHandler(log_filename)
except Exception as e:
        raise e

handler.setLevel(set_log_level)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the file handler to the logger
logger.addHandler(handler)
