from .classes import class_download_salesforce as SalesForce
from .classes.global_var import logger
from .classes.class_bx_sftp import local_dir

def download_contact_from_sf():

    # ----------------------------------------------------------------------------------------------------------------------
    #  salesforce connection
    # ----------------------------------------------------------------------------------------------------------------------
    salesForceConnection = SalesForce.salesforce_connection().sf_connection()

    # ----------------------------------------------------------------------------------------------------------------------
    #  Create local folders
    # ----------------------------------------------------------------------------------------------------------------------
    local_dir().create_download_folder()

    # ----------------------------------------------------------------------------------------------------------------------
    #  Queries Contact data from Salesforce
    # ----------------------------------------------------------------------------------------------------------------------

    contact_query_data = SalesForce.download_salesforce().query_all_Contact_info(salesForceConnection)

    if len(contact_query_data) != 0 :

        # ----------------------------------------------------------------------------------------------------------------------
        #  organise data to BoardEx standards and place into a dictionary
        # ----------------------------------------------------------------------------------------------------------------------
        contact_data_array = SalesForce.add_bx_headers().query_Contacts_into_dict(contact_query_data)

        # ----------------------------------------------------------------------------------------------------------------------
        #  removes unauthorised characters
        # ----------------------------------------------------------------------------------------------------------------------
        cleaned_data = SalesForce.clean_data().remove_unauthorised_characters(contact_data_array)

        # ----------------------------------------------------------------------------------------------------------------------
        #  save company file to CSV
        # ----------------------------------------------------------------------------------------------------------------------

        export_to_csv = SalesForce.export_to().contact_csv(cleaned_data)
    else:
        logger.info('No records found without a BoardExID')

if __name__ == '__main__':
    download_contact_from_sf()