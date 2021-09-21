import os

class Carver():
    def __init__(self, scan_target, save_directory, file_header_list):
        # Initialize variables
        self.scan_target = str(scan_target.get())
        self.save_directory = str(save_directory.get())

        self.file_header_list = file_header_list

        print(self.scan_target)
        print(self.save_directory)
        print(self.file_header_list)

    def start(self):

        recovered_files_list = []

        with open(self.scan_target, 'rb') as drive:
            start_sector = 0
            end_sector = 1000000

            sector_size = 512
            recovery_counter = dict((key,0) for key in self.file_header_list.keys())
            max_file_size = 10000000

            while start_sector < end_sector:
                try:
                    recovered_file_record = [None, None, None, None]

                    drive.seek(start_sector * sector_size)

                    sector_file_header = ''

                    sector_file_header = drive.read(32)

                    for file_type in self.file_header_list:
                        if sector_file_header[:len(self.file_header_list[file_type][0])] == self.file_header_list[file_type][0]:

                            print(file_type.upper() + ' File Signature Found at sector', start_sector, end="")

                            recovery_counter[file_type] += 1

                            recovered_file_record[0] = str(recovery_counter[file_type]) + '.' + file_type

                            recovered_file_record[1] = self.save_directory + '/' + str(recovery_counter[file_type]) + '.' + file_type

                            recovered_file_record[2] = 'High'

                            recovered_file_record[3] = self.save_directory + '/' + str(recovery_counter[file_type]) + '.' + file_type

                            recovered_file = open(self.save_directory + '/' + str(recovery_counter[file_type]) + '.' + file_type, 'wb')

                            recovering = True

                            drive.seek(start_sector * sector_size)

                            max_file_size_counter = 0

                            file_footer_length = len(self.file_header_list[file_type][1])
                            sector_file_footer = b'\x00' * file_footer_length

                            while recovering and max_file_size_counter < max_file_size:
                                read = drive.read(1)
                                sector_file_footer = sector_file_footer[1:file_footer_length] + read

                                recovered_file.write(read)

                                if sector_file_footer == self.file_header_list[file_type][1]:

                                    recovering = False
                                    recovered_file_record[1] = str("{:.2f}".format(round(max_file_size_counter * 0.001, 2))) + ' KB' 

                                    recovered_file.close()
                                    recovered_files_list.append(recovered_file_record)

                                    print(" - Recovery Successful!")

                                max_file_size_counter += 1

                            if max_file_size_counter >= max_file_size:
                                recovered_file_record[1] = str("{:.2f}".format(round(max_file_size_counter * 0.001, 2))) + ' KB'
                                recovered_file_record[2] = 'Low'

                                recovered_file.close()

                                recovered_files_list.append(recovered_file_record)
                                print(" - Recovery Failed")

                except:
                    pass

                # increment the start_sector to move from one sector to another
                start_sector += 1

        return recovered_files_list
