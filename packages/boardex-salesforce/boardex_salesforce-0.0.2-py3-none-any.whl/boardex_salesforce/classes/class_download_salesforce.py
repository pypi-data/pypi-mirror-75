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

from . import global_var # import all the varaibles and libraries


if global_var.upload_to_sftp:
     from . import class_bx_sftp as bx_sftp  # import class_bx_sftp only if upload_to_sftp == True in config.py

# ----------------------------------------------------------------------------------------------------------------------
#  SalesForce connection
# ----------------------------------------------------------------------------------------------------------------------
class salesforce_connection:
    # ----------------------------------------------------------------------------------------------------------------------
    #  create  salesforce connection
    # ----------------------------------------------------------------------------------------------------------------------
    def sf_connection(self):
        try:
            global_var.logger.info('##################------salesForce_connection()------#################')
            sfa = global_var.Salesforce(username=global_var.username, password=global_var.password,
                                        security_token=global_var.security_token)
            global_var.logger.info(str(global_var.username) + ' is connected to SalesForce')
            return sfa
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            if ('REQUEST_LIMIT_EXCEEDED' in str(e)):
                global_var.logger.error('REQUEST_LIMIT_EXCEEDED')
            else:
                global_var.logger.critical('Error: connection failed; please check username, password, security_token')
# ----------------------------------------------------------------------------------------------------------------------
#  makes sql queries to salesforce for companies and contacts
# ----------------------------------------------------------------------------------------------------------------------
class download_salesforce:
    # ----------------------------------------------------------------------------------------------------------------------
    #  sql query to salesforce - gets companies information
    # ----------------------------------------------------------------------------------------------------------------------
    def query_all_COMPANY_info(self, needSalesForceConnection):
        try:
            global_var.logger.info('Querying company details from SF')
            global_var.logger.debug('using the query: ' + str(global_var.company_query))

            accountsInfo = needSalesForceConnection.bulk.Account.query(global_var.company_query)
            global_var.logger.info(str(len(accountsInfo)) + ' records found FROM Account')

            return accountsInfo
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error(
                'Error: cannot query data from salesforce. Please check Credendtials or contact_query in the config.py file')
            raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  sql query to salesforce - gets contacts information
    # ----------------------------------------------------------------------------------------------------------------------
    def query_all_Contact_info(self, needSalesForceConnection):
        try:
            global_var.logger.info('Querying Contact from SF')
            if global_var.query_email == False:
                global_var.contact_query = "SELECT ID, FirstName, LastName, BoardEx__Client_Individual_ID__c, Title, Account.Name FROM Contact WHERE BoardEx__Client_Individual_ID__c !=''"
            else:
                global_var.contact_query

            global_var.logger.debug('using the query: ' + str(global_var.contact_query))

            accountsInfo = needSalesForceConnection.bulk.Contact.query(global_var.contact_query)

            global_var.logger.info(str(len(accountsInfo)) + ' records found FROM Contact')
            return accountsInfo
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error(
                'Error: cannot query data from salesforce. Please check Credendtials or contact_query in the config.py file')
            raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  sql query to salesforce - gets user details
    # ----------------------------------------------------------------------------------------------------------------------
    def query_all_UserDetails_info(self, needSalesForceConnection):
        try:
            global_var.logger.info('Querying User details from SF')
            global_var.logger.debug('using the query: ' + str(global_var.UserDetails_query))

            accountsInfo = needSalesForceConnection.bulk.Contact.query(global_var.UserDetails_query)

            global_var.logger.info(str(len(accountsInfo)) + ' records found FROM Contact')
            return accountsInfo
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error(
                'Error: cannot query data from salesforce. Please check Credendtials or UserDetails_query in the config.py file')
            raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  sql query to salesforce - gets contacts details
    # ----------------------------------------------------------------------------------------------------------------------
    def query_all_ContactDetails_info(self, needSalesForceConnection):
        try:
            global_var.logger.info('Querying User details from SF')
            global_var.logger.debug('using the query: ' + str(global_var.ContactDetails_query))

            accountsInfo = needSalesForceConnection.bulk.Contact.query(global_var.ContactDetails_query)

            global_var.logger.info(str(len(accountsInfo)) + ' records found FROM Contact')
            return accountsInfo
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error(
                'Error: cannot query data from salesforce. Please check Credendtials or ContactDetails_query in the config.py file')
            raise e
# ----------------------------------------------------------------------------------------------------------------------
#  Creates a table, adds BoardEx headers to the company and contact csv file
# ----------------------------------------------------------------------------------------------------------------------
class add_bx_headers:
    # ----------------------------------------------------------------------------------------------------------------------
    #  Compant table: The following headers will be added - Company, ClientCompanyID, ClientCountry,CompanyID
    # ----------------------------------------------------------------------------------------------------------------------
    def query_Company_into_dict(self, get_all_records):
        try:
            newList = []
            # Place query data into a data frame
            df = global_var.pd.DataFrame(get_all_records)
            global_var.logger.debug('Placing the company data from Salesforce in a table')
            df = df.loc[:, ['Name', 'Id', 'BillingCountry', 'BoardEx__Client_Organization_ID__c']]
            # Rename the extracted columns
            df.rename(columns={'Name': 'Company'}, inplace=True)
            df.rename(columns={'Id': 'ClientCompanyID'}, inplace=True)
            df.rename(columns={'BillingCountry': 'ClientCountry'}, inplace=True)
            df.rename(columns={'BoardEx__Client_Organization_ID__c': 'CompanyID'}, inplace=True)

            cols = list(df.columns.values)
            global_var.logger.debug('Creating the following Columns: ' + str(cols))
            # putting the data in an array
            arrayDF = df.to_numpy()
            global_var.logger.debug('Lenght of the array: ' + str(len(arrayDF)))
            global_var.logger.debug('Inserting the data from the array into a list')

            for item in global_var.tqdm(arrayDF):
                Company = str(item[0])
                ClientCompanyID = str(item[1])
                ClientCountry = str(item[2])
                CompanyID = str(item[3])

                newList.append(
                    {'Company': Company, 'ClientCompanyID': ClientCompanyID, 'ClientCountry': ClientCountry,
                     'CompanyID': CompanyID})

            global_var.logger.debug(str(len(newList)) + ' Compamies have been converted into BoardEx standard')
            return newList
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  add the following headers - Forename1, Forename2, Forename3, UsualName, Surname, IBSID, Role, Organisation, BoardExID
    # ----------------------------------------------------------------------------------------------------------------------
    def query_Contacts_into_dict(self, get_all_records):
                try:
                    newList = []
                    # Place query data into a data frame
                    df = global_var.pd.DataFrame(get_all_records)
                    global_var.logger.debug('Placing the Contact data from Salesforce in a table')
                    if global_var.query_email == False:
                        df = df.loc[:,
                         ['FirstName', 'LastName',  'Title', 'Account', 'Id', 'BoardEx__Client_Individual_ID__c']]
                    else:
                        df = df.loc[:,
                         ['FirstName', 'LastName', 'Email', 'Title', 'Account', 'Id', 'BoardEx__Client_Individual_ID__c']]
                    # Rename the columns
                    df.rename(columns={'FirstName': 'Forename1'}, inplace=True)
                    df.rename(columns={'LastName': 'Surname'}, inplace=True)
                    df.rename(columns={'Id': 'IBSID'}, inplace=True)
                    df.rename(columns={'Title': 'Role'}, inplace=True)
                    df.rename(columns={'BoardEx__Client_Individual_ID__c': 'BoardExID'}, inplace=True)
                    df.rename(columns={'Account': 'Organisation'}, inplace=True)

                    # Adds empty columns in specific location
                    df.insert(1, 'Forename2', '', allow_duplicates=False)
                    df.insert(2, 'Forename3', '', allow_duplicates=False)
                    df.insert(3, 'UsualName', '', allow_duplicates=False)

                    cols = list(df.columns.values)
                    global_var.logger.debug('Creating the following Columns: ' + str(cols))

                    # putting the data in an array
                    arrayDF = df.to_numpy()
                    global_var.logger.debug('Lenght of the array: ' + str(len(arrayDF)))
                    global_var.logger.debug('Inserting the data from the array into a list')

                    for item in global_var.tqdm(arrayDF):
                        Forename1 = str(item[0])
                        Forename2 = str(item[1])
                        Forename3 = str(item[2])
                        UsualName = str(item[3])
                        Surname = str(item[4])

                        if global_var.query_email == False:
                            Role = str(item[5])
                            Organisation = str(item[6]['Name'])
                            IBSID = str(item[7])
                            BoardExID = str(item[8])

                            newList.append(
                                {'Forename1': Forename1, 'Forename2': Forename2, 'Forename3': Forename3, 'UsualName': UsualName,
                                 'Surname': Surname, 'Role': Role, 'Organisation': Organisation, 'IBSID': IBSID,
                                 'BoardExID': BoardExID})
                        else:
                            Email = str(item[5])
                            Role = str(item[6])
                            Organisation = str(item[7]['Name'])
                            IBSID = str(item[8])
                            BoardExID = str(item[9])

                            newList.append(
                                {'Forename1': Forename1, 'Forename2': Forename2, 'Forename3': Forename3, 'UsualName': UsualName,
                                 'Surname': Surname, 'Email': Email, 'Role': Role, 'Organisation': Organisation, 'IBSID': IBSID,
                                 'BoardExID': BoardExID})


                    global_var.logger.debug(str(len(newList)) + ' Contacts have been converted into BoardEx standard')

                    return newList

                except Exception as e:
                    global_var.logger.error(e, exc_info=True)
                    raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  add the following headers - UserGUID, FirstName, Surname, Email, Department, Role, Region, NetworkBandID, Disabled
    # ----------------------------------------------------------------------------------------------------------------------
    def query_UserDetails_into_dict(self, get_all_records):
                try:
                    newList = []
                    # Place query data into a data frame
                    df = global_var.pd.DataFrame(get_all_records)
                    global_var.logger.debug('Placing the UserDetails data from Salesforce in a table')
                    df = df.loc[:,
                         ['FirstName', 'LastName', 'Email', 'Title']]

                    # Rename the extracted columns
                    df.rename(columns={'FirstName': 'FirstName'}, inplace=True)
                    df.rename(columns={'LastName': 'Surname'}, inplace=True)
                    df.rename(columns={'Email': 'Email'}, inplace=True)
                    df.rename(columns={'Title': 'Role'}, inplace=True)

                    # Adds empty columns in specific location
                    df.insert(0, 'UserGUID', '', allow_duplicates=False)
                    df.insert(4, 'Department', '', allow_duplicates=False)
                    df.insert(6, 'Region', '', allow_duplicates=False)
                    df.insert(7, 'NetworkBandID', '300', allow_duplicates=False)
                    df.insert(8, 'Disabled', '0', allow_duplicates=False)

                    cols = list(df.columns.values)
                    global_var.logger.debug('Creating the following Columns: ' + str(cols))

                    # putting the data in an array
                    arrayDF = df.to_numpy()
                    global_var.logger.debug('Lenght of the array: ' + str(len(arrayDF)))
                    global_var.logger.debug('Inserting the data from the array into a list')

                    for item in global_var.tqdm(arrayDF):
                        UserGUID = str(item[3])
                        FirstName = str(item[1])
                        Surname = str(item[2])
                        Email = str(item[3])
                        Department = str(item[4])
                        Role = str(item[5])
                        Region = str(item[6])
                        NetworkBandID = str(item[7])
                        Disabled = str(item[8])

                        newList.append(
                            {'UserGUID': UserGUID, 'FirstName': FirstName, 'Surname': Surname, 'Email': Email,
                             'Department': Department, 'Role': Role, 'Region': Region, 'NetworkBandID': NetworkBandID, 'Disabled': Disabled})

                    global_var.logger.debug(str(len(newList)) + ' UserDetails have been converted into BoardEx standard')

                    return newList

                except Exception as e:
                    global_var.logger.error(e, exc_info=True)
                    raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  add the following headers - UserGUID, FirstName, Surname, Email, Department, Role, Region, NetworkBandID, Disabled
    # ----------------------------------------------------------------------------------------------------------------------
    def query_ContactDetails_into_dict(self, get_all_records):
                try:
                    newList = []
                    userguid_entityid_only = [[]]
                    try:
                        get_totalSize = len(get_all_records)
                        for r in global_var.tqdm(range(0, get_totalSize)):
                            a = get_all_records[r]['Owner']['Email']
                            b = get_all_records[r]['BoardEx__Client_Individual_ID__c']
                            c = a, b
                            userguid_entityid_only.append(c)
                            # rename the columns
                            df = global_var.pd.DataFrame(userguid_entityid_only, columns=['UserGUID', 'EntityID'])
                    except Exception as e:
                        global_var.logger.error(e, exc_info=True)

                    # Place query data into a data frame
                    df = global_var.pd.DataFrame(df)

                    # Removes the first row which contains None for 'UserGUID', 'EntityID'
                    df = df.stack().str.replace('None', ' ').unstack()
                    global_var.logger.debug('Placing the ContactDetails data from Salesforce in a table')
                    df = df.loc[:,
                         ['UserGUID', 'EntityID']]

                    # Adds empty columns in specific location
                    df.insert(2, 'Weighting', '5', allow_duplicates=False)
                    df.insert(3, 'Personal', '', allow_duplicates=False)
                    df.insert(4, 'VisibilityID', '', allow_duplicates=False)
                    df.insert(5, 'PermissionID', '', allow_duplicates=False)
                    df.insert(6, 'Deleted', '', allow_duplicates=False)

                    cols = list(df.columns.values)
                    global_var.logger.debug('Creating the following Columns: ' + str(cols))

                    # putting the data in an array
                    arrayDF = df.to_numpy()
                    global_var.logger.debug('Lenght of the array: ' + str(len(arrayDF)))
                    global_var.logger.debug('Inserting the data from the array into a list')

                    for item in global_var.tqdm(arrayDF):
                        UserGUID = str(item[0])
                        EntityID = str(item[1])
                        Weighting = str(item[2])
                        Personal = str(item[3])
                        VisibilityID = str(item[4])
                        PermissionID = str(item[5])
                        Deleted = str(item[6])

                        newList.append(
                            {'UserGUID': UserGUID, 'EntityID': EntityID, 'Weighting': Weighting, 'Personal': Personal,
                             'VisibilityID': VisibilityID, 'PermissionID': PermissionID, 'Deleted': Deleted})

                    global_var.logger.debug(str(len(newList)) + ' ContactDetails have been converted into BoardEx standard')

                    return newList

                except Exception as e:
                    global_var.logger.error(e, exc_info=True)
                    raise e
# ----------------------------------------------------------------------------------------------------------------------
#  removes unauthorised characters
# ----------------------------------------------------------------------------------------------------------------------
class clean_data:
    def remove_unauthorised_characters(self,data_array):
        try:
            global_var.logger.debug('Converts array into a table')

            df = global_var.pd.DataFrame(data_array)

            global_var.logger.debug('Removes unauthorised characters ')

            # cleans data according to BoardEx Template
            df = df.stack().str.replace(',', ' ').unstack()
            df = df.stack().str.replace("'", ' ').unstack()
            df = df.stack().str.replace('|', ' ').unstack()
            df = df.stack().str.replace('(', ' ').unstack()
            df = df.stack().str.replace(')', ' ').unstack()
            df = df.stack().str.replace('\\', ' ').unstack()
            df = df.stack().str.replace('/', ' ').unstack()
            df = df.stack().str.replace('"', ' ').unstack()
            df = df.stack().str.replace('   ', ' ').unstack()
            df = df.stack().str.replace('None', ' ').unstack()
            return df
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e
# ----------------------------------------------------------------------------------------------------------------------
#  export to csv file
# ----------------------------------------------------------------------------------------------------------------------
class export_to:
    # ----------------------------------------------------------------------------------------------------------------------
    #  export company csv file
    # ----------------------------------------------------------------------------------------------------------------------
    def company_csv(self,cleaned_company_data):

        # re-orders the columns hearders and their data.
        df = cleaned_company_data[['Company', 'ClientCompanyID', 'ClientCountry', 'CompanyID']]

        global_var.logger.debug('Saving file as: ' + str(global_var.save_company_as))
        global_var.logger.debug('Saving file to: ' + str(global_var.save_company_to))

        try:
            global_var.logger.info('Saving company csv as: ' + str(global_var.save_company_to))

            # Exports and encodes the file as a CSV file with a pipe delimiter
            df.to_csv(global_var.save_company_to, sep=global_var.delimiter, encoding=global_var.encoder, index=False)

            global_var.logger.info('Company csv saved to: ' + str(global_var.save_company_to))
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Error saving Company data to csv')
            raise e

        # ----------------------------------------------------------------------------------------------------------------------
        #  uploads to csv to sftp
        # ----------------------------------------------------------------------------------------------------------------------
        if global_var.upload_to_sftp == True:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))
            try:
                export_to().BoardEx_sftp(global_var.save_company_to, global_var.remote_path_company)
            except Exception as e:
                global_var.logger.error(e, exc_info=True)
                raise e
        else:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))

    # ----------------------------------------------------------------------------------------------------------------------
    #  export contact csv file
    # ----------------------------------------------------------------------------------------------------------------------
    def contact_csv(self,cleaned_contact_data):
        # re-orders the columns hearders and their data.
        if global_var.query_email == False:
            df = cleaned_contact_data[['Forename1', 'Forename2', 'Forename3', 'UsualName', 'Surname', 'Role', 'Organisation', 'IBSID','BoardExID']]

        else:
            df = cleaned_contact_data[['Forename1', 'Forename2', 'Forename3', 'UsualName', 'Surname', 'Email', 'Role', 'Organisation', 'IBSID','BoardExID']]

        global_var.logger.debug('Saving file as: ' + str(global_var.save_contact_as))
        global_var.logger.debug('Saving file to: ' + str(global_var.save_contact_to))

        try:
            global_var.logger.info('Saving contact csv as: ' + str(global_var.save_contact_to))

            # Exports and encodes the file as a CSV file with a pipe delimiter
            df.to_csv(global_var.save_contact_to, sep=global_var.delimiter, encoding=global_var.encoder, index=False)
            global_var.logger.info('contact csv saved to: ' + str(global_var.save_contact_to))

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Error saving Company data to csv')
            raise e

        # ----------------------------------------------------------------------------------------------------------------------
        #  uploads to csv to sftp
        # ----------------------------------------------------------------------------------------------------------------------
        if global_var.upload_to_sftp == True:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))
            try:
                export_to().BoardEx_sftp(global_var.save_contact_to, global_var.remote_path_contact)
            except Exception as e:
                global_var.logger.error(e, exc_info=True)
                raise e
        else:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))

    # ----------------------------------------------------------------------------------------------------------------------
    #  export UserDetails csv file
    # ----------------------------------------------------------------------------------------------------------------------
    def UserDetails_csv(self,cleaned_contact_data):

        # re-orders the columns hearders and their data.
        df = cleaned_contact_data[
                ['UserGUID', 'FirstName', 'Surname', 'Email', 'Department', 'Role', 'Region', 'NetworkBandID',
                 'Disabled']]

        global_var.logger.debug('Saving file as: ' + str(global_var.save_UserDetails_as))
        global_var.logger.debug('Saving file to: ' + str(global_var.save_UserDetails_to))

        try:
            global_var.logger.info('Saving contact csv as: ' + str(global_var.save_UserDetails_to))

            # Exports and encodes the file as a CSV file with a pipe delimiter
            df.to_csv(global_var.save_UserDetails_to, sep=global_var.delimiter, encoding=global_var.encoder, index=False)

            global_var.logger.info('contact csv saved to: ' + str(global_var.save_UserDetails_to))

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Error saving Company data to csv')
            raise e

        # ----------------------------------------------------------------------------------------------------------------------
        #  uploads to csv to sftp
        # ----------------------------------------------------------------------------------------------------------------------
        if global_var.upload_to_sftp == True:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))
            try:
                export_to().BoardEx_sftp(global_var.save_UserDetails_to, global_var.remote_path_UserDetails)
            except Exception as e:
                global_var.logger.error(e, exc_info=True)
                raise e
        else:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))

    # ----------------------------------------------------------------------------------------------------------------------
    #  export ContactDetails csv file
    # ----------------------------------------------------------------------------------------------------------------------
    def ContactDetails_csv(self,cleaned_contact_data):
        # re-orders the columns hearders and their data.
        df = cleaned_contact_data[
                ['UserGUID', 'EntityID', 'Weighting', 'Personal', 'VisibilityID', 'PermissionID', 'Deleted']]

        global_var.logger.debug('Saving file as: ' + str(global_var.save_ContactDetails_as))
        global_var.logger.debug('Saving file to: ' + str(global_var.save_ContactDetails_to))

        try:
            global_var.logger.info('Saving contact csv as: ' + str(global_var.save_ContactDetails_to))

            # Exports and encodes the file as a CSV file with a pipe delimiter
            df.to_csv(global_var.save_ContactDetails_to, sep=global_var.delimiter, encoding=global_var.encoder, index=False)

            global_var.logger.info('contact csv saved to: ' + str(global_var.save_ContactDetails_to))

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Error saving Company data to csv')
            raise e

        # ----------------------------------------------------------------------------------------------------------------------
        #  uploads to csv to sftp
        # ----------------------------------------------------------------------------------------------------------------------
        if global_var.upload_to_sftp == True:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))
            try:
                export_to().BoardEx_sftp(global_var.save_ContactDetails_to, global_var.remote_path_ContactDetails)
            except Exception as e:
                global_var.logger.error(e, exc_info=True)
                raise e
        else:
            global_var.logger.info("upload_to_sftp: " + str(global_var.upload_to_sftp))

    # ----------------------------------------------------------------------------------------------------------------------
    #  connects to sftp server, creates the required folder and uploads csv file
    # ----------------------------------------------------------------------------------------------------------------------
    def BoardEx_sftp(self,local_csv, remote_csv):
        # ----------------------------------------------------------------------------------------------------------------------
        #  sftp connection to BoardEx from class_bx_sftp
        # ----------------------------------------------------------------------------------------------------------------------
            sftp_conn = bx_sftp.bx_sftp().bx_sftp_connection()
        # ----------------------------------------------------------------------------------------------------------------------
        #  creates a log folder on sftp server
        # ----------------------------------------------------------------------------------------------------------------------
            bx_sftp.create_folder().create_remote_log_folder(sftp_conn)
            global_var.logger.debug("Remote log folder created")
        # ----------------------------------------------------------------------------------------------------------------------
        #  creates an archive folder on sftp server
        # ----------------------------------------------------------------------------------------------------------------------
            bx_sftp.create_folder().create_remote_archive_folder(sftp_conn)
            global_var.logger.debug("Remote archive folder created")
        # ----------------------------------------------------------------------------------------------------------------------
        #  uploads csv file
        # ----------------------------------------------------------------------------------------------------------------------
            try:
                global_var.logger.debug("Uploading csv to sftp")
                filePath = sftp_conn.put(local_csv, remote_csv)
                global_var.logger.debug('File uploaded to: ' + str(remote_csv))
                global_var.logger.debug("Upload to sftp complete")

            except Exception as e:
                global_var.logger.error(e, exc_info=True)
                raise e

        # ----------------------------------------------------------------------------------------------------------------------
        #  uploads csv file
        # ----------------------------------------------------------------------------------------------------------------------

            global_var.logger.debug("Uploading logs")
            bx_sftp.upload_logs_to_sftp().upload_log(sftp_conn)
            global_var.logger.debug("Upload complete")

