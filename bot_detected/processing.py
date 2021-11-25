from enum import Enum
import pandas as pd
import numpy as np
import re
import difflib


class CommentProcessing:
    @staticmethod
    def list_len_comment(list_comment):
        return [len(x) for x in list_comment]

    @staticmethod
    def count_diff_layouts(list_comment):
        pattern = r'([а-я]*[a-z0-9]+[а-я]+[a-z]?)+'
        return sum([len(re.findall(pattern, comment.lower())) for comment in list_comment])

    @staticmethod
    def count_comments_with_diff_layouts(list_comment):
        pattern = r'([а-я]*[a-z0-9]+[а-я]+[a-z]?)+'
        return len([comment for comment in list_comment if len(re.findall(pattern, comment.lower()))])

    @staticmethod
    def count_diff_comments(list_comment):
        return len(set(list_comment))

    @staticmethod
    def count_cliched_words(list_comment):
        pattern = r'(((супер)|(крут)|(восхитительн)|(отличн)|(хорош)|(класс))\w*)|(сам\w{2}\W)|(очень)'
        return sum([len(re.findall(pattern, comment.lower())) for comment in list_comment])

    @staticmethod
    def count_comments_with_cliched(list_comment):
        pattern = r'(((супер)|(крут)|(восхитительн)|(отличн)|(хорош)|(класс))\w*)|(сам\w{2}\W)|(очень)'
        return len([comment for comment in list_comment if len(re.findall(pattern, comment.lower()))])

    @staticmethod
    def compare_comments(list_comment):
        list_compare = [difflib.SequenceMatcher(None, s1, s2).ratio()
                        for i1, s1 in enumerate(list_comment) for i2, s2 in enumerate(list_comment[i1 + 1:])
                        if (abs(len(s1.split()) - len(s2.split())) <= 4)]
        return np.mean(list_compare) if len(list_compare) else 0


class DataProcessing:
    class Act(Enum):
        COMMENT = 1
        DOWNLOAD = 2
        RATING = 3
        RUN = 4
        STOP = 5

    action_type = {
        Act.COMMENT.value: 'comment',
        Act.DOWNLOAD.value: 'download',
        Act.RATING.value: 'rating',
        Act.RUN.value: 'run',
        Act.STOP.value: 'stop'
    }

    def __init__(self, act, users):
        self.act = act.copy()
        self.users = users.copy()

        self.data = pd.DataFrame()
        self.data['user_id'] = self.users.user_id
        self.data['bot'] = self.users.bot

        self.comment_data = pd.DataFrame()
        self.comment_data['user_id'] = self.users.user_id
        self.comment_data['bot'] = self.users.bot

    def data_processing(self):
        self.basic_act_processing()
        self.basic_users_processing()
        self.comment_processing()
        self.count_actions()
        self.count_app_iter()
        self.count_active_days()
        self.rating_mean()
        self.mean_act_per_day()
        self.act_without_run_or_download()
        self.counting_mean_working_hours()
        self.fill_nan()
        return self.users, self.comment_data, self.data

    def basic_act_processing(self):
        self.act.rename(columns={'date': 'full_date'}, inplace=True)
        self.act['full_date'] = pd.to_datetime(self.act['full_date'])
        self.act['time'] = self.act['full_date'].dt.time
        self.act['date'] = self.act['full_date'].dt.date
        self.act.fillna({'data': ''}, inplace=True)

    def basic_users_processing(self):
        self.users.gender.fillna(1, inplace=True)
        self.users.fillna(False, inplace=True)
        self.users['img_url'] = self.users.img_url.apply(lambda x: 1 if x else 0)
        self.users['second_mail'] = self.users.second_mail.apply(lambda x: 1 if x else 0)
        self.users['cards'] = self.users.cards.apply(lambda x: 1 if x else 0)
        self.users['phone'] = self.users.phone.apply(lambda x: 1 if x else 0)
        self.users.replace({'gender': {'m': 1, 'w': 0, 'f': 0}}, inplace=True)
        self.users.drop('id', axis=True, inplace=True)

    def comment_processing(self):
        processing = CommentProcessing()
        comment_data = self.act[self.act.action_type == DataProcessing.Act.COMMENT.value][['user_id', 'data']]\
            .groupby('user_id')\
            .agg(list)\
            .reset_index()\
            .rename(columns={'data': 'list_comment'})
        comment_data['cnt_comment'] = comment_data.list_comment.apply(lambda x: len(x))
        comment_data['list_len_comment'] = comment_data.list_comment.apply(processing.list_len_comment)

        comment_data['mean_len_comment'] = comment_data.list_len_comment.apply(lambda x: sum(x) / len(x))
        comment_data['min_len_comment'] = comment_data.list_len_comment.apply(lambda x: min(x))
        comment_data['max_len_comment'] = comment_data.list_len_comment.apply(lambda x: max(x))

        comment_data['cnt_diff_layouts'] = comment_data.list_comment.apply(processing.count_diff_layouts)
        comment_data['cnt_comments_with_diff_layouts'] = comment_data.list_comment \
            .apply(processing.count_comments_with_diff_layouts)
        comment_data['percent_comments_with_diff_layouts'] = comment_data.cnt_comments_with_diff_layouts / \
                                                             comment_data.list_comment.apply(lambda x: len(x))

        comment_data['cnt_cliched_words'] = comment_data.list_comment.apply(processing.count_cliched_words)
        comment_data['cnt_comments_with_cliched'] = comment_data.list_comment \
            .apply(processing.count_comments_with_cliched)
        comment_data['percent_comments_with_cliched'] = comment_data.cnt_comments_with_cliched / \
                                                        comment_data.list_comment.apply(lambda x: len(x))

        comment_data['cnt_different_comments'] = comment_data.list_comment.apply(processing.count_diff_comments)
        comment_data['percent_diff_comments'] = comment_data.cnt_different_comments / \
                                                comment_data.list_comment.apply(lambda x: len(x))

        comment_data['mean_similarity_comments'] = comment_data.list_comment.apply(processing.compare_comments)

        comment_data.drop(['cnt_comments_with_cliched', 'cnt_comments_with_diff_layouts',
                           'cnt_different_comments', 'list_len_comment', 'list_comment'], axis=1, inplace=True)

        self.comment_data = self.comment_data.merge(comment_data, how='left')

    def count_actions(self):
        def count_parameter(act_type):
            return self.act[self.act.action_type == act_type].groupby('user_id') \
                .agg({'date': 'count', 'app_id': 'nunique'}) \
                .reset_index() \
                .rename(columns={'date': 'cnt_' + DataProcessing.action_type[act_type],
                                 'app_id': 'cnt_uniq_' + DataProcessing.action_type[act_type]})

        self.data = self.data.merge(count_parameter(DataProcessing.Act.COMMENT.value), how='left') \
            .merge(count_parameter(DataProcessing.Act.RATING.value), how='left') \
            .merge(count_parameter(DataProcessing.Act.RUN.value), how='left') \
            .merge(count_parameter(DataProcessing.Act.DOWNLOAD.value), how='left')
        self.data.drop('cnt_uniq_download', axis=1, inplace=True)

    def count_app_iter(self):
        self.data = self.data.merge(self.act.groupby('user_id')
                                    .agg({'app_id': 'nunique'})
                                    .reset_index()
                                    .rename(columns={'app_id': 'cnt_app_iter'}), how='left')

    def count_active_days(self):
        self.data = self.data.merge(self.act.groupby('user_id')
                                    .agg({'date': 'nunique'})
                                    .reset_index()
                                    .rename(columns={'date': 'cnt_active_days'}),
                                    how='left')

    def rating_mean(self):
        self.data = self.data.merge(self.act[self.act.action_type == DataProcessing.Act.RATING.value]
                                      .astype({'data': np.float32})
                                      .groupby('user_id')
                                      .agg({'data': 'mean'})
                                      .reset_index()
                                      .rename(columns={'data': 'rating_mean'}),
                                      how='left')

    def mean_act_per_day(self):
        data_by_date = self.act.groupby(['user_id', 'date']).agg({'action_type': list}).reset_index()

        data_by_date['count_comment'] = data_by_date.action_type \
            .apply(lambda type_act: len([x for x in type_act if x == DataProcessing.Act.COMMENT.value]))
        data_by_date['count_rating'] = data_by_date.action_type \
            .apply(lambda type_act: len([x for x in type_act if x == DataProcessing.Act.RATING.value]))
        data_by_date['count_download'] = data_by_date.action_type \
            .apply(lambda type_act: len([x for x in type_act if x == DataProcessing.Act.DOWNLOAD.value]))
        data_by_date['count_run'] = data_by_date.action_type \
            .apply(lambda type_act: len([x for x in type_act if x == DataProcessing.Act.RUN.value]))

        data_by_date = data_by_date.groupby('user_id').mean().reset_index() \
            .rename(columns={'count_comment': 'mean_comment_per_day',
                             'count_rating': 'mean_rating_per_day',
                             'count_download': 'mean_download_per_day',
                             'count_run': 'mean_run_per_day'})

        self.data = self.data.merge(data_by_date, how='left')

    def act_without_run_or_download(self):
        info_set_app = self.act[(self.act.action_type == DataProcessing.Act.COMMENT.value) |
                                (self.act.action_type == DataProcessing.Act.RATING.value)] \
            .groupby('user_id') \
            .agg({'app_id': set}) \
            .reset_index() \
            .rename(columns={'app_id': 'comm_and_rat_set'})

        info_set_app = info_set_app.merge(self.act[(self.act.action_type == DataProcessing.Act.DOWNLOAD.value)]
                                          .groupby('user_id')
                                          .agg({'app_id': set})
                                          .reset_index()
                                          .rename(columns={'app_id': 'download_set'})
                                          , how='left')

        info_set_app = info_set_app.merge(self.act[(self.act.action_type == DataProcessing.Act.RUN.value)]
                                          .groupby('user_id')
                                          .agg({'app_id': set})
                                          .reset_index()
                                          .rename(columns={'app_id': 'run_set'})
                                          , how='left')

        info_set_app['comm_and_rat_set'] = info_set_app.comm_and_rat_set.apply(lambda x: set() if pd.isnull(x) else x)
        info_set_app['download_set'] = info_set_app.download_set.apply(lambda x: set() if pd.isnull(x) else x)
        info_set_app['run_set'] = info_set_app.run_set.apply(lambda x: set() if pd.isnull(x) else x)

        info_set_app['list_download_without_run'] = info_set_app.download_set - info_set_app.run_set
        info_set_app['list_not_download'] = info_set_app.comm_and_rat_set - info_set_app.download_set
        info_set_app['list_not_run'] = info_set_app.comm_and_rat_set - info_set_app.run_set

        info_set_app['cnt_download_without_run'] = info_set_app.list_download_without_run.apply(lambda x: len(x))
        info_set_app['cnt_act_without_download'] = info_set_app.list_not_download.apply(lambda x: len(x))
        info_set_app['cnt_act_without_run'] = info_set_app.list_not_run.apply(lambda x: len(x))

        self.data = self.data.merge(info_set_app[['user_id',
                                                  'cnt_download_without_run',
                                                  'cnt_act_without_download',
                                                  'cnt_act_without_run']],
                                    how='left')

    def counting_mean_working_hours(self):
        def mean_worktime(tuple_act):
            diff_time = []
            for act in tuple_act:
                while act:
                    if len(act) < 2:
                        break
                    run, stop, *act = act
                    if run[1] == DataProcessing.Act.RUN.value \
                            and stop[1] == DataProcessing.Act.STOP.value:
                        diff_time.append((stop[2] - run[2]).total_seconds())
                    elif (run[1] == stop[1] == DataProcessing.Act.RUN.value) \
                            or (run[1] == DataProcessing.Act.STOP.value):
                        act = list([stop]) + act

            if len(diff_time):
                return np.mean(diff_time) / 60
            else:
                return 0

        run_stop_data = self.act[(self.act.action_type == DataProcessing.Act.RUN.value)
                                 | (self.act.action_type == DataProcessing.Act.STOP.value)]
        run_stop_data = run_stop_data[['user_id', 'app_id', 'action_type', 'full_date']]
        run_stop_data['tuple'] = run_stop_data[['app_id', 'action_type', 'full_date']].values.tolist()
        run_stop_data = run_stop_data.groupby(['user_id', 'app_id'])\
            .agg({'tuple': list})\
            .reset_index() \
            .groupby('user_id')\
            .agg({'tuple': list})\
            .reset_index()
        run_stop_data['mean_worktime'] = run_stop_data.tuple.apply(mean_worktime)

        self.data = self.data.merge(run_stop_data[['user_id', 'mean_worktime']], how='left')

    def fill_nan(self):
        self.comment_data['percent_diff_comments'].fillna(1, inplace=True)
        self.comment_data.fillna(0, inplace=True)
        self.data.fillna(0, inplace=True)
