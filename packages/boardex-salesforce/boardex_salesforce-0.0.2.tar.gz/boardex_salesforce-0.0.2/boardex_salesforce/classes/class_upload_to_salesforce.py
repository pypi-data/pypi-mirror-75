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
#  update BoardExID to salesforce
# ----------------------------------------------------------------------------------------------------------------------
class upload_to_salesfore:
    # ----------------------------------------------------------------------------------------------------------------------
    #  update contact to salesforce
    # ----------------------------------------------------------------------------------------------------------------------
    def update_contacts_to_sf(self, salesforce_connection, path_split_contact):

        global_var.logger.debug('update_contact_to_salesforce')
        global_var.logger.info('Please wait updating contacts to salesforce')

        bx_out_notnull = global_var.pd.read_csv(path_split_contact, encoding=global_var.encoder, sep = global_var.delimiter)
        df2 = global_var.pd.DataFrame(bx_out_notnull)

        total_rows = len(df2)
        counter = 0

        Bulk_data = []

        for i in (range(0,len(df2))):
            BoardExID = df2['BoardExID'].values[i]
            IBSID = df2['IBSID'].values[i]

            if  str(BoardExID) == 'nan' or str(BoardExID).strip() == '':
                global_var.logger.debug('ERROR: no BXid for ' + str(IBSID))
            else:
                data = {'Id': IBSID, 'BoardEx__Client_Individual_ID__c': BoardExID}
                Bulk_data.append(data)
        try:
            global_var.logger.info('Updating contacts to salesforce')
            t = salesforce_connection.bulk.Contact.upsert(Bulk_data, 'Id')
            global_var.logger.info('Update complete')


        except Exception as e:
                    global_var.logger.error(e, exc_info=True)
                    global_var.logger.debug('ERROR: Boardex ID not updated for  ' + IBSID )
                    raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  update company to salesforce
    # ----------------------------------------------------------------------------------------------------------------------
    def update_company_to_sf(self, salesforce_connection, path_split_contact):

        global_var.logger.debug('update_company_to_sf')
        global_var.logger.info('Please wait updating company salesforce')

        bx_out_notnull = global_var.pd.read_csv(path_split_contact, encoding=global_var.encoder, sep = global_var.delimiter)
        df2 = global_var.pd.DataFrame(bx_out_notnull)

        total_rows = len(df2)
        counter = 0

        Bulk_data = []


        for i in (range(0,len(df2))):
            CompanyID = str(df2['CompanyID'].values[i])
            ClientCompanyID = str(df2['ClientCompanyID'].values[i])

            if  str(CompanyID) == 'nan' or str(CompanyID).strip() == '' :
                global_var.logger.debug('ERROR: no BXid for ' + ClientCompanyID)
            else:
                data = {'Id': ClientCompanyID, 'BoardEx__Client_Organization_ID__c': CompanyID}

                Bulk_data.append(data)
        try:
            global_var.logger.info('Updating Company to salesforce')
            t = salesforce_connection.bulk.Account.upsert(Bulk_data, 'Id')
            global_var.logger.info('Update complete')

        except Exception as e:
                    global_var.logger.error(e, exc_info=True)
                    global_var.logger.debug('ERROR: Boardex ID not updated for  ' + ClientCompanyID )
                    raise e
# ----------------------------------------------------------------------------------------------------------------------
#  Download all csv OUT file if upload_to_sftp == True
# ----------------------------------------------------------------------------------------------------------------------
class download_from_sftp:
    ### The main methods are called from classes.class_bx_sftp.py
    def download_all_csv(self):
        if global_var.upload_to_sftp == True:
            # ----------------------------------------------------------------------------------------------------------------------
            #  sftp connection to BoardEx
            # ----------------------------------------------------------------------------------------------------------------------
            sftp_conn = bx_sftp.bx_sftp().bx_sftp_connection()
            # ----------------------------------------------------------------------------------------------------------------------
            #  Get all csv files on BoardEx sftp server
            # ----------------------------------------------------------------------------------------------------------------------
            all_remote_csv = bx_sftp.bx_sftp().get_all_csv(sftp_conn)

            if len(all_remote_csv) !=0 :
                # ----------------------------------------------------------------------------------------------------------------------
                #  download all csv files on BoardEx sftp server
                # ----------------------------------------------------------------------------------------------------------------------
                bx_sftp.bx_sftp().download_all_csv_from_bx(sftp_conn, all_remote_csv)
                # ----------------------------------------------------------------------------------------------------------------------
                #   create archive folder on BoardEx sftp server
                # ----------------------------------------------------------------------------------------------------------------------
                bx_sftp.create_folder().create_remote_archive_folder(sftp_conn)
                # ----------------------------------------------------------------------------------------------------------------------
                #   move files to archive folder on sftp server
                # ----------------------------------------------------------------------------------------------------------------------
                bx_sftp.move_files().move_files_to_archive(sftp_conn,all_remote_csv)
            else:
                global_var.logger.info('No csv OUT file found sftp server')
        else:
            global_var.logger.debug('upload_to_sftp : ' + str(global_var.upload_to_sftp))
