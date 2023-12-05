import logging
import os

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')



class Dataset:

    def __init__(self, data_dir, source_code_dir, generate_dataset=False, generate_loc=None) -> None:

        logging.debug("Initializing Dataset")

        self.data_dir = data_dir
        self.source_code_dir = source_code_dir
        self.csv_files = self.__find_all_csv()

        logging.info("Found {} csv files".format(len(self.csv_files)))
        logging.debug("csv files: {}".format(self.csv_files))

        if generate_dataset and generate_loc:
            self.generate_loc = generate_loc
            if not os.path.exists(self.generate_loc):
                os.mkdir(self.generate_loc)
            self.__generate_dataset()

    def __find_all_csv(self):
        csv_files = []
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith(".csv"):
                    csv_files.append(os.path.join(root, file))
        return csv_files

    def __generate_dataset(self):
        logging.info("Generating Complete dataset")
        for csv_file in self.csv_files:
            self._generate_dataset_from_csv(csv_file)

    def _generate_dataset_from_csv(self, csv_file):
        logging.info("Generating dataset from {}".format(csv_file))
        df = pd.read_csv(csv_file)
        df['source_code'] = df.apply(lambda x: self.__get_source_code(x.file_loc, x.file_loc_non_promissing), axis=1)
        df['original_file_loc'] = df.apply(lambda x: type(x.file_loc) != float, axis=1)
        df.drop(['file_loc', 'file_loc_non_promissing'], axis=1, inplace=True)

        new_file_name = os.path.join(self.generate_loc, os.path.basename(csv_file) + ".with_code.csv")
        df.to_csv(new_file_name, index=False)
        logging.info("Generated dataset for {} saved to {}".format(csv_file, new_file_name))

    def __get_source_code(self, file_loc, second_file_loc):

        logging.debug("Getting source code from {}, {}".format(file_loc, second_file_loc))

        code_path = file_loc
        if type(file_loc) == float:
            if type(second_file_loc) == float:
                return ""
            code_path = second_file_loc

        file_path = os.path.join(self.source_code_dir, code_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError as e:
            logging.warning(f"UnicodeDecodeError: {e}")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        return content


if __name__ == "__main__":
    data_dir = "data"
    source_code_dir = "data/source_code"
    dataset = Dataset(data_dir, source_code_dir, generate_dataset=True, generate_loc="data/with_code")

