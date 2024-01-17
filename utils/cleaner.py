import glob

import pandas as pd
from loguru import logger


class Cleaner:
    def __init__(self, config) -> None:
        self.input_dir = config.input_dir
        self.rename_dict = config.rename_dict
        self.min_duration = config.min_duration

    def __call__(self) -> pd.DataFrame:
        files = glob.glob(self.input_dir + '/*.csv')
        all_grand_rounds = []

        for file in files:
            data = pd.read_csv(file)
            while data.columns[0] != 'Name (Originalname)':  # find first row to read (differs between files)
                new_header = data.iloc[0]
                data = data[1:]  # remove current header row
                data.columns = new_header
            data = data.rename(columns=self.rename_dict)
            data = data[['name', 'mail', 'duration']]  # keep only relevant columns

            # use loc notation to avoid SettingWithCopyWarning
            data.loc[:, 'duration'] = data['duration'].astype(int)
            data.loc[:, 'name'] = data['name'].apply(lambda text: text.partition('(')[0].strip())  # clean names

            data = data.groupby('name', as_index=False).agg({'mail': 'first', 'duration': 'sum'})
            data = data.loc[data['duration'] >= self.min_duration]
            data['credits'] = 1
            all_grand_rounds.append(data)

        complete_data = pd.concat(all_grand_rounds)
        complete_data = complete_data.drop(columns=['duration'])
        complete_data = complete_data.groupby(['name'], as_index=False).agg({'mail': 'first', 'credits': 'sum'})

        # highlight duplicate mails for manual inspection
        complete_data['mail_duplicate'] = complete_data['mail'].duplicated(keep=False)
        complete_data.loc[complete_data['mail'].isna(), 'mail_duplicate'] = False

        return complete_data
