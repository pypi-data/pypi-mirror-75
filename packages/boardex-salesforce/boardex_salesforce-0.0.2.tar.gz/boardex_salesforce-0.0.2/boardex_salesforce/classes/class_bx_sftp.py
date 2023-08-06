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

# ----------------------------------------------------------------------------------------------------------------------
#  Create sftp connection
# ----------------------------------------------------------------------------------------------------------------------
class bx_sftp:
    # ----------------------------------------------------------------------------------------------------------------------
    #  Create sftp connection
    # ----------------------------------------------------------------------------------------------------------------------
    def bx_sftp_connection(self):
        try:
            global_var.logger.debug('-----------------------------sftp_connection_to_BoardEx()'
                                    '------------------------------------------')
            global_var.logger.debug('connecting to Boardex Sftp service')

            sftp_connection = global_var.pysftp.Connection(global_var.myHostname,
                                                           username=global_var.myUsername,
                                                           password=global_var.myPassword)

            global_var.logger.debug(str(global_var.myUsername) + " is connected to: "
                                    + str(global_var.myHostname))
            global_var.logger.debug('Connected to Boardex Sftp service')

            return sftp_connection

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  Get all csv files on remote server
    # ----------------------------------------------------------------------------------------------------------------------
    def get_all_csv(self,sftp_connection):

        try:
            global_var.logger.debug('Getting all csv files from Boardex Sftp ')
            list_all_files = sftp_connection.listdir()
            global_var.logger.debug('Searching for files that contains the word: ' + str(
                global_var.search_out) + ' and has the extension ' + str(global_var.fileExtention))

            for file in list_all_files:
                if str(global_var.search_out) in file and str(file).endswith(str(global_var.fileExtention)):
                    global_var.array_csv_only.append(file)

            global_var.logger.info('csv out file : ' + str(global_var.array_csv_only))
            return global_var.array_csv_only
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e
    # ----------------------------- -----------------------------------------------------------------------------------------
    #  Download all csv file to local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def download_all_csv_from_bx(self,sftp_connection, all_csv_files):
        try:
            global_var.logger.debug('downloading all csv files from sftp server from BoardEx SFTP to '+ global_var.folder_upload_name)
            global_var.logger.debug( 'Downloading  '+str(len(all_csv_files)) +' files to '+ global_var.folder_upload_name)

            # ----------------------------------------------------------------------------------------------------------------------
            #  Create local folders
            # ----------------------------------------------------------------------------------------------------------------------
            local_dir().create_upload_folder()
            for item in  global_var.tqdm(all_csv_files):
                sftp_connection.get(str(item), str(global_var.folder_upload_name) +'//'+str(item))

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e

# ----------------------------------------------------------------------------------------------------------------------
#  Create  folders
# ----------------------------------------------------------------------------------------------------------------------
class create_folder:
    # ----------------------------------------------------------------------------------------------------------------------
    #  create remote archive
    # ----------------------------------------------------------------------------------------------------------------------
    def create_remote_archive_folder(self,sftp_connection):
        global_var.logger.debug('Checking for remote archive folder in archive')
        # check if global_var.path_remote_archive exist
        if sftp_connection.lexists(global_var.path_remote_archive):
            global_var.logger.debug('remote archive folder has already been created')
        else:
            global_var.logger.warning('no archive folder found')
            # creates global_var.path_remote_root folder
            try:
                global_var.logger.info('creating a remote archive folder')
                sftp_connection.mkdir(global_var.os.path.join(global_var.path_remote_archive),
                                      mode=global_var.create_folder_mode)
                global_var.logger.info('remote archive folder created')
            except Exception as e:
                global_var.logger.error(
                    'Could not create archive folder. ')
                global_var.logger.error(e, exc_info=True)
                raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  create log folder
    # ----------------------------------------------------------------------------------------------------------------------
    def create_remote_log_folder(self,sftp_connection ):
        global_var.logger.debug('Checking for remote log folder in archive')
        # check if global_var.path_remote_log exist
        if sftp_connection.lexists(global_var.path_remote_log):
            global_var.logger.debug('remote log folder has already been created')
        else:
            global_var.logger.warning('no log folder found')
            # creates global_var.path_remote_root folder
            try:
                global_var.logger.info('creating a remote log folder')
                sftp_connection.mkdir(global_var.os.path.join(global_var.path_remote_log),
                                      mode=global_var.create_folder_mode)
                global_var.logger.info('remote log folder created')
            except Exception as e:
                global_var.logger.error(
                    'Could not create log folder. ')
                global_var.logger.error(e, exc_info=True)
                raise e
# ----------------------------------------------------------------------------------------------------------------------
#  upload logs
# ----------------------------------------------------------------------------------------------------------------------
class upload_logs_to_sftp:
    # ----------------------------------------------------------------------------------------------------------------------
    #  upload logs to boardEx sftp server
    # ----------------------------------------------------------------------------------------------------------------------
    def upload_log(self,sftp_connection ):
        global_var.logger.debug('Listing all files in '+ str(global_var.path_local_temp))
        listOfFile = global_var.os.listdir()
        global_var.logger.debug('Files found '+ str(listOfFile))

        for logs in listOfFile:
            if global_var.search_logs in logs:
                global_var.logger.debug('Getting all log files ' + str(logs))
                remote_path = global_var.path_remote_log +'//'+ logs
                local_path = global_var.path_local_temp  + logs

                try:
                    global_var.logger.debug('Uploading log file to: ' + str(remote_path))
                    filePath = sftp_connection.put(local_path, remote_path)
                    global_var.logger.debug('log file uploaded to boardex sftp server: ' + remote_path)

                except Exception as e:
                   global_var.logger.error(e, exc_info=True)
                   raise e

# ----------------------------------------------------------------------------------------------------------------------
#  move files on sftp server
# ----------------------------------------------------------------------------------------------------------------------
class move_files:
    # ----------------------------------------------------------------------------------------------------------------------
    #  move files to remote archive folder
    # ----------------------------------------------------------------------------------------------------------------------
    def move_files_to_archive( self, sftp_connection, files):

            try:
                global_var.logger.debug('Moving: ' + str(files) + ' to archive folder on BX sftp')
                if len(files) != 0:
                    for file in files:
                        sftp_connection.rename(file, global_var.path_remote_archive+'//'+file)
                    global_var.logger.debug('Files moved to Archive folder on sftp completed')
                else:
                    global_var.logger.debug('no csv file found to move to archive folder')
            except Exception as e:
                global_var.logger.error(e, exc_info=True)
                raise e

    def move_local_csv_to_archive(self):
        global_var.logger.debug('move local csv to archive')

# ----------------------------------------------------------------------------------------------------------------------
#  creates folders on the local machine
# ----------------------------------------------------------------------------------------------------------------------
class local_dir:
    # ----------------------------------------------------------------------------------------------------------------------
    #  creates split  folder on the local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def create_splitfolder(self):
        try:
            global_var.logger.debug('Checking if there is a local split folder @ '+str(global_var.path_local_split_csv_files))
            if not global_var.os.path.exists(global_var.path_local_split_csv_files):
                global_var.os.makedirs(global_var.path_local_split_csv_files)
                global_var.logger.debug('split cvs folder has been created @ ' + global_var.path_local_split_csv_files)
            else:
                global_var.logger.info('There is split folder @ ' + global_var.path_local_split_csv_files)
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Could not create a local split folder @ ' + str(global_var.path_local_split_csv_files))
            raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  creates archive  folder on the local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def create_archive_folder(self):
        try:
            global_var.logger.debug('Checking if there is a local archive folder @ '+str(global_var.path_local_temp)+'\\'+str(global_var.folder_archive_name))
            if not global_var.os.path.exists(str(global_var.path_local_temp)+'\\'+str(global_var.folder_archive_name)):
                global_var.os.makedirs(str(global_var.path_local_temp)+'\\'+str(global_var.folder_archive_name))
                global_var.logger.debug('archive folder has been created @ ' +str(global_var.path_local_temp)+'\\'+str(global_var.folder_archive_name))
            else:
                global_var.logger.info('There is archive folder @ ' + str(global_var.path_local_temp)+'\\'+str(global_var.folder_archive_name))
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Could not create a local archive folder @ ' + str(global_var.path_local_temp)+'\\'+str(global_var.folder_archive_name))
            raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  creates upload  folder on the local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def create_upload_folder(self):
        try:
            global_var.logger.debug('Checking if there is a local upload folder @ '+str(global_var.folder_upload_name))
            if not global_var.os.path.exists(str(global_var.folder_upload_name)):
                global_var.os.makedirs(str(global_var.folder_upload_name))
                global_var.logger.debug('upload folder has been created @ ' +str(global_var.folder_upload_name))
            else:
                global_var.logger.info('There is upload folder @ ' +str(global_var.folder_upload_name))
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Could not create a local upload folder @ ' +str(global_var.folder_upload_name))
            raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  creates download  folder on the local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def create_download_folder(self):
        try:
            global_var.logger.debug('Checking if there is a local download folder @ '+str(global_var.folder_download_name))
            if not global_var.os.path.exists(str(global_var.folder_download_name)):
                global_var.os.makedirs(str(global_var.folder_download_name))
                global_var.logger.debug('download folder has been created @ ' +str(global_var.folder_download_name))
            else:
                global_var.logger.info('There is download folder @ ' +str(global_var.folder_download_name))
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.error('Could not create a local download folder @ ' +str(global_var.folder_download_name))
            raise e

class delete:
    def split_all_split_files(self):
        try:
            path_local_temp =global_var.os.listdir()

            for folder in path_local_temp:
                if global_var.local_split_folder in folder:
                    try:
                        global_var.logger.info('Deleting files in split folder')

                        global_var.shutil.rmtree(global_var.path_local_split_csv_files)
                    except Exception as e:
                        global_var.logger.error(e, exc_info=True)
                        raise e

        except Exception as e:
                    global_var.logger.error(e, exc_info=True)
                    global_var.logger.debug('ERROR: deleting split folder')

    def combined_csv(self):
        try:
            path_local_temp = global_var.os.listdir()

            for folder in path_local_temp:
                if global_var.combined_company_cvs_filepath in folder:
                    try:
                        global_var.logger.info('Deleting files in combined company folder')
                        global_var.os.remove(global_var.combined_company_cvs_filepath)
                    except Exception as e:
                        global_var.logger.error(e, exc_info=True)
                        raise e
                if global_var.combined_contact_cvs_filepath in folder:
                    try:
                        global_var.logger.info('Deleting files in combined contact folder')
                        global_var.os.remove(global_var.combined_contact_cvs_filepath)
                    except Exception as e:
                        global_var.logger.error(e, exc_info=True)
                        raise e


        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            global_var.logger.debug('ERROR: deleting combined csv files')
            raise e
