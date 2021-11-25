from tensorflow.keras.models import load_model
from numpy import mean


class BotDetected:
    def __init__(self, model_users='bot_detected/model_users.model',
                 model_data='bot_detected/model_data.model',
                 model_comment='bot_detected/model_comment.model'):
        self.model_users = load_model(model_users)
        self.model_data = load_model(model_data)
        self.model_comment = load_model(model_comment)

    def predict(self, prepared_users, prepared_data, comment_data):
        print('users model:')
        x = prepared_users.drop(['bot', 'user_id'], axis=True)
        x = x.values
        predict_users = self.model_users(x)
        print(predict_users)

        print('data model:')
        x = prepared_data.drop(['bot', 'user_id'], axis=True)
        x = x.values
        predict_data = self.model_data(x)
        print(predict_data)

        print('comment model:')
        x = comment_data.drop(['bot', 'user_id'], axis=True)
        x = x.values
        predict_comment = self.model_comment(x)
        print(predict_comment)

        print('Result: ', 1 if mean([predict_users, predict_data, predict_comment]) > 0.5 else 0)

