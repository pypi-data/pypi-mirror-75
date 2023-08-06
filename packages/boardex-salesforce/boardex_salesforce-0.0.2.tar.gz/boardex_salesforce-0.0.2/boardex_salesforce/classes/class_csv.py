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
#  CSV
# ----------------------------------------------------------------------------------------------------------------------

class csv:
    # ----------------------------------------------------------------------------------------------------------------------
    #  Count number of rows in csv file
    # ----------------------------------------------------------------------------------------------------------------------
    def count_total_rows(self, filename):
            global_var.logger.debug('Counting total rows')
            with open(filename) as f:
                return sum(1 for line in f)

    # ----------------------------------------------------------------------------------------------------------------------
    #  Get all csv files on local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def get_csv_out(self):
        try:
            global_var.logger.debug('Getting all csv files local machine')
            listOfFile = global_var.os.listdir(global_var.folder_upload_name)
            global_var.logger.debug('Searching for files that contains the word: ' + str(
                global_var.search_out) + ' and has the extension ' + str(global_var.fileExtention))

            for file in listOfFile:
                if str(global_var.search_out) in file and str(file).endswith(str(global_var.fileExtention)):
                    global_var.array_csv_only.append(file)

            global_var.logger.info('csv out file : ' + str(global_var.array_csv_only))
            return global_var.array_csv_only

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e
    # ----------------------------------------------------------------------------------------------------------------------
    #  Get all company csv out files on local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def get_company_out(self, all_concordance_result_file):
        try:
            global_var.logger.debug('Getting all company csv files local machine')

            for company in all_concordance_result_file:
                if global_var.search_company in company:
                    global_var.array_company.append(str(global_var.folder_upload_name)+'//'+str(company))

            return global_var.array_company
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  Get all company csv out files on local machine
    # ----------------------------------------------------------------------------------------------------------------------
    def get_contact_out(self,all_concordance_result_file):
        try:
            global_var.logger.debug('Getting all contact csv files local machine')

            for contact in all_concordance_result_file:
                if global_var.search_contact in contact:
                    global_var.array_contact.append(str(global_var.folder_upload_name)+'//'+str(contact))

            return global_var.array_contact
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  merge csv files
    # ----------------------------------------------------------------------------------------------------------------------
    def merge_csv(self, concordance_output, combined_cvs_filepath):

        try:
            global_var.logger.debug('Combining csv : ' + str(concordance_output))
            combined_csv = global_var.pd.concat(
            [global_var.pd.read_csv(f) for f in global_var.tqdm(concordance_output)], sort=False)

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e

        try:
            global_var.logger.debug('outputing csv :' + str(combined_cvs_filepath))

            combined_csv.to_csv(combined_cvs_filepath, index=False, encoding=global_var.encoder)
            global_var.logger.debug('Combine completed, file@ ' + str(combined_cvs_filepath))

            return combined_cvs_filepath

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  gets local split csv files
    # ----------------------------------------------------------------------------------------------------------------------
    def get_local_split_csv(self):
        global_var.logger.debug('Getting all csv files on local machine @ ' + str(global_var.path_local_split_csv_files))
        array_csv_only1 = []
        try:
        # Getting all csv files on local machine
        # r=root, d=directories, f = files
            for r, d, f in global_var.os.walk(global_var.path_local_split_csv_files):
                for file in f:
                    try:
                        if  global_var.search_split_csv in file and str(file).endswith('.csv') :
                            array_csv_only1.append(file)
                        else:
                            global_var.logger.debug('no split csv files found')

                    except Exception as e:
                        global_var.logger.error(e, exc_info=True)
                        raise e

            return array_csv_only1
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e

    # ----------------------------------------------------------------------------------------------------------------------
    #  gets local company split csv files
    # ----------------------------------------------------------------------------------------------------------------------
    def get_local_company_csv(self, all_local_csv):
        array_local_company = []
        global_var.logger.debug('Getting all company csv files on local machine from '
                                + str(global_var.path_local_split_csv_files))
        try:
            for eachFile in all_local_csv:
                if global_var.search_split_company in eachFile:
                    array_local_company.append(eachFile)

            return array_local_company
        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e


    # ----------------------------------------------------------------------------------------------------------------------
    #  gets local contact split csv files
    # ----------------------------------------------------------------------------------------------------------------------
    def get_local_contact_csv(self, all_local_csv):
        array_local_contacts = []
        global_var.logger.debug('Getting all contact csv files on local machine from '
                                + str(global_var.path_local_split_csv_files))
        try:
            for eachFile in all_local_csv:
                if global_var.search_split_contact in eachFile:
                    array_local_contacts.append(eachFile)

            return array_local_contacts

        except Exception as e:
            global_var.logger.error(e, exc_info=True)
            raise e

# ----------------------------------------------------------------------------------------------------------------------
#  split combine csv file into multiple files
# ----------------------------------------------------------------------------------------------------------------------
class split_csv:
    # ----------------------------------------------------------------------------------------------------------------------
    #  split company csv files
    # ----------------------------------------------------------------------------------------------------------------------
    def split_company_csv(self,  filehandler,
                          delimiter=global_var.delimiter,
                          row_limit=global_var.row_limit1,
                          output_name_template=global_var.split_company_output_filename,
                          output_path=global_var.path_local_split_csv_files,
                          keep_headers=True):

            global_var.logger.debug('Splitting company files and placing them in ' + str(global_var.path_local_split_csv_files))

            reader = global_var.csv.reader(filehandler, delimiter=delimiter)
            current_piece = 1
            current_out_path =global_var. os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = global_var.csv.writer(open(current_out_path, 'w', newline='', encoding=global_var.encoder),
                                            delimiter=delimiter)
            current_limit = row_limit
            if keep_headers:
                headers = next(reader)
                current_out_writer.writerow(headers)
            for i, row in enumerate(reader):
                if i + 1 > current_limit:
                    current_piece += 1
                    current_limit = row_limit * current_piece
                    current_out_path = global_var.os.path.join(
                        output_path,
                      output_name_template % current_piece
                    )
                    current_out_writer = global_var.csv.writer(open(current_out_path, 'w', newline='', encoding=global_var.encoder),
                                                    delimiter=delimiter)
                    if keep_headers:
                        current_out_writer.writerow(headers)
                current_out_writer.writerow(row)

    # ----------------------------------------------------------------------------------------------------------------------
    #  split contact csv files
    # ----------------------------------------------------------------------------------------------------------------------

    def split_contact_csv(self, filehandler, delimiter='|', row_limit=global_var.row_limit1,
                          output_name_template=global_var.split_contact_output_filename,
                          output_path=global_var.path_local_split_csv_files, keep_headers=True):

        global_var.logger.debug('Splitting contact files and placing them in ' + str(global_var.path_local_split_csv_files))

        reader = global_var.csv.reader(filehandler, delimiter=delimiter)
        current_piece = 1
        current_out_path = global_var.os.path.join(
            output_path,
            output_name_template % current_piece
        )
        current_out_writer = global_var.csv.writer(open(current_out_path, 'w', newline='', encoding=global_var.encoder),
                                        delimiter=delimiter)
        current_limit = row_limit
        if keep_headers:
            headers = next(reader)
            current_out_writer.writerow(headers)
        for i, row in enumerate(reader):
            if i + 1 > current_limit:
                current_piece += 1
                current_limit = row_limit * current_piece
                current_out_path = global_var.os.path.join(
                    output_path,
                    output_name_template % current_piece
                )
                current_out_writer = global_var.csv.writer(open(current_out_path, 'w', newline='', encoding=global_var.encoder),
                                                delimiter=delimiter)
                if keep_headers:
                    current_out_writer.writerow(headers)
            current_out_writer.writerow(row)