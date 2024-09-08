import os
import re
import pandas as pd

# Function to read data from text files and write to both text and Excel files
def combine_text_files(input_folder, output_file, excel_output_file):
    file_data = []
    header = []

    # Iterate over all files in the input folder
    for idx, filename in enumerate(sorted(os.listdir(input_folder))):
        if filename.endswith('.asc'):  # Process only .asc files
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as infile:
                lines = infile.readlines()

                # Determine the number of columns in the current file
                num_columns = len(lines[0].strip().split())

                # Extract the base filename (remove extension only)
                base_filename = os.path.splitext(filename)[0]  # Remove the extension, keep filename

                # Generate headers with the same base filename for all columns
                file_header = [base_filename] * num_columns

                # For the first file, include all headers and all data
                if idx == 0:
                    header.extend(file_header)  # Include headers for all columns
                    for line in lines:
                        file_data.append(line.strip().split())  # Append all columns of data
                else:
                    # For subsequent files, skip the first column header and its corresponding data
                    header.extend(file_header[1:])  # Skip the first header
                    for i, line in enumerate(lines):
                        file_data[i].extend(line.strip().split()[1:])  # Skip the first column of data

    # Write the combined data to the output text file
    with open(output_file, 'w') as outfile:
        # Write the headers
        outfile.write('\t'.join(header) + '\n')
        # Write the combined data rows
        for data in file_data:
            outfile.write('\t'.join(data) + '\n')

    # Convert the data to a DataFrame for Excel output
    df = pd.DataFrame(file_data, columns=header)

    # Write the DataFrame to an Excel file
    df.to_excel(excel_output_file, index=False)

    print(f"Data from all text files in '{input_folder}' has been written to '{output_file}' and '{excel_output_file}'")

# Specify the input folder and output files
current_directory = os.getcwd()
asc_folder_path = os.path.join(current_directory, 'asc')  # Replace with your 'asc' folder
input_folder = asc_folder_path  # Input folder path
text_filename = "data.txt"
output_file = os.path.join(current_directory, text_filename)  # Output text file path
excel_filename = "data.xlsx"
excel_output_file = os.path.join(current_directory, excel_filename)  # Output Excel file path

# Call the function to combine text files and export to both formats
combine_text_files(input_folder, output_file, excel_output_file)
