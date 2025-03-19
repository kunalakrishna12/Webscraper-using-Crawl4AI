import pandas as pd
import os
def combine_excel_files(input_folder, output_filename,output_folder):
    """
    Combines data from multiple Excel files in a folder into a single Excel file.
    Args:
        input_folder (str): Path to the folder containing the Excel files.
        output_file (str): Path to the output Excel file.
    """
    all_data = pd.DataFrame()  # Initialize an empty DataFrame
    for filename in os.listdir(input_folder):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):  # Check for Excel files
            filepath = os.path.join(input_folder, filename)
            try:
                df = pd.read_excel(filepath)
                all_data = pd.concat([all_data, df], ignore_index=True) # Append to the combined DataFrame
                print(f"Successfully read and combined data from: {filename}")
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
                continue # Skip to the next file if there's an error
    if not all_data.empty:
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, output_filename)  # Construct the full output path
        try:
            all_data.to_excel(output_path, index=False)
            print(f"Combined data saved to: {output_path}")
        except Exception as e:
            print(f"Error saving combined data to {output_path}: {e}")
    else:
        print("No data found to combine.")
# Example usage:
input_folder = "/home/krishna/Desktop/Big E Brains/Projects/Crawl4AI Webscraper/data"  # Replace with the actual path to your folder
output_folder = "/home/krishna/Desktop/Big E Brains/Projects/Crawl4AI Webscraper"  # Replace with the desired output folder
output_filename = "Stainless Steel 316 Round Bar.xlsx"  # Replace with the desired output file name
combine_excel_files(input_folder, output_filename,output_folder)









