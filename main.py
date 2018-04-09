from global_motion import *

################################
PARTICIPANT_NAME = "result"
################################

################################
SHEET_DIRECTORY = r"C:\Users\gabriel\Documents\src.xlsx"
OUTPUT_SHEET_DIRECTORY = r"C:\Users\gabriel\Documents\new_src.xlsx"
################################

def main():
    """txt_file_1, txt_file_2, output_file_directory = merge_directory_names(PARTICIPANT_NAME)
    
    excel_file_1_directory, excel_file_2_directory = convert_input_files_to_txt_file(txt_file_1, txt_file_2)    
    
    final_matrix = create_new_matrix_from_excel_files_data(excel_file_1_directory, excel_file_2_directory)
    
    create_new_result_file(output_file_directory, final_matrix)

    new_matrix = merge_trial_indices_lines(output_file_directory)
    
    create_new_result_file(output_file_directory, new_matrix)
    """
    new_matrix = create_new_duplicated_row_matrix(SHEET_DIRECTORY)
    
    create_new_result_file(OUTPUT_SHEET_DIRECTORY, new_matrix)
    
    
if __name__ == '__main__':main()