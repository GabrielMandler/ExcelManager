import xlrd
import xlwt
import string
import numpy as np

class ExcelManager:
    def open_file(self, path):
        # check if the file exists   
        #self.check_path(path)
        
        # if the file exist open it
        try:
            book = xlrd.open_workbook(path)
        except:
            print ("The file doesn't exist")
            
        sheet = book.sheet_by_index(0)
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        return book, sheet, number_of_rows, number_of_columns
    
    """ check if the file exist
    def check_path(self, file_path):
        file = path(file)
        if file.is_file():
            print("The path doesn't exist!")
            return False
    """
    # create new Workbook
    def create_new_excel_file(self):        
        workbook = xlwt.Workbook() 
        sheet = workbook.add_sheet("BLOCK") 
        return workbook, sheet
    
    def concatenate_labels_and_data_matrix(self, labels, matrix):
        labels_vector = np.array([labels])
        data_matrix = np.array(matrix)
        
        matrix = np.concatenate((labels_vector, data_matrix), axis = 0)
        
        return matrix
    
    def get_dimensions(self, sheet):
        number_of_columns = sheet.ncols
        number_of_rows = sheet.nrows
        
        return number_of_rows, number_of_columns
    
    def concatenate_matrices(self, matrices_list):
        matrix = np.array(matrices_list[0])
        
        for current_matrix in matrices_list[1:len(matrices_list)]:
            current_matrix = np.array(current_matrix)
            
            matrix = np.concatenate((matrix, current_matrix))
        
        return matrix
    
    # copy matrix to excel file
    def copy_to_excel_file(self, sheet, new_matrix):
        for row_count, row_value in enumerate(new_matrix):
            for column_count, column_value in enumerate(row_value):
                sheet.write(row_count, column_count, column_value)
                
    def open_txt_file(self, directory):
        try: 
            txt_file = open(directory, 'r+')
        except:
            print("The text file wasn't found")
            return False
        
        return txt_file
    
    # get complete row
    def get_row(self, sheet, row):
        number_of_columns = sheet.ncols
        row = sheet.row_values(rowx = row, 
                              start_colx = 0, 
                              end_colx = number_of_columns)
        
        return row
    
    def create_new_matrix(self, number_of_rows, number_of_columns):
        new_matrix = [[0 for column in range(number_of_columns)] for row in range(number_of_rows)]
        return new_matrix
    
    def merge_labels_and_data(self, new_labels, new_data):    
        new_data.insert(0, new_labels)
        return new_data
    
    def create_row(self, row_values, number_of_columns):
        print(number_of_columns)
        row = np.empty((0, number_of_columns), int)
        print(row)
        i = 0
        #for value in row_values:
        np.insert(row, 0, row_values)
        i = i + 1
            
        return row
    
    # create labels matrix from excel file 
    def create_label_matrix(self, sheet):
        # get label's row
        row = self.get_row(sheet, 0)
         
        return row
    
    # create data matrix from excel file  
    def create_data_matrix(self, sheet):
        matrix = []
        number_of_rows = sheet.nrows
        for row in range(number_of_rows-1):
            current_row = self.get_row(sheet, row+1) 
            matrix.append(current_row)
                            
        return matrix
    
    def create_new_vector(self, vector_size):
        new_vector = [0 for columns in range(vector_size)]
        return new_vector
    
    def create_list_from_txt_file(self, txt_file_directory):
        # open text file
        txt_file = self.open_txt_file(txt_file_directory)
        
        # read text file and insert into list
        list = []
        for line in txt_file.readlines():
            column = [value for value in line.split()]
            list.append(column)
    
        txt_file.close()

        return list
        
    def create_excel_from_txt_file(self, directory):
        # copy the text file content into new list  
        new_matrix = self.create_list_from_txt_file(directory)
        
        # create new excel file
        workbook, worksheet = self.create_new_excel_file()
        
        # write to a new excel file
        self.copy_to_excel_file(worksheet, new_matrix)

        # save new excel file
        new_directory = directory.replace('.txt','.xls')
        workbook.save(new_directory)
        
        return new_directory
        
    
            
            
class StringsManager: 
    # check if  
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False 
    """
    def find_between(self, s):
        self.new_string = s
        if(s.find("text") != -1):
            text_start_symbol = "'"
            start = s.index( text_start_symbol ) + len( text_start_symbol )
            end = s.index( text_start_symbol, start )
            self.new_string = s[start:end]
        elif(s.find("number") != -1):
            number_start_symbol = ":"
            start = s.index( number_start_symbol ) + len( number_start_symbol )
            self.new_string = s[start:]   
        return self.new_string
    """
    # concatenate_matrices strings
    def merge_strings(self, list_of_strings):
        self.new_directory = ''
        for string in list_of_strings:
            self.new_directory += string
        
        return self.new_directory
        