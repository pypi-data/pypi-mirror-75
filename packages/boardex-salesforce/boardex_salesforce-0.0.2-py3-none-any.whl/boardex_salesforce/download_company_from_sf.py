from .classes import class_download_salesforce as SalesForce
from .classes.global_var import logger
from .classes.class_bx_sftp import local_dir

def download_company_from_sf():

    # ----------------------------------------------------------------------------------------------------------------------
    #  salesforce connection
    # ----------------------------------------------------------------------------------------------------------------------
    salesForceConnection = SalesForce.salesforce_connection().sf_connection()

    # ----------------------------------------------------------------------------------------------------------------------
    #  Create local folders
    # ----------------------------------------------------------------------------------------------------------------------
    local_dir().create_download_folder()

    # ----------------------------------------------------------------------------------------------------------------------
    #  Queries Company data from Salesforce
    # ----------------------------------------------------------------------------------------------------------------------
    company_query_data = SalesForce.download_salesforce().query_all_COMPANY_info(salesForceConnection)

    if len(company_query_data) != 0 :

        # ----------------------------------------------------------------------------------------------------------------------
        #  organise data to BoardEx standards and place into a dictionary
        # ----------------------------------------------------------------------------------------------------------------------
        company_data_array = SalesForce.add_bx_headers().query_Company_into_dict(company_query_data)

        # ----------------------------------------------------------------------------------------------------------------------
        #  removes unauthorised characters
        # ----------------------------------------------------------------------------------------------------------------------
        cleaned_data = SalesForce.clean_data().remove_unauthorised_characters(company_data_array)

        # ----------------------------------------------------------------------------------------------------------------------
        #  save company file to CSV
        # ----------------------------------------------------------------------------------------------------------------------

        export_to_csv = SalesForce.export_to().company_csv(cleaned_data)

    else:
        logger.info('No records found without a BoardExID')


if __name__ == '__main__':
    download_company_from_sf()