from .classes import class_download_salesforce as SalesForce
from .classes.global_var import logger
from .classes.class_bx_sftp import local_dir

def download_ContactDetails_from_sf():

    # ----------------------------------------------------------------------------------------------------------------------
    #  salesforce connection
    # ----------------------------------------------------------------------------------------------------------------------
    salesForceConnection = SalesForce.salesforce_connection().sf_connection()
    # ----------------------------------------------------------------------------------------------------------------------
    #  Create local folders
    # ----------------------------------------------------------------------------------------------------------------------
    local_dir().create_download_folder()
    # ----------------------------------------------------------------------------------------------------------------------
    #  Queries ContactDetails data from Salesforce
    # ----------------------------------------------------------------------------------------------------------------------
    ContactDetails_query_data = SalesForce.download_salesforce().query_all_ContactDetails_info(salesForceConnection)

    if len(ContactDetails_query_data) != 0 :

        # ----------------------------------------------------------------------------------------------------------------------
        #  organise data to BoardEx standards and place into a dictionary
        # ----------------------------------------------------------------------------------------------------------------------
        ContactDetails_data_array = SalesForce.add_bx_headers().query_ContactDetails_into_dict(ContactDetails_query_data)

        # ----------------------------------------------------------------------------------------------------------------------
        #  removes unauthorised characters
        # ----------------------------------------------------------------------------------------------------------------------
        cleaned_data = SalesForce.clean_data().remove_unauthorised_characters(ContactDetails_data_array)

        # ----------------------------------------------------------------------------------------------------------------------
        #  save ContactDetails file to CSV
        # ----------------------------------------------------------------------------------------------------------------------

        export_to_csv = SalesForce.export_to().ContactDetails_csv(cleaned_data)

    else:
        logger.info(('No records found without a BoardExID'))

if __name__ == '__main__':
    download_ContactDetails_from_sf()