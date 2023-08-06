from .classes import class_download_salesforce as SalesForce
from .classes.global_var import logger, combined_contact_cvs_filepath, combined_company_cvs_filepath
from .classes.class_bx_sftp import local_dir, delete, upload_logs_to_sftp, bx_sftp
from . import global_var
from .classes import class_upload_to_salesforce as upload
from .classes import class_csv as csv


def upload_to_sf():

    # ----------------------------------------------------------------------------------------------------------------------
    #  Create upload folder
    # ----------------------------------------------------------------------------------------------------------------------
    local_dir().create_upload_folder()
    # ----------------------------------------------------------------------------------------------------------------------
    #  Download all csv OUT file to local machine and move them to archive
    # ----------------------------------------------------------------------------------------------------------------------
    upload.download_from_sftp().download_all_csv()

    # ----------------------------------------------------------------------------------------------------------------------
    #  Locate all csv file on local machine
    # ----------------------------------------------------------------------------------------------------------------------

    all_concordance_result_file = csv.csv().get_csv_out()
    logger.info(str(len(all_concordance_result_file)) + ' csv out files found on local machine')

    # ----------------------------------------------------------------------------------------------------------------------
    #   all company csv file on local machine
    # ----------------------------------------------------------------------------------------------------------------------

    company_concordance_output = csv.csv().get_company_out(all_concordance_result_file)

    if len(company_concordance_output) !=0:
        logger.info(company_concordance_output)
        logger.debug(company_concordance_output)
        # ----------------------------------------------------------------------------------------------------------------------
        #   merge or rename company files
        # ----------------------------------------------------------------------------------------------------------------------
        combined_company_concordance_output = csv.csv().merge_csv(company_concordance_output, combined_company_cvs_filepath)

        # ----------------------------------------------------------------------------------------------------------------------
        #  count number of rows company
        # ----------------------------------------------------------------------------------------------------------------------
        company_row_count = csv.csv().count_total_rows(combined_company_concordance_output)
        logger.info(str(company_row_count) +' rows for company out csv')
        logger.debug(str(company_row_count) +' rows for company out csv')

    else:
        logger.debug('No company concordance found')

    # ----------------------------------------------------------------------------------------------------------------------
    #   all contact csv file on local machine
    # ----------------------------------------------------------------------------------------------------------------------

    contact_concordance_output = csv.csv().get_contact_out(all_concordance_result_file)

    if len(contact_concordance_output) !=0:
        logger.debug(contact_concordance_output)
        # ----------------------------------------------------------------------------------------------------------------------
        #   merge or rename contact files
        # ----------------------------------------------------------------------------------------------------------------------
        combined_contact_concordance_output = csv.csv().merge_csv(contact_concordance_output, combined_contact_cvs_filepath)
        # ----------------------------------------------------------------------------------------------------------------------
        #  count number of rows contact
        # ----------------------------------------------------------------------------------------------------------------------
        contact_row_count = csv.csv().count_total_rows(combined_contact_concordance_output)
        logger.debug(str(contact_row_count) +' rows for contacts out csv')
    else:
        logger.debug('No contact concordance found')


    # ----------------------------------------------------------------------------------------------------------------------
    #  create a folder to store any csv that has been split
    # ----------------------------------------------------------------------------------------------------------------------
    try:
        local_dir().create_splitfolder()
    except Exception as e:
        global_var.logger.error(e, exc_info=True)
        raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  split contact csv files
    # ----------------------------------------------------------------------------------------------------------------------
    if len(contact_concordance_output) !=0:

        if contact_row_count >= global_var.row_limit1:
            logger.info('splitting merged contact csv file ....')
            csv.split_csv().split_contact_csv(open(global_var.combined_contact_cvs_filepath, 'r' ,  encoding =  global_var.encoder))
            logger.info('Spliting complete')
        else:
            logger.info(global_var.combined_contact_cvs_filepath)
            global_var.shutil.move(global_var.combined_contact_cvs_filepath, global_var.moved_combined_contact_cvs_filepath)
    else:
        logger.info('no contact out files found')

    # ----------------------------------------------------------------------------------------------------------------------
    #  split company csv files
    # ----------------------------------------------------------------------------------------------------------------------
    if len(company_concordance_output) != 0:

        if company_row_count >= global_var.row_limit1:
            logger.info('splitting merged company csv file ....')
            csv.split_csv().split_company_csv(open(global_var.combined_company_cvs_filepath, 'r' ,  encoding =  global_var.encoder))
            logger.info('Spliting complete')
        else:
            logger.info(global_var.combined_company_cvs_filepath)
            global_var.shutil.move(global_var.combined_company_cvs_filepath, global_var.moved_combined_company_cvs_filepath)
    else:
        logger.info('no company files found')

    # ----------------------------------------------------------------------------------------------------------------------
    #  get all split files
    # ----------------------------------------------------------------------------------------------------------------------

    all_split_csv = csv.csv().get_local_split_csv()

    # ----------------------------------------------------------------------------------------------------------------------
    #  get all company split files
    # ----------------------------------------------------------------------------------------------------------------------

    if len(company_concordance_output) != 0:
        company_split_csv = csv.csv().get_local_company_csv(all_split_csv)
        logger.info('Number of company csv split files: ' + str(len(company_split_csv)))
    else:
        logger.info('no company files found')

    # ----------------------------------------------------------------------------------------------------------------------
    #  get all contact split files
    # ----------------------------------------------------------------------------------------------------------------------
    if len(contact_concordance_output) != 0:

        contact_split_csv = csv.csv().get_local_contact_csv(all_split_csv)
        logger.info('Number of contact csv split files: ' + str(len(contact_split_csv)))
    else:
        logger.info('no Contact files found')


    # ----------------------------------------------------------------------------------------------------------------------
    #  salesforce connection
    # ----------------------------------------------------------------------------------------------------------------------

    salesForceConnection = SalesForce.salesforce_connection().sf_connection()

    # ----------------------------------------------------------------------------------------------------------------------
    #   updates salesforce with BoardExID
    # ----------------------------------------------------------------------------------------------------------------------
    if len(company_concordance_output) != 0:

        if len(company_split_csv) !=0 :
            for i in global_var.tqdm(company_split_csv):
                upload.upload_to_salesfore().update_company_to_sf(salesForceConnection, str(global_var.path_local_split_csv_files)+'\\'+str(i))
        else:
            upload.upload_to_salesfore().update_company_to_sf(salesForceConnection, str(global_var.moved_combined_company_cvs_filepath))
    else:
        logger.info('no company files found')

    # ----------------------------------------------------------------------------------------------------------------------
    #   updates salesforce with BoardExID
    # ----------------------------------------------------------------------------------------------------------------------
    if len(contact_concordance_output) != 0:
        if len(contact_split_csv) !=0 :
            for i in global_var.tqdm(contact_split_csv):
                upload.upload_to_salesfore().update_contacts_to_sf(salesForceConnection, global_var.path_local_split_csv_files+'\\'+i)
        else:
            upload.upload_to_salesfore().update_contacts_to_sf(salesForceConnection, global_var.moved_combined_contact_cvs_filepath)
    else:
        logger.info('no company files found')

    # ----------------------------------------------------------------------------------------------------------------------
    #   delete local split or merged files
    # ----------------------------------------------------------------------------------------------------------------------

    delete().split_all_split_files()
    delete().combined_csv()

    # ----------------------------------------------------------------------------------------------------------------------
    #  sftp connection to BoardEx from class_bx_sftp
    # ----------------------------------------------------------------------------------------------------------------------
    if global_var.upload_to_sftp == True:
        sftp_conn = bx_sftp().bx_sftp_connection()
    else:
        logger.info(global_var.upload_to_sftp)

    # ----------------------------------------------------------------------------------------------------------------------
    #  uploads csv file
    # ----------------------------------------------------------------------------------------------------------------------
    if global_var.upload_to_sftp == True:
        upload_logs_to_sftp().upload_log(sftp_conn)
    else:
        logger.info(global_var.upload_to_sftp)

if __name__ == '__main__':
    upload_to_sf()