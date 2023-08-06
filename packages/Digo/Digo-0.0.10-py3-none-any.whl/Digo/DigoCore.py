'''
@Author: YunsangJeong
@Company: Digger
@Digo - Python Logger Module
'''
import requests
import json
import sys
import random
import string
import atexit
import base64

from collections import OrderedDict

from Digo import Project
from Digo import Error
from Digo import Network
from Digo import Utils
from Digo import Singletone

from Digo import ExceptionHandler


class Core():


    DIGO_WEB = 'http://digo.ai:7777/digo-server'


    # def __init__(self, api, project_name):
    #     super().__init__()
    #     self.__user = Project.User(api_key=api)
    #     self.__experiment = Project.Experiment()
    #     self.__project = Project.Project(project_name=project_name)
    #     self.__log: OrderedDict = OrderedDict()
    #     self.__project.name = project_name
    #     self.__step: int = 0
    #     __instance = self
    #     self.login()

    def __init__(self, api, workspace_name, project_name):
        super().__init__()
        self.__user = Project.User(api_key=api)
        self.__experiment = Project.Experiment()
        self.__project = Project.Project(
            project_name=project_name, workspace=workspace_name)
        self.__log: OrderedDict = OrderedDict()
        self.__step: int = 0
        self.login()
        atexit.register(ExceptionHandler.exit_process, self.stateUpdate)

    def send_log(self, log):
        keys = [key for key in log]
        for key in keys:
            value = log[key]
            if type(value) is float:
                log[key] = round(value, 3)

        log["step"] = self.__step
        self.__step += 1
        log_json = json.dumps(log)

        print(log)
        Network.updateLog(api_key=self.__user.api_key, account_id=self.__user.id, project_id=self.__project.id,
                          experiment_id=self.__experiment.id,  log=log_json)

    def printLog(self, log):
        Network.updatePrintLog(api_key=self.__user.api_key, account_id=self.__user.id, project_id=self.__project.id,
                               experiment_id=self.__experiment.id, log=log)

    def send_hyper_parameter(self, hyper_parameter):
        Network.updateHyperParameter(api_key=self.__user.api_key, account_id=self.__user.id, project_id=self.__project.id,
                                     experiment_id=self.__experiment.id, hyper_parameter=hyper_parameter)

    def login(self):
        json_data = Network.login(
            api_key=self.__user.api_key, workspace_name=self.__project.workspace)

        if 'code' not in json_data:
            raise Error.APIInvalidError
            return

        if json_data['code'] == 0:
            self.__user.id = json_data['account_id']
            self.__user.sas_token = json_data['sas_token']
            self.__user.setContainer(json_data['cloud_container_name'])
            print('Login Complete, Welcome {0}'.format(self.__user.id))
            self.create_experiment()
            self.uploadSourceCode()
            self.uploadRequirement()

            
        else:
            # print(json_data)
            raise Error.APIInvalidError

    def create_experiment(self):
        experiment_name: str = Utils.create_experiment_name()

        conn: requests.Response = None

        if self.__project.workspace is None:
            conn = requests.get(self.DIGO_WEB + "/CreateExperiment", params={
                                'api_key': self.__user.api_key, 'account_id': self.__user.id, 'project_name': self.__project.name, 'experiment_name': experiment_name})
        else:
            params = {'api_key': self.__user.api_key, 'account_id': self.__user.id, 'project_name': self.__project.name,
                      'experiment_name': experiment_name, 'workspace_name': self.__project.workspace}
            conn = requests.get(
                self.DIGO_WEB + "/CreateExperiment", params=params)
            # print(params)

        json_data = conn.json()
        # print (json_data)

        if json_data['code'] == 0:
            self.__experiment.id = json_data['experiment_id']
            self.__experiment.name = experiment_name
            self.__project.id = json_data['project_id']
            print("Created Experiment : {0}".format(experiment_name))
        else:
            
            raise Error.FailExperiment

    def uploadSourceCode(self):
        Network.uploadSourceCode(experiment_name=self.__experiment.name,
                                 experiment_id=self.__experiment.id,
                                 project_id=self.__project.id,
                                 sas_token=self.__user.sas_token,
                                 container_name=self.__user.container,
                                 project_name=self.__project.name, api_key=self.__user.api_key, account_id=self.__user.id)

    def uploadRequirement(self):
        Network.uploadRequirementsFile(api_key=self.__user.api_key, account_id=self.__user.id, project_id=self.__project.id,
                                       experiment_id=self.__experiment.id, requirements=Utils.getRequirements())

    def imageLog(self, log):
        Network.uploadImageLog(api_key=self.__user.api_key, account_id=self.__user.id, sas_token=self.__user.sas_token, project_id=self.__project.id,
                               experiment_id=self.__experiment.id, container_name=self.__user.container, project_name=self.__project.name, experiment_name=self.__experiment.name, imageLog=log)

    def uploadModel(self, model_path):
        Network.uploadModelFile(experiment_name=self.__experiment.name,
                                 experiment_id=self.__experiment.id,
                                 project_id=self.__project.id,
                                 sas_token=self.__user.sas_token,
                                 container_name=self.__user.container,
                                 project_name=self.__project.name, api_key=self.__user.api_key, account_id=self.__user.id
                                 ,model_path=model_path)

    def stateUpdate(self, state):
        # state 0 : running, 1 : finished, 2 crashed
        Network.updateExperimentState(api_key=self.__user.api_key, experiment_id=self.__experiment.id, project_id=self.__project.id, account_id=self.__user.id, state=state)

    def upload_test(self, file):
        Network.upload_file_to_main(api_key=self.__user.api_key, account_id=self.__user.id, file=file, file_type = Utils.FILETYPE.IMAGE.name)