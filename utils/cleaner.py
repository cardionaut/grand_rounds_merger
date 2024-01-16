import glob

import pandas as pd
import numpy as np
from loguru import logger


class Cleaner:
    def __init__(self, config) -> None:
        self.input_dir = config.input_dir
        self.rename_dict = config.rename_dict

    def __call__(self) -> pd.DataFrame:
        files = glob.glob(self.input_dir + '/*.csv')

        all_grand_rounds = []
        for file in files[5:6] + files[8:9]:
            logger.debug(file)
            data = pd.read_csv(file)
            while data.columns[0] != 'Name (Originalname)':  # find first row to read
                new_header = data.iloc[0]
                data = data[1:]
                data.columns = new_header
            data = data.rename(columns=self.rename_dict)
            data = data[['name', 'mail', 'duration']]
            data['duration'] = data['duration'].astype(int)
            # TODO: remove nadia mail from host
            
            # TODO: keep first mail per name, but group by name only
            data = data.groupby(['name', 'mail']).sum().reset_index()
            logger.debug(data.head())
            data = data.loc[data['duration'] > 20]
            data['count'] = 1
            all_grand_rounds.append(data)

        complete_data = pd.concat(all_grand_rounds)
        complete_data = complete_data.drop(columns=['duration'])
        complete_data = complete_data.groupby(['name', 'mail']).sum().reset_index()


        logger.debug(complete_data.head())
        logger.debug(complete_data.shape)

    
