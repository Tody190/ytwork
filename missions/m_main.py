# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/6 23:20
"""
import glob
import os.path
import json
import pprint
import shutil
import getpass
import sys
import traceback
import time
import importlib


class MissionsPlanner(object):
    def __init__(self, missions_path):
        """
        mission_paths: str
        """
        #self.mission_center = mission_center.replace("\\", "/")
        self.missions_path = missions_path

        self.backup_path = ""

    def mission_exists(self, mission_name):
        mission_json = self.missions_path + "/" + "*-" + mission_name + ".json"
        all_mission_json = glob.glob(mission_json)
        if all_mission_json:
            return all_mission_json

    def create_missions(self, mission_name, max_retries=3,
                        python_script="", fun_name="", fun_args=[], fun_kwargs={},
                        environment={}):

        """
        :param mission_name: str
        :param expression: Functions executed by Python , eval(expression)
        :param expression_args: Parameters executed by Python, eval(expression)(expression_args)
        :param max_retries: int
        :param accomplished_conditions: list, When the function returns the following results in the list,
        it is considered successful execution, otherwise it is considered a failure
        :param failed_conditions: list, When the function returns the following results in the list,
        it is considered failure execution, otherwise it is considered a successful
        :execute_python: (str, str)， (python script file to execute, function_name)
        environment: dict, environment
        """

        exists_missions = self.mission_exists(mission_name)
        if exists_missions:
            print("Mission already exists: %s" % exists_missions)
            return

        if not os.path.exists(self.missions_path):
            os.makedirs(self.missions_path)

        # # copy python script
        # dst_python_script = self.mission_center + "/" + os.path.basename(self.python_script)
        # shutil.copy(self.python_script, dst_python_script)

        mission_json = self.missions_path + "/" + "waiting-" + mission_name + ".json"

        with open(mission_json, "w") as f:
            obj = {
                "mission_name": mission_name,
                "status": "waiting",
                "python_script": python_script.replace("\\", "/"),
                "fun_name": fun_name,
                "fun_args": fun_args,
                "fun_kwargs": fun_kwargs,
                "environment": environment,
                "max_retries": max_retries,
                "history": []
            }
            f.write(json.dumps(obj, indent=4, ensure_ascii=False))


class Quester(object):
    def __init__(self, missions_path):
        self.missions_path = missions_path.replace("\\", "/")
        self.__current_missions_file = None
        self.__current_missions_data = {}

        self.user_name = getpass.getuser()
        # self.current_failed_missions = []  # Do not execute the wrong task
        # self.executed_missions = []
        self.pass_mission_files = []

        self.__missions_data = {}

    def select_mission_data(self):
        mission_files_glob = glob.glob(self.missions_path + "/waiting-*.json")
        for m_file in mission_files_glob:
            if m_file in self.pass_mission_files:
                continue
            else:
                try:
                    with open(m_file, "r") as f:
                        self.pass_mission_files.append(m_file)
                        self.__current_missions_file = m_file
                        self.__current_missions_data = json.loads(f.read())
                        return self.__current_missions_data
                except Exception as e:
                    print(e)

    def __write_mission_data(self, **kwargs):
        self.__current_missions_data.update(kwargs)

        if os.path.exists(self.__current_missions_file):
            with open(self.__current_missions_file, "w") as f:
                f.write(json.dumps(self.__current_missions_data,
                                   indent=4,
                                   ensure_ascii=False))

    def __write_execution_result(self, status, result):
        history_data = {"quester": self.user_name,
                        "result": str(result),
                        "index": len(self.__current_missions_data["history"]) + 1}
        self.__current_missions_data["history"].append(history_data)

        self.__write_mission_data(status=status,
                                  result=result,
                                  history=self.__current_missions_data["history"])

    def rename_mission_file(self, status):
        old_file = self.__current_missions_file
        mission_path = os.path.dirname(old_file)
        mission_file_name = os.path.basename(old_file)
        mission_file_name_no_status = mission_file_name.split("-", 1)[-1]

        new_mission_file_name = status + "-" + mission_file_name_no_status
        new_file = mission_path + "/" + new_mission_file_name

        os.rename(old_file, new_file)
        self.__current_missions_file = new_file
        print(self.__current_missions_file)

    def execute_mission(self, missions_data):
        # set env
        for k, v in missions_data["environment"].items():
            os.environ[k] = str(v)

        python_script = missions_data["python_script"]
        function_name = missions_data["fun_name"]
        fun_args = missions_data["fun_args"]
        fun_kwargs = missions_data["fun_kwargs"]

        try:
            sys.path.insert(0, os.path.dirname(python_script))
            module_name = os.path.splitext(os.path.basename(python_script))[0]
            # import model
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            if fun_args:
                results = function(*fun_args)
            elif fun_kwargs:
                results = function(**fun_kwargs)
            else:
                results = function()
            self.__write_execution_result("accomplished", results)
            return True
        except:
            print(traceback.format_exc())
            self.__write_execution_result("failed", traceback.format_exc())
            return False

    def start_mission(self):
        while True:
            mission_data = self.select_mission_data()
            if not mission_data:
                return

            try:
                #  write data
                self.__write_mission_data(quester=self.user_name,
                                          status="executing")

                # Change the JSON name to executing to prevent other machines from taking on tasks
                self.rename_mission_file("executing")

                # exe data
                execute_accomplished = self.execute_mission(mission_data)

                # rename file
                if execute_accomplished:
                    self.rename_mission_file("accomplished")
                else:
                    self.rename_mission_file("waiting")

            except Exception as e:
                print(e)

