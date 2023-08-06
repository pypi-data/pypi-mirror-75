import allure
import pandas as pd
import time, os
import logging
# from matplotlib import pyplot as plt
# import numpy as np
# import seaborn as sn
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.token_json import UserToken
from toolkit_w.internal.vars_global import ProblemType, TargetMetric, FeatureType
from toolkit_w.internal.vars_global import InterpretabilityLevel as Interpt
from toolkit_w.resources.auth import authenticate
import toolkit_w as my_toolkit

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

#############################
########    SDK      ########
#############################
#############################
###    Functionality      ###
#############################

class MyWhatify:
    #############################
    #######    API's      #######
    #############################
    user_token = None

    def __init__(self):
        pass

    def authenticate(self, username, password):
        self.login(email=username,password=password)

    def login(self, email, password):
        with allure.step('login with user: ' + str(email)):
            logging.info('login with user: ' + str(email))  # + ' and password: ' + password)
            authenticate(username=email, password=password)
            self.user_token = UserToken(my_toolkit.token)
            print("{} - Login successful".format(str(email)))

    def mark_ensemble_in_production(self, ensemble_id, mark_production=True):
        with allure.step('setting ensemble_id: ' + str(ensemble_id) + ' as in production: ' + str(mark_production)):
            logging.info('setting ensemble_id: ' + str(ensemble_id) + ' as in production: ' + str(mark_production))
            if mark_production:
                my_toolkit.Ensemble.set_ensemble_in_production(ensemble_id=ensemble_id)
            else:
                my_toolkit.Ensemble.remove_ensemble_in_production(ensemble_id=ensemble_id)


    def run_prediction(self, data_name, ensemble_id, data_file=None, wait=True, file_path=None, header=None, data_id=None):
        with allure.step('running prediction on data name: ' + data_name + ' with ensemble id: ' + str(ensemble_id) + ' and wait is: ' + str(wait)):
            print('running prediction on data name: ' + data_name + ' with ensemble id: ' + str(ensemble_id) + ' and wait is: ' + str(wait))
            logging.info('running prediction on data name: ' + data_name + ' with ensemble id: ' + str(ensemble_id) + ' and wait is: ' + str(wait))
            status = True
            predict_id = None
            message = None
            # data_file.drop(data_file.columns[len(df.columns) - 1], axis=1, inplace=True)
            try:
                if not (file_path or data_id):
                    data_id = my_toolkit.Datasource.create_from_dataframe(df=data_file, data_source_name=data_name,
                                                                       wait=True, skip_if_exists=True)['id']
                predict_id = my_toolkit.Prediction.create(ensemble_id=ensemble_id, data_id=data_id, data_name=data_name,
                                                       file_path=file_path, header=header, wait=wait)['id']
            except Exception as ex:
                message = ex.args
                status = False
        return predict_id, status, message

    def upload_data_file(self, data_file, data_name, wait=True, skip_if_exists=True, na_values=None):
        with allure.step('uploading csv name: ' + data_name + ' with wait= ' + str(wait) +
                     ' and skip if exist= ' + str(skip_if_exists)):
            source_id = -1
            try:
                source_id = my_toolkit.Datasource.create_from_dataframe(df=data_file,
                                                                     data_source_name=data_name,
                                                                     wait=wait, skip_if_exists=skip_if_exists,
                                                                     na_values=na_values)['id']
                print("\nYour Source ID for {} is: {}".format(data_name, source_id))
            except Exception as e:
                print(e)
        return source_id

    def preparing_data_set(self, source_id, data_set_name, sample_id=['car_id'],
                           retype_columns={'car_id': FeatureType.CATEGORICAL}, target='class',
                           problem_type=ProblemType.CLASSIFICATION, wait=True):
        with allure.step('Preparing Dataset name: ' + str(data_set_name) + ' source_id= ' + str(source_id) +
                     ' problem_type: ' + str(problem_type) + ' target: ' + str(target) + ' wait: ' + str(wait)):
            dataset_id = -1
            # task_type = eval(problem_type.value)

            try:
                dataset_id = my_toolkit.resources.Datasource.prepare_data(
                    datasource_id=source_id,
                    dataset_name=data_set_name,
                    target=target,
                    problem_type=problem_type,
                    sample_id=sample_id,
                    retype_columns=retype_columns,
                    wait=wait, skip_if_exists=True)['id']
                print("Dataset {} id is {}".format(data_set_name, dataset_id))
            except Exception as e:
                logging.exception('failed preparing data set' + data_set_name +' got error: ' + e)
        return dataset_id

    def create_data_set(self, source_id, data_set_name, problem_type=ProblemType.CLASSIFICATION, target='class',
                        not_used=None, na_values=None, skip_if_exists=True, wait=True):
        with allure.step('Preparing Dataset name: ' + str(data_set_name) + ' source_id= ' + str(source_id) +
                     ' problem_type: ' + str(problem_type) + ' target: ' + str(target) + ' wait: ' + str(wait)):
            dataset_id = -1
            task_type = eval(problem_type.value)

            try:
                dataset_id = my_toolkit.Dataset.create(datasource_id=source_id, dataset_name=data_set_name,
                                    problem_type=task_type,
                                    target=target, not_used=not_used, na_values=na_values,
                                    skip_if_exists=skip_if_exists, wait=True)['id']
                print("Dataset {} id is {}".format(data_set_name, dataset_id))
            except Exception as e:
                logging.exception('failed creating data set' + data_set_name +' got error: ' + e)
        return dataset_id

    def train_model(self, data_name, dataset_id, target_metric=TargetMetric.RECALL_MACRO, training_time_in_minutes=6,
                    cv_folds=3, ensemble_size=5, interpt_level=Interpt.EXPLAINABLE):
        with allure.step('On data_name: ' + data_name + ' ID: ' + str(dataset_id) +
                     ' training a model with target_metric: ' + str(target_metric.value) +
                     ' cv_folds: ' + str(cv_folds) + ' ensemble_size: ' + str(ensemble_size) +
                     ' interpt_level: ' + str(interpt_level) + ' training_time_in_minutes:' + str(training_time_in_minutes)):
            task_id = None
            ret_dict = None
            # target_metric_eval = eval(target_metric.value)
            # @markdown * Allocate training time
            # Training_time_in_minutes = training_time_in_minutes  # @param {type:'number'}

            # @markdown * Data partitioning
            # @markdown * Hold-out // Cross-Validation

            pipeline = self.get_pipeline_estimators_list(dataset_id, True, interpt_level)
            estimators = self.get_pipeline_estimators_list(dataset_id, False, interpt_level)
            if interpt_level == Interpt.EXPLAINABLE:
                interpretability_level = my_toolkit.enums.InterpretabilityLevel.EXPLAINABLE
            else:
                interpretability_level = my_toolkit.enums.InterpretabilityLevel.PRECISE

            # print('The training time is:', Training_time_in_minutes)
            # print ('The selected Target Metric is:', Target_metric.value)

            try:
                task = my_toolkit.Dataset.train(
                    task_name=data_name + " " + interpretability_level.name,
                    estimators=estimators,
                    pipeline=pipeline,
                    target_metric=target_metric,
                    dataset_id=dataset_id,
                    # splitting_strategy=firefly.enums.SplittingStrategy.STRATIFIED,
                    notes='created from Automation, run minutes: ' + str(training_time_in_minutes),
                    ensemble_size=ensemble_size,
                    n_folds=cv_folds,
                    max_models_num=None,
                    interpretability_level=interpretability_level,
                    timeout=training_time_in_minutes * 60, wait=True, skip_if_exists=True
                )
                task_id = task['id']
                ret_dict = task.to_dict()
            except Exception as e:
                logging.exception('Failed to train model on data_name: ' + str(data_name) + ' dataset_id: ' + str(dataset_id) +
                                  ' target_metric_eval ' + str(target_metric_eval) + 'in Time: ' +
                                  str(training_time_in_minutes) + ' interpretability_level ' + str(interpretability_level))
        return task_id, ret_dict

    def model_sensitivity_report(self, ensemble_id, alg='Permutation', max_iteration=10):
        logging.info('running model sensitivity report for ensemble_id: ' + str(ensemble_id) + ' alg: ' + str(alg) +
                     ' max iter: ' + str(max_iteration))
        df = pd.DataFrame()
        n = 4
        # alg = 'Permutation'  # @param['Permutation', 'NA value']

        sens = None

        while max_iteration > 0:
            max_iteration = max_iteration - 1
            try:
                sens = my_toolkit.Ensemble.get_model_sensitivity_report(id=ensemble_id)
                if sens is not None:
                    break
                time.sleep(5)
            except Exception as e:
                print(e)
                break

        return sens[alg]

    def delete_data_source(self, data_id):
        logging.info('deleting data Source data_id: ' + str(data_id))
        my_toolkit.Datasource.delete(data_id)

    def delete_data_set(self, data_id):
        logging.info('deleting dataset data_id: ' + str(data_id))
        my_toolkit.Dataset.delete(data_id)

    def delete_task(self, task_id):
        logging.info('deleting task_id: ' + str(task_id))
        my_toolkit.Task.delete(task_id)

    # def delete_user(self, email=None, password=None, delete_user_id=None):
    #     with allure.step('Marking user email ' + str(email) + ' or user_id:' + str(delete_user_id) + ' as Deleted in the DB with API'):
    #         logging.info('deleting user email: ' + str(email))
    #         if not delete_user_id:
    #             self.login(email=email, password=password)
    #             delete_user_id = self.user_token.get_user_id()
    #
    #         if delete_user_id:
    #             self.login(email=vars_global.Users.AUTO_QA_ADMIN.get_email(), password=vars_global.Users.AUTO_QA_ADMIN.get_password())
    #             #TODO move to test
    #             # self.umClient = UMClient(host=conf_server['USERM_HOST'], port=conf_server['USERM_PORT'])  # , use_https=True)
    #             # self.umClient.delete_user(jwt=self.user_token.get_token(), user_id=delete_user_id)

    #############################
    ###        Gettrs         ###
    #############################
    def get_api_post(self, url, api_key=None):
        return APIRequestor().post(url=url, api_key=api_key)

    def get_data_source(self, data_name):
        logging.info('getting the DataSource list for data_name: ' + str(data_name))
        return my_toolkit.Datasource.list(search_term=data_name)['hits']

    def get_data_source_list(self, len=10):
        with allure.step('getting the DataSource list with len: ' + str(len)):
            list_sources = my_toolkit.Datasource.list()
            sources = pd.DataFrame(list_sources['hits'])

        return sources[['creation_date', 'data_size', 'id', 'name', 'row_count', 'state', ]].head(len)

    def get_data_set(self, data_name):
        logging.info('getting the DataSet list for data_name: ' + str(data_name))
        return my_toolkit.Dataset.list(search_term=data_name)['hits']

    def get_datasets_list(self, len=10):
        with allure.step('getting the Dataset list with len: ' + str(len)):
            list_datasets = my_toolkit.Dataset.list()
            datasets = pd.DataFrame(list_datasets['hits'])
            datasets.set_index('creation_date')
        return datasets[['creation_date', 'id', 'name', 'problem_type', 'row_count', 'state']].head(len)

    def get_tasks(self, data_name):
        logging.info('getting the Tasks list for data_name: ' + str(data_name))
        return my_toolkit.Task.list(search_term=data_name)['hits']

    def get_tasks_list(self, len=10):
        with allure.step('getting the tasks list with len: ' + str(len)):
            list_tasks = my_toolkit.Task.list()
            tasks = pd.DataFrame(list_tasks['hits'])

            tasks.columns
        return tasks[['creation_date', 'dataset_id', 'name', 'notes', 'problem_type',
               'state', 'target_metric']].head(len)

    def get_ensemble_list(self, task_id):
        with allure.step('getting the Ensemble list for task ID: ' + str(task_id)):
            # get list of ensembles
            return my_toolkit.Ensemble.list(filter_={'task_id': [task_id], 'stage': ['TASK', 'REFIT']})['hits']

    def get_data_file(self, data_name='car_sdk_demo.csv'):
        with allure.step('getting csv from data file for data_name: ' + str(data_name)):
            script_dir = os.path.dirname(__file__)
            path = os.path.join(script_dir, '../data_source/')
            # path = "https://raw.githubusercontent.com/NeuralAlgorithms/firefly-python-sdk/master/examples/"
        return pd.read_csv(path + data_name)

    def get_created_data_file(self, data_name='temp.csv'):
        df_data = self.get_data_file(data_name='car_sdk_demo_test_no.csv')
        data = df_data.get_values()
        script_dir = os.path.dirname(__file__)
        path = os.path.join(script_dir, '../data_source/') + data_name
        with open(path, 'a') as f:
            f.write('car_id,buying,maint,doors,persons,lug_boot,junk_feature,safety')
            for i in range(1):
                for row in data:
                    text = ''
                    for index in range(row.__len__()):
                        text += str(row.tolist().pop(index)) + ","
                    f.write('\n' + text[:-1])
            f.close()

    def get_data_file_s3(self, data_name='car_sdk_demo.csv'):
        logging.info('getting csv from data file for data_name: ' + str(data_name))
        script_dir = os.path.dirname(__file__)
        path = os.path.join(script_dir, '../data_source/')
        path = "s3://firefly-automation/whatify_demo/"
        # path = "https://raw.githubusercontent.com/NeuralAlgorithms/firefly-python-sdk/master/examples/"
        return pd.read_csv(path + data_name)

    def get_pipeline_list(self, dataset_id, interpt_level=Interpt.PRECISE):
        return self.get_pipeline_estimators_list(dataset_id, True, interpt_level)

    def get_pipeline_estimators_list(self, dataset_id, interpt_level=Interpt.PRECISE):
        return self.get_pipeline_estimators_list(dataset_id, False, interpt_level)

    def get_pipeline_estimators_list(self, dataset_id, is_pipeline=True, interpt_level=Interpt.PRECISE):
        with allure.step('getting the Dataset pipeline or estimators list for dataset_id: ' + str(dataset_id)
                     + ' is_pipeline: ' + str(is_pipeline) + ' interpt_level: ' + str(interpt_level)):
            ret_list = None
            if is_pipeline:
                ret_list = my_toolkit.Dataset.get_available_pipeline(inter_level=interpt_level, id=dataset_id)
            else:
                ret_list = my_toolkit.Dataset.get_available_estimators(inter_level=interpt_level, id=dataset_id)
        return ret_list

    def get_prediction(self, predict_id, len=10):
        with allure.step('getting prediction list for predict_id: ' + str(predict_id) + ' len: ' + str(len)):
            ret_prediction = None
            predict_results = my_toolkit.Prediction.get(predict_id)

            download_url = predict_results['result_path']

            if download_url is not None:
                df_predict = pd.read_csv(download_url)
                ret_prediction = df_predict.head(len)
        return ret_prediction

    def get_prediction_error(self, predict_id):
        with allure.step('getting prediction list for predict_id: ' + str(predict_id) + ' len: ' + str(len)):
            error_message = None
            predict_results = my_toolkit.Prediction.get(predict_id)
            error_message = predict_results['error_message']
        return error_message

    def get_wisdom_list(self):
        with allure.step('getting wisdom list'):
            my_list = my_toolkit.Wisdom.get_wisdom_list_with_demo()
            len1 = len(my_list)
        return my_list

    # def get_task_result_Tom(self):
    #     #todo delete fun
    #     self.login(email=vars_global.Users.AUTO_QA007.get_email(),
    #                password=vars_global.Users.AUTO_QA007.get_password())
    #
    #     task_id = 138637
    #     task_id_older = 138630
    #     jwt = self.user_token.get_token()
    #     self.halClient = HalClient(host=conf_server['HAL_HOST'], port=conf_server['HAL_PORT'], use_https=True)
    #     self.report_client = ReportsClient(host=conf_server['REPORT_HOST'], port=conf_server['REPORT_PORT'])
    #     for index in range(99):
    #         try:
    #             if index % 3:
    #                 task_result = HalClient(host=conf_server['HAL_HOST'], port=conf_server['HAL_PORT'], use_https=True).get_task_result(jwt=jwt, task_id=task_id)
    #             if index % 2:
    #                 sensitivity_result = ReportsClient(host=conf_server['REPORT_HOST'], port=conf_server['REPORT_PORT']).get_model_sensitivity(jwt=jwt, ensemble_id=task_id)
    #         except:
    #             pass
    #     print('dddd')



    #############################
    ###      Validation       ###
    #############################
