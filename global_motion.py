from environment import ExcelManager
from environment import StringsManager
import copy
from _sqlite3 import Row
from pathlib import Path
import numpy as np


EM = ExcelManager()
SM = StringsManager()

################################
EXPERIMENT_A_RESULT_DIRECTORY = r"C:\Users\gabriel\Documents\my-experiments\eyelink-experiment\experiment1\\"
EXPERIMENT_B_RESULT_DIRECTORY = r"C:\Users\gabriel\Documents\my-experiments\eyelink-experiment\experiment2\\"

OUTPUT_EXCEL_FILE_DIRECTORY = r"C:\Users\gabriel\Documents\my-experiments\\"
################################


################################
EXPERIMENT_A_FILE_NAME = 'a'
EXPERIMENT_B_FILE_NAME = 'b'
################################

################################
NAME_OF_FILE = "src"
EXCEL_FORMAT = ".xls"
TXT_FORMAT = ".txt"
SLASH = '\\'
################################

################################
COLUMNS_NAMES = ['TRIAL_INDEX', 'signalstrength', 'direction',  'speed', 'displacement', 'signalplacemen',  'expected_key_pressed', 'ANSWER',  'KEYPRESS', 'CORRECT_OR_INCORRECT', 'RESPONSE', 'IA_FIXATION_%',  'IA_FIXATION_COUNT']
LABELS_TO_NUMERATE = ['IA_FIXATION_%', 'IA_FIXATION_COUNT']
NUMBER_OF_TRIAL_ROWS = 3
################################

NUMBER_OF_ROW_DUPLICATIONS = 6

def temp_func():
    

def create_new_duplicated_row_matrix(sheet_directory):
    _, sheet, _, _ = EM.open_file(sheet_directory)
    label_matrix, data_matrix = get_matrices(sheet_directory)
    
    number_of_rows, number_of_columns = EM.get_dimensions(sheet)
    new_number_of_rows = number_of_rows * NUMBER_OF_ROW_DUPLICATIONS
    new_matrix = np.zeros(shape=(new_number_of_rows, number_of_columns))
    
    new_data_matrix = duplicate_each_data_row(data_matrix, new_matrix, number_of_rows, number_of_columns)
    print(number_of_rows, number_of_columns)
    new_matrix = EM.concatenate_matrices(label_matrix, new_data_matrix)
    
    return new_matrix

# duplicate data rows except labels and create new matrix
def duplicate_each_data_row(data_matrix, new_matrix, number_of_rows, number_of_columns):
    for row in range(1, number_of_rows):
       
        current_row = EM.create_row(data_matrix[:row], number_of_columns)
        np.insert(new_matrix, (row*NUMBER_OF_ROW_DUPLICATIONS)+1, current_row, NUMBER_OF_ROW_DUPLICATIONS)  
    
    return new_matrix

# create label and data matrix from excel file
def get_matrices(sheet_directory):
    _, sheet, _, _ = EM.open_file(sheet_directory)
    
    label_matrix = EM.create_label_matrix(sheet)
    data_matrix = EM.create_data_matrix(sheet)
    
    return label_matrix, data_matrix

# enumerate dynamic labels and create new labels vector
def numerate_labels(labels):
    new_labels = copy.deepcopy(labels)
     
    # enumerate labels 
    for label in  LABELS_TO_NUMERATE:
        for trial_row in range(1, NUMBER_OF_TRIAL_ROWS+1):
            new_name = [label,'_',str(trial_row)]
            new_label_name = ''.join(new_name)
            new_labels.append(new_label_name)
            
    # remove unumbered labels          
    for label in  LABELS_TO_NUMERATE:
        new_labels.remove(label)
   
    return new_labels


def create_columns_vector(original_columns, new_columns, number_of_columns):
    # create new vectors 
    columns_vector = [0 for columns in range(number_of_columns)]
    
    # insert into the new vector the updated columns
    for column in range(number_of_columns):
        columns_vector[column] = original_columns.index(new_columns[column])

    return columns_vector
    
def  insert_to_new_data_matrix(new_data, original_data, static_labels_column_vector, dynamic_label_column_vector, new_number_of_rows, number_of_static_labels, number_of_dynamic_labels):
    for row in  range(new_number_of_rows): 
        # jump to the next trial row
        trial_number = row * NUMBER_OF_TRIAL_ROWS
        for column in range(number_of_static_labels):
            # get static labels columns
            current_original_column = static_labels_column_vector[column]
            
            # insert static data to the new matrix
            new_data[row][column] = original_data[trial_number][current_original_column]
            
        # iterate through dynamic labels and insert dynamic row data to new numerated labels
        for current_dynamic_label in range(number_of_dynamic_labels):
            # number of columns inserted for the dynamic labels
            next_label_column_jump = current_dynamic_label * NUMBER_OF_TRIAL_ROWS
            
            # get the original dynamic label
            original_dynamic_label_column = dynamic_label_column_vector[current_dynamic_label]  
             
            # iterate through number of rows in the current trial 
            for trial_row in range(NUMBER_OF_TRIAL_ROWS):
                # get the current column for the new numerated label
                new_dynamic_label_column = number_of_static_labels + next_label_column_jump + trial_row
                
                # current trail row
                trial_row = trial_number + trial_row
                
                # insert to the new data matrix
                new_data[row][new_dynamic_label_column] = original_data[trial_row][original_dynamic_label_column]
               
    return new_data

# create the new data result matrix       

def create_new_data_matrix(original_data, original_labels, new_labels, number_of_original_label_rows, number_of_original_labels):
    # calculation for the new matrix dimension
    new_number_of_rows = int((number_of_original_label_rows-1)/NUMBER_OF_TRIAL_ROWS)
    new_number_of_columns = len(new_labels)
    number_of_deleted_original_labels = len(LABELS_TO_NUMERATE)
    number_of_static_labels = number_of_original_labels - number_of_deleted_original_labels
    
    # create new matrix
    new_matrix = EM.create_new_matrix(new_number_of_rows, new_number_of_columns) 
    
    # create 'columns vector' that hold the updated columns of the labels
    columns_vector_of_original_labels = create_columns_vector(original_labels, new_labels, number_of_static_labels)
    columns_vector_of_deleted_labels  = create_columns_vector(original_labels, LABELS_TO_NUMERATE, number_of_deleted_original_labels)
    
    # insert the data to the new matrix
    new_matrix = insert_to_new_data_matrix(new_matrix, original_data, columns_vector_of_original_labels, columns_vector_of_deleted_labels,new_number_of_rows, number_of_static_labels, number_of_deleted_original_labels)
    return new_matrix


# merge each trial multiple rows into a single row 
def merge_trial_indices_lines(directory):
    _, _, number_of_rows, number_of_columns = EM.open_file(directory)
    
    original_labels, original_data = get_matrices(directory)
    # create new labels by numerating each 'dynamic label' (labels where the data changes through the same trial rows) 
    new_labels = numerate_labels(original_labels)
    # create a new matrix where each trial data is inserted in a single line
    new_data = create_new_data_matrix(original_data, original_labels, new_labels, number_of_rows, number_of_columns)
    
    new_matrix = EM.merge_labels_and_data(new_labels, new_data)
    
    return new_matrix

# insert new matrix data into a new excel file 
def create_new_result_file(directory, new_matrix):
    file, sheet = EM.create_new_excel_file()
    
    EM.copy_to_excel_file(sheet, new_matrix)
    
    file.save(directory) 

def merge(labels, matrix_data_1, matrix_data_2):
    day_separator = EM.create_row(["Day 2"], len(matrix_data_1[1:]))

    data_matrix = EM.concatenate_matrices([matrix_data_1, day_separator, matrix_data_2])
    final_matrix = EM.concatenate_labels_and_data_matrix(labels, data_matrix)
    
    return final_matrix

# merge 2 files and return a new matrix with both files data
def create_new_matrix_from_excel_files_data(excel_file_directory_1, excel_file_directory_2):
    matrices_labels, matrix_data_1 = get_matrices(excel_file_directory_1)
    _, matrix_data_2 = get_matrices(excel_file_directory_2)
     
    final_matrix = merge(matrices_labels, matrix_data_1, matrix_data_2)
    
    return final_matrix

def merge_directory_names(participant_name):
    txt_file_1 = SM.merge_strings([EXPERIMENT_A_RESULT_DIRECTORY,SLASH, participant_name, SLASH, EXPERIMENT_A_FILE_NAME, TXT_FORMAT])
    txt_file_2 = SM.merge_strings([EXPERIMENT_B_RESULT_DIRECTORY, SLASH, participant_name, SLASH, EXPERIMENT_B_FILE_NAME, TXT_FORMAT])
    output_file_directory = SM.merge_strings([OUTPUT_EXCEL_FILE_DIRECTORY, participant_name, EXCEL_FORMAT])
    
    return txt_file_1, txt_file_2, output_file_directory

def convert_input_files_to_txt_file(txt_file_1, txt_file_2):
    excel_file_1_directory = EM.create_excel_from_txt_file(txt_file_1)
    excel_file_2_directory = EM.create_excel_from_txt_file(txt_file_2)
    return excel_file_1_directory, excel_file_2_directory
    