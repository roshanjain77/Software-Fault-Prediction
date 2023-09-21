"""Extracting source code"""
import logging
import os
import re
import tarfile
import traceback
import zipfile

import pandas as pd

SOURCE_CODE_FOLDER = "../data/source_code"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s')


def unzip_files(directory):
    logging.info(f"Unzipping files in {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(root)
                logging.info(f"Unzipped {file} to {root}")
            elif file.endswith(".tar.gz"):
                with tarfile.open(file_path, 'r:gz') as tar_ref:
                    try:
                        tar_ref.extractall(root)
                        logging.info(f"Extracted {file} to {root}")
                    except:
                        logging.error(f"Failed to extract {file}")
                        logging.error(traceback.format_exc())


def list_all_java_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if re.search(r"\.java$", file):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


def process_file(csv_file):
    data = pd.read_csv(csv_file)

    def remove_extension(file_name):
        return ".".join(file_name.split(".")[:-1])

    software_name, version = remove_extension(csv_file).split("/")[-1].split("-")
    data["file_loc"] = ""

    logging.info(f"Processing {csv_file}: {software_name}-{version} Adding location of source code")

    file_list = list_all_java_files(SOURCE_CODE_FOLDER)
    potential_list = []
    for file in file_list:
        if software_name in file and version in file:
            potential_list.append(file)
    
    logging.debug(f"Potential list for {software_name}-{version}:", potential_list)

    for index, row in data.iterrows():
        file_name = row['name']
        file_name = file_name.replace(".", "/") + ".java"

        candidate_list = []
        for file in potential_list:
            if file_name in file and "testcases" not in file:
                candidate_list.append(file)
        if len(candidate_list) != 1:
            logging.error(f"Failed to find {file_name}")
            logging.error("Candidates: %s", candidate_list)
        else:
            data.at[index, "file_loc"] = candidate_list[0]

        logging.debug(f"Candidates for {row['name']}:", candidate_list)
        logging.info(f"Processed {index+1}/{len(data)}")

    logging.debug(f"Done with adding location for file: {csv_file}\nData: {data}")
    return data


if __name__ == "__main__":
    print(process_file("../data/txt/ant/ant-1.3.csv"))
