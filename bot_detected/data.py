import pandas as pd
from bot_detected.processing import DataProcessing
from bot_detected.predict import BotDetected


class Data:
    def __init__(self, act=None, users=None):
        self.act = pd.DataFrame() if act is None else act
        self.users = pd.DataFrame() if users is None else users

        self.prepared_users = pd.DataFrame()
        self.comment_data = pd.DataFrame()
        self.prepared_data = pd.DataFrame()

    def read_data(self, file_users=None, file_actions=None):
        if file_users is not None and file_actions is not None:
            self.act = pd.read_csv(file_actions).drop('id', axis=1)
            self.users = pd.read_csv(file_users).drop('id', axis=1)

    def data_preparation(self):
        preparation = DataProcessing(self.act, self.users)
        self.prepared_users, self.comment_data, self.prepared_data = preparation.data_processing()

    def save_prepared_data(self, filename_data='prepared_data.csv',
                           filename_comment='comment_data.csv',
                           filename_users='prepare_users.csv'):
        self.prepared_data.to_csv(filename_data, index=False)
        self.comment_data.to_csv(filename_comment, index=False)
        self.prepared_users.to_csv(filename_users, index=False)

    def print(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        print('DATA:')
        print(self.prepared_data)
        print('COMMENT:')
        print(self.comment_data)
        print('INFO:')
        print(self.prepared_users)

    def bot_detected(self):
        pred = BotDetected()
        pred.predict(self.prepared_users, self.prepared_data, self.comment_data)
