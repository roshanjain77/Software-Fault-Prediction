"""Extracting source code"""
import logging
import os
import re
import tarfile
import traceback
import zipfile

import pandas as pd

SOURCE_CODE_FOLDER = "../data/source_code"
CSV_FOLDER = "../data/csv"
PROCESSED_FOLDER = "../data/processed"

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s')


def unzip_files(directory):
    logging.info(f"Unzipping files in {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    try:
                        # path should be same as file name
                        zip_ref.extractall(path=root)
                        logging.info(f"Extracted {file} to {root}")
                    except:
                        logging.error(f"Failed to extract {file}")
                        logging.error(traceback.format_exc())
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
            if re.search(r"\.java$", file) or re.search(r"\.scala$", file):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


def process_file(csv_file):
    data = pd.read_csv(csv_file)

    def remove_extension(file_name):
        return ".".join(file_name.split(".")[:-1])

    software_name, version = remove_extension(csv_file).split("/")[-1].split("-")
    data["file_loc"] = ""
    data["file_loc_non_promissing"] = ""

    logging.info(f"Processing {csv_file}: {software_name}-{version} Adding location of source code")

    file_list = list_all_java_files(SOURCE_CODE_FOLDER)
    potential_list = []
    for file in file_list:
        if software_name in file and version in file:
            potential_list.append(file)

    logging.debug(f"Potential list for {software_name}-{version}:", potential_list)

    missing_files = 0
    nonpromissing_files = 0
    for index, row in data.iterrows():
        file_name = row['name']
        file_name = file_name.replace(".", "/")
        if "scala" in file_name:
            file_name += ".scala"
        else:
            file_name += ".java"

        candidate_list = []
        for file in potential_list:
            if file_name in file and "testcases" not in file:
                candidate_list.append(file)
        if len(candidate_list) > 1:
            logging.error(f"Failed to find {file_name} of {csv_file}")
            logging.error("Candidates: %s", candidate_list)
            missing_files += 1
        elif len(candidate_list) == 1:
            data.at[index, "file_loc"] = candidate_list[0]
        else:
            logging.warning(f"Failed to find {file_name} of {csv_file}, now using unpromissing method")
            short_file_name = file_name.split("/")[-1]
            for file in potential_list:
                if short_file_name in file and "testcases" not in file:
                    candidate_list.append(file)

            if len(candidate_list) == 1:
                logging.warning(f"Found {file_name} of {csv_file} using unpromissing method: {candidate_list}")
                data.at[index, "file_loc_non_promissing"] = candidate_list[0]
                nonpromissing_files += 1
            else:
                logging.error(f"Failed to find {file_name} of {csv_file} using unpromissing method")
                logging.error("Candidates: %s", candidate_list)
                missing_files += 1
        # else:
        #     logging.error(f"Failed to find {file_name} of {csv_file}")
        #     logging.error("Candidates: %s", candidate_list)
        #     missing_files += 1

        logging.debug(f"Candidates for {row['name']}:", candidate_list)
        logging.info(f"Processed {index+1}/{len(data)}")


    for index, rows in data.iterrows():
        if rows["file_loc"]:
            extention = rows["file_loc"].split(".")[-1]
            os.system(f"cp '{rows['file_loc']}' '{PROCESSED_FOLDER}/source_code/{software_name}-{version}-{rows['name']}.{extention}'")
            data.at[index, "file_loc"] = f"{software_name}-{version}-{rows['name']}.{extention}"
        elif rows["file_loc_non_promissing"]:
            extention = rows["file_loc_non_promissing"].split(".")[-1]
            os.system(f"cp '{rows['file_loc_non_promissing']}' '{PROCESSED_FOLDER}/source_code/{software_name}-{version}-{rows['name']}.nonpromissing.{extention}'")
            data.at[index, "file_loc_non_promissing"] = f"{software_name}-{version}-{rows['name']}.nonpromissing.{extention}"


    logging.debug(f"Done with adding location for file: {csv_file}\nData: {data}")
    logging.info(f"Missing files: {missing_files}")
    logging.info(f"Nonpromissing files: {nonpromissing_files}")
    return data


def read_all_csv(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                process_file(file_path).to_csv(PROCESSED_FOLDER + "/" + file, index=False)


if __name__ == "__main__":
    # unzip_files(SOURCE_CODE_FOLDER)
    read_all_csv(CSV_FOLDER)
