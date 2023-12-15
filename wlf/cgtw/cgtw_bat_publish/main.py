# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/11/12
"""
一件提交所有与 pub 标识开头的提交框
文件必须符合命名规范，且在提交目录底下
如果获取不到文件，会提供用户手动提交的方式
"""

import pprint
import sys
import os
import traceback
import copy
import threading

__file__ = r"C:\CgTeamWork_v6.2\bin\ext_plugin\Cgtw_Bat_Publish\main.py"
CGTW_ROOT_BIN = __file__.replace(u"\\", u"/").split(u"ext_plugin")[0]
for _path in [
    CGTW_ROOT_BIN + u"base",
    CGTW_ROOT_BIN + u"lib/pyside",
    CGTW_ROOT_BIN + u"cgtw",
    CGTW_ROOT_BIN + u"base/com_lib",
    CGTW_ROOT_BIN + u"base/com_icon"
]:
    _path in sys.path or sys.path.append(_path)

# pyside
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

QtWidgets.QApplication.addLibraryPath(CGTW_ROOT_BIN + u"lib/pyside/PySide2/plugins/")

import cgtw2
import ct_lib
from ctlib import file as ct_file


class VersionFilesInfo():
    """获取任务相关数据 名称 文件版本等"""

    def __init__(self, a_tw, a_database, a_module, a_module_type, a_id_list, a_filebox_id, a_func):
        self.m_id_list = a_id_list
        self.m_module = a_module
        self.m_database = a_database
        self.m_module_type = a_module_type
        self.m_func = a_func
        self.m_filebox_id = a_filebox_id
        self.m_tw = a_tw

    def get(self):
        t_error = ''
        for _id in self.m_id_list:
            # -link_entity
            t_link_entity = self.get_link_entity(_id)
            if t_link_entity == False:
                t_error += u'ID:{} 获取link entity名称失败'.format(_id)
                continue
            # -get filebox info
            try:
                t_filebox_data = self.m_func.get_filebox(self.m_database, self.m_module, _id, self.m_filebox_id)
                if not isinstance(t_filebox_data, dict) or t_filebox_data == {}:
                    t_error += u'记录:{} id:{} 获取文件框数据失败\n'.format(t_link_entity, _id)
                    continue

                t_version_type = t_filebox_data['version_type']
                t_max_version = t_filebox_data['last_max_version']  # 20210702 防止多任务
                t_rule_list = t_filebox_data['rule_view']
                t_filebox_path = t_filebox_data['path']
                t_version_length = int(t_filebox_data['version_length'])
                if t_max_version == '':
                    t_max_version = '0' * t_version_length
                # 20200721 新增跟随版本
                t_is_follow = t_filebox_data['is_follow'].lower().strip()
                t_follow_version = t_filebox_data['follow_version']
                t_follow_title = t_filebox_data['follow_title']
                if t_follow_version != '':
                    t_follow_version = str(int(t_follow_version)).zfill(t_version_length)

            except Exception as error:
                t_error += u'记录:{} id:{} 获取文件框数据失败:{}\n'.format(t_link_entity, _id, error)
                continue

            # -get version info
            t_res = self.get_version_info(t_version_type, t_filebox_path, t_rule_list, t_max_version,
                                          t_filebox_data['server'], t_is_follow, t_follow_version, t_follow_title,
                                          t_version_length)
            if not isinstance(t_res, dict):
                t_error += u'记录:{} id:{} 获取文件框版本数据信息失败:{}\n'.format(t_link_entity, _id, t_res)
                continue

            return {'link_entity': t_link_entity, 'version': t_res['version'], 'filenames': t_res['filenames'],
                    'upload_paths': t_res['upload_paths'], 'online_paths': t_res['online_paths'],
                    'status': t_res['status'], 'tip': t_res['tip'], 'id': _id, 'filebox_data': t_filebox_data}

        if t_error != '':
            print(t_error)

    def get_version_info(self,
                         a_version_type,
                         a_filebox_path,
                         a_rule_list,
                         a_max_version,
                         a_server,
                         a_is_follow,
                         a_follow_version,
                         a_follow_title,
                         a_version_length):
        """获取版本信息"""
        try:
            if a_is_follow == 'y':
                if a_version_type in ['file', 'folder']:
                    return self.get_follow_version_file(a_filebox_path, a_rule_list, a_follow_version, a_follow_title,
                                                        a_server)
                else:
                    return u'Version type error.'
            else:
                if a_version_type == 'file':
                    return self.get_file_version(a_filebox_path, a_rule_list, a_max_version, a_version_length, a_server)
                elif a_version_type == 'folder':
                    return self.get_folder_version(a_filebox_path, a_rule_list, a_max_version, a_version_length,
                                                   a_server)
                elif a_version_type == 'same':
                    return self.get_same_version(a_filebox_path, a_rule_list, a_max_version, a_server)
                elif a_version_type == 'compat':  # compat
                    return self.get_compat_version(a_filebox_path, a_rule_list, a_max_version, a_version_length,
                                                   a_server)
                else:
                    return u'Version type error.'
        except:
            return traceback.format_exc()

    def get_link_entity(self, _id):
        """名称"""
        try:
            t_link_entity = self.m_tw.link_entity.get_name(self.m_database, self.m_module, self.m_module_type, _id)
        except Exception, e:
            print traceback.format_exc()
            t_link_entity = False
        return t_link_entity

    def get_file_version(self, a_filebox_path, a_rule_list, a_max_version, a_version_length, a_server):
        """文件"""
        t_res_dict = {'version': 'Null', 'filenames': '', 'upload_paths': [], 'status': u'跳过', 'tip': '',
                      'online_paths': []}  # 返回数据
        if not os.path.exists(a_filebox_path):
            return t_res_dict
        # all file list
        t_new_ver_rule_list = [
            _rule.replace('{ver}', '#' * a_version_length).replace("#", "[0-9]").replace("?", "[a-zA-Z]") for _rule in
            a_rule_list]
        t_file_list = ct_file().get_path_list(a_filebox_path, t_new_ver_rule_list)
        if not isinstance(t_file_list, list) or t_file_list == []:
            return t_res_dict
        # {ver:[],ver:[],ver:[]}
        t_version_dict = {}
        for _file in t_file_list:
            _file = _file.replace('\/', '/').replace('\\', '/')
            if _file.endswith('.db'):
                continue
            if os.path.isdir(_file) and os.path.basename(_file) == 'history':
                continue
            _version = self.__get_version('file', _file, a_rule_list, a_version_length)
            if _version == '':
                _version = '0' * a_version_length
            # -小于等于提交最大版本跳过
            if int(_version) <= int(a_max_version):
                continue
            t_version_dict.setdefault(str(_version), []).append(_file)

        if t_version_dict == {}:
            t_res_dict['status'] = u'无文件'
            return t_res_dict
        #
        t_current_version = sorted(t_version_dict.keys(), key=int)[-1]

        t_upload_list = t_version_dict[t_current_version]

        t_res_dict['version'] = t_current_version
        t_res_dict['filenames'] = ','.join([os.path.basename(_file) for _file in t_upload_list])
        t_res_dict['upload_paths'] = t_upload_list
        t_res_dict['online_paths'] = self._replace_server_path(t_upload_list, a_server)
        t_res_dict['status'] = u'等待'

        return t_res_dict

    def get_folder_version(self, a_filebox_path, a_rule_list, a_max_version, a_version_length, a_server):
        """目录"""
        t_res_dict = {'version': 'Null', 'filenames': '', 'upload_paths': [], 'status': u'跳过', 'tip': '',
                      'online_paths': []}  # 返回数据
        # 1.z:/xiaoying/shot/aa{ver}aa/check  -->  aa{ver}aa
        t_ver_basename = self.__get_folder_ver_basename(a_filebox_path)
        t_ver_rule = t_ver_basename.replace('{ver}', '[0-9]' * a_version_length)

        t_ver_dir = a_filebox_path[:a_filebox_path.find(t_ver_basename)]

        if not os.path.exists(t_ver_dir):
            return t_res_dict
        # -查这层目录下所有目录列表
        try:
            # 2.z:/xiaoying/shot/aa{ver}aa
            t_ver_folder_list = ct_file().get_path_list(t_ver_dir, [t_ver_rule])  # {ver} 这层所有版本目录列表
        except:
            print(traceback.format_exc())
            t_res_dict['tip'] = u'获取文件筐目录下文件失败:{},:{}'.format(a_filebox_path, traceback.format_exc())
            t_res_dict['status'] = u'错误'
            return t_res_dict

        t_version_dict = {}

        # 循环版本列表
        for _file in t_ver_folder_list:
            _file = _file.replace('\/', '/').replace('\\', '/')
            # -获取路径版本
            _version = self.__get_version('folder', _file, a_rule_list, a_version_length, a_filebox_path)

            if _version == '':
                continue
            # 版本小于等于最大版本的跳过
            if int(_version) <= int(a_max_version):
                continue
            # -使用版本 替换文件筐{ver}
            # 3.z:/xiaoying/shot/aa001aa/check
            t_filebox_ver_path = a_filebox_path.replace('{ver}', _version)
            # -路径存在时
            if os.path.exists(t_filebox_ver_path):
                t_version_dict[_version] = t_filebox_ver_path
        if t_version_dict == {}:
            t_res_dict['status'] = u'无文件'
            return t_res_dict

        # 查询目录下是否有文件
        t_current_version = ''
        t_new_rule_list = [unicode(_rule).strip().replace("#", "[0-9]").replace("?", "[a-zA-Z]") for _rule in
                           a_rule_list]
        # 从最大版本开始
        t_search_file_list = []
        for _ver in sorted(t_version_dict.keys(), key=int, reverse=True):
            _filebox_path = t_version_dict[_ver]
            t_temp_rule = copy.copy(t_new_rule_list)
            t_temp_rule = [_rule.replace('{ver}', _ver) for _rule in t_temp_rule]
            try:
                # 匹配命名规则
                t_search_file_list = ct_file().get_path_list(_filebox_path, t_temp_rule)
            except:
                print traceback.format_exc()
                t_search_file_list = []
            t_search_file_list = self._replace_new_file_list(t_search_file_list)
            if t_search_file_list == []:
                continue
            else:
                # 找到则退出循环
                t_current_version = _ver
                break
        if t_current_version == '':
            return t_res_dict

        t_res_dict['version'] = t_current_version
        t_res_dict['filenames'] = ','.join([os.path.basename(i) for i in t_search_file_list])
        t_res_dict['upload_paths'] = t_search_file_list
        t_res_dict['online_paths'] = self._replace_server_path(t_search_file_list, a_server)
        t_res_dict['status'] = u'等待'
        return t_res_dict

    def get_same_version(self, a_filebox_path, a_rule_list, a_max_version, a_server):
        """相同"""
        t_res_dict = {'version': 'Null', 'filenames': '', 'upload_paths': [], 'status': u'跳过', 'tip': '',
                      'online_paths': []}  # 返回数据
        #
        if not os.path.exists(a_filebox_path):
            return t_res_dict
        # 根据路径和命名规则
        t_new_rule_list = [unicode(_rule).strip().replace("#", "[0-9]").replace("?", "[a-zA-Z]") for _rule in
                           a_rule_list]
        try:
            t_file_list = ct_file().get_path_list(a_filebox_path, t_new_rule_list)
        except:
            t_res_dict['status'] = u'错误'
            t_res_dict['tip'] = u'获取文件筐目录下文件失败:{},:{}'.format(a_filebox_path, traceback.format_exc())
            return t_res_dict

        if not isinstance(t_file_list, list) or t_file_list == []:
            return t_res_dict

        t_file_list = self._replace_new_file_list(t_file_list)
        if t_file_list == []:
            return t_res_dict
        # 循环拼接字典
        # {
        # cc.txt:{"time":文件修改时间, size:xx},
        # test:{child:{'cc.jpg':{"time":xx, size:xx}, 'bb/dd.jpg': {"time":xx, size:xx}, 'aa/1/11.txt': {"time":xx, size:xx} }}
        # }
        t_local_file_dict = {}
        t_file_name_array = []
        t_folder_name_array = []
        try:
            for _file in t_file_list:
                _file = _file.replace('\/', '/').replace('\\', '/')
                if _file.endswith('.db'):
                    continue
                t_basename = os.path.basename(_file)
                # -文件
                if os.path.isfile(_file):
                    t_file_name_array.append(t_basename)
                    t_size = ct_file().get_size(_file)
                    t_time = ct_file().get_modify_time(_file)
                    t_local_file_dict[t_basename] = {'size': unicode(t_size), 'time': t_time}

                else:
                    if os.path.basename(_file).lower().strip() == 'history':
                        continue
                    t_folder_name_array.append(t_basename)
                    t_local_file_dict[t_basename] = {'child': {}}
                    _file = _file.rstrip('/') + '/'
                    # 目录
                    try:
                        t_walk_file_list = ct_file().get_file_with_walk_folder(_file)
                    except:
                        print traceback.format_exc()
                        continue
                    for _child in t_walk_file_list:
                        _child = _child.replace('\/', '/').replace('\\', '/')
                        _child_name = _child.replace(_file, '')
                        t_size = ct_file().get_size(_child)
                        t_time = ct_file().get_modify_time(_child)
                        t_local_file_dict[t_basename]['child'][_child_name] = {'size': unicode(t_size), 'time': t_time}
        except:
            t_res_dict['status'] = u'错误'
            t_res_dict['tip'] = u'获取文件框本地同版本数据失败:{}'.format(traceback.format_exc())
            return t_res_dict

        # 服务器获取相同的数据
        # 获取在线路径
        try:
            t_online_data = self.m_tw.send_web('c_file', 'get_info', {
                'db': self.m_database, 'module': self.m_module, 'module_type': self.m_module_type,
                'online_dir': a_filebox_path.replace(a_server.rstrip('/'), ''), 'file_name_array': t_file_name_array,
                'folder_name_array': t_folder_name_array
            })
        except:
            t_res_dict['status'] = u'错误'
            t_res_dict['tip'] = u'获取文件框在线同版本数据失败:{}'.format(traceback.format_exc())
            return t_res_dict
        # 获取要上传文件列表
        # 目录:文件个数不一样 或者其中一个文件大小或者修改时间不一样
        # 文件:时间或者大小不一样
        t_upload_file_list = []
        for _basename in t_local_file_dict:
            _upload_file = a_filebox_path + '/' + _basename
            _upload_file = _upload_file.replace('\/', '/').replace('\\', '/')
            # 返回空列表
            if t_online_data == []:
                t_upload_file_list.append(_upload_file)
                continue
            if not t_online_data.has_key(_basename):
                t_upload_file_list.append(_upload_file)
                continue
            # 目录
            if t_online_data[_basename].has_key('child'):
                t_local_child_dict = t_local_file_dict[_basename]['child']
                t_online_child_dict = t_online_data[_basename]['child']
                # 比较数量
                if len(t_local_child_dict.keys()) != len(t_online_child_dict.keys()):
                    t_upload_file_list.append(_upload_file)
                else:
                    for _child in t_local_child_dict.keys():
                        # 不存在child
                        if not t_online_child_dict.has_key(_child):
                            t_upload_file_list.append(_upload_file)
                            break
                        # 比较大小 修改时间
                        if self.__check_upload(t_local_child_dict[_child], t_online_child_dict[_child]):
                            t_upload_file_list.append(_upload_file)
                            break
            # 文件
            else:
                if self.__check_upload(t_local_file_dict[_basename], t_online_data[_basename]):
                    t_upload_file_list.append(_upload_file)
                    break
        if t_upload_file_list == []:
            return t_res_dict

        t_res_dict['version'] = str(int(a_max_version) + 1).zfill(3)
        t_res_dict['filenames'] = ','.join([os.path.basename(_file) for _file in t_upload_file_list])
        t_res_dict['upload_paths'] = t_upload_file_list
        t_res_dict['online_paths'] = self._replace_server_path(t_upload_file_list, a_server)
        t_res_dict['status'] = u'等待'
        return t_res_dict

    def get_follow_version_file(self, a_filebox_path, a_rule_list, a_follow_version, a_follow_title, a_server):
        # 仅目录和文件版本
        t_res_dict = {'version': a_follow_version, 'filenames': '', 'upload_paths': [], 'status': u'跳过', 'tip': '',
                      'online_paths': []}  # 返回数据
        if a_follow_version.strip() == '':
            t_res_dict['status'] = u'错误'
            t_res_dict['tip'] = u'请先提交被跟随的文件框({})'.format(a_follow_title)
            t_res_dict['version'] = 'Null'
            return t_res_dict
        t_filebox_path = a_filebox_path.replace('{ver}', a_follow_version)
        if not os.path.exists(t_filebox_path):
            return t_res_dict
        t_new_rule_list = [_rule.replace('{ver}', a_follow_version).replace("#", "[0-9]").replace("?", "[a-zA-Z]") for
                           _rule in a_rule_list]
        t_file_list = ct_file().get_path_list(t_filebox_path, t_new_rule_list)
        if not isinstance(t_file_list, list) or t_file_list == []:
            return t_res_dict
        t_file_list = self._replace_new_file_list(t_file_list)
        if t_file_list == []:
            return t_res_dict
        t_res_dict['filenames'] = ','.join([os.path.basename(_file) for _file in t_file_list])
        t_res_dict['upload_paths'] = t_file_list
        t_res_dict['online_paths'] = self._replace_server_path(t_file_list, a_server)
        t_res_dict['status'] = u'等待'
        return t_res_dict

    def get_compat_version(self, a_filebox_path, a_rule_list, a_max_version, a_version_length, a_server):
        """文件"""
        t_res_dict = {'version': 'Null', 'filenames': '', 'upload_paths': [], 'status': u'跳过', 'tip': '',
                      'online_paths': []}  # 返回数据
        if not os.path.exists(a_filebox_path):
            return t_res_dict
        # all file list
        t_new_ver_rule_list = [
            _rule.replace('{ver}', '#' * a_version_length).replace("#", "[0-9]").replace("?", "[a-zA-Z]") for _rule in
            a_rule_list]

        t_file_list = ct_file().get_path_list(a_filebox_path, t_new_ver_rule_list)
        if not isinstance(t_file_list, list) or t_file_list == []:
            return t_res_dict
        t_upload_list = self._replace_new_file_list(t_file_list)
        if t_upload_list == []:
            return t_res_dict
        t_upload_list = [sorted(t_upload_list)[-1]]

        t_res_dict['version'] = str(int(a_max_version) + 1).zfill(a_version_length)
        t_res_dict['filenames'] = ','.join([os.path.basename(_file) for _file in t_upload_list])
        t_res_dict['upload_paths'] = t_upload_list
        t_res_dict['online_paths'] = self._replace_server_path(t_upload_list, a_server)
        t_res_dict['status'] = u'等待'
        return t_res_dict

    def __check_upload(self, a_loacl_dict, a_online_dict):
        """检查是否上传"""
        if a_loacl_dict['time'] == a_online_dict['time'] and a_loacl_dict['size'] == a_online_dict['size']:
            return False
        else:
            return True

    def __get_folder_ver_basename(self, a_filebox_path):
        """找到目录{ver}那层级的basename"""
        # a_filebox_path = 'i:/xiaoying/Shot/Folder_Test/ep001/eq001/sc002/v{ver}aa/work'
        # a_filebox_path = 'i:/xiaoying/Shot/Folder_Test/ep001/eq001/sc002/v{ver}aa/'
        # a_filebox_patht = 'i:/xiaoying/Shot/Folder_Test/ep001/eq001/sc002/v{ver}aa'
        # a_filebox_path = 'i:/xiaoying/Shot/Folder_Test/ep001/eq001/sc002/v{ver}'
        t_ver_first_index = a_filebox_path.find('{ver}')  # {ver} 开始的位置
        t_lindex = a_filebox_path.rfind('/', 0, t_ver_first_index)  # {ver}左侧字符串 右边开始的一个'/'的位置
        t_rindex = a_filebox_path.find('/', t_lindex + 1)  # 找到{ver}层级后第一个'/'
        if t_rindex == -1:
            t_basename = a_filebox_path[t_lindex + 1:]
        else:
            t_basename = a_filebox_path[t_lindex + 1:t_rindex]
        return t_basename

    def __get_version(self, a_version_type, a_path, a_rule_list, a_version_length, a_filebox_path=''):
        version = ""
        # 文件版本
        if a_version_type == 'file':
            t_new_rule_list = []
            for _rule in a_rule_list:
                _rule = unicode(_rule).replace("{ver}", "#" * a_version_length)
                t_new_rule_list.append(_rule)
            t_basename = os.path.basename(a_path)
            for i in range(len(t_new_rule_list)):
                # 符合命名规则，获取版本号
                if ct_lib.com().is_match_regexp_string(t_new_rule_list[i], t_basename):
                    old_rule = t_new_rule_list[i]  # 带有{ver}的命名规则， shot01_ep01_v{ver}.mov
                    start_index = unicode(old_rule).find("#" * a_version_length)
                    end_index = start_index + a_version_length
                    if start_index != -1:
                        temp_ver = t_basename[start_index: end_index]
                        if temp_ver != "":
                            try:
                                temp_ver = int(temp_ver)  # 如果drag_ver不是数字则会报错
                                version = unicode("%0{}d".format(a_version_length) % temp_ver)
                            except:
                                version = ""

                    break
        # 目录版本
        else:
            # i:/xiaoying/Shot/Folder_Test/ep001/eq001/sc003/v{ver}a/work
            # i:/xiaoying/Shot/Folder_Test/ep001/eq001/sc003/v001
            # i:/xiaoying/Shot/Folder_Test/ep001/eq001/sc003/v001a
            t_ver_path = a_filebox_path.replace("\\", "/")  # 带有{ver}---  z:/test/aa/v{ver}/work
            index = unicode(t_ver_path).find("{ver}")
            if index != -1:
                left_str = t_ver_path[:index]  # z:/test/aa/v
                # 匹配源文件的版本
                a_path = unicode(a_path).replace("\\", "/").lower()
                if unicode(a_path).find(left_str.lower()) != -1:
                    # -直接返回  [index:index+3]
                    drag_ver = a_path[index:index + a_version_length]
                    # 判断长度是否为3 并是否是数字
                    if len(drag_ver) == a_version_length and drag_ver.isdigit():
                        version = drag_ver

        return version

    def _replace_server_path(self, a_file_list, a_server):

        # 替换server
        t_new_file_list = []
        t_temp_server = copy.copy(a_server).replace('\\', '/')
        for _file in a_file_list:
            _file = _file.replace('\\', '/').replace(t_temp_server, a_server)
            t_new_file_list.append(_file)
        return t_new_file_list

    def _replace_new_file_list(self, a_file_list):
        '''除db history目录'''
        t_new_file_list = []
        for _file in a_file_list:
            _file = _file.replace('\/', '/').replace('\\', '/')
            if _file.endswith('.db'):
                continue
            if os.path.isdir(_file) and os.path.basename(_file) == 'history':
                continue
            t_new_file_list.append(_file)
        return t_new_file_list


class CGTWWapper(cgtw2.tw):
    """
    cgtw2 的包装，增加了获取获取文件筐信息和提交
    """

    def __init__(self, http_ip=u"", account=u"", password=u""):
        cgtw2.tw.__init__(self, http_ip=http_ip, account=account, password=password)
        self.w_database = self.client.get_database()
        self.w_module = self.client.get_module()
        self.w_module_type = self.client.get_module_type()
        self.w_pipeline_id = self.client.get_sys_key(u"pipeline_id")
        self.w_id = self.client.get_id()

    def w_get_task_info(self):
        return self.task.get(db=self.w_database,
                             module=self.w_module,
                             id_list=self.w_id,
                             field_sign_list=["seq.entity",
                                              "shot.entity",
                                              "pipeline.entity",
                                              "task.entity",
                                              "task.artist"
                                              ])

    def w_get_filebox_data(self):
        filebox_data = self.filebox.get(db=self.w_database,
                                        module=self.w_module,
                                        module_type=self.w_module_type,
                                        field_list=self.filebox.fields(),
                                        pipeline_id_list=[self.w_pipeline_id])
        return filebox_data

    def w_pub(self, pub_data):
        t_filebox_data = pub_data['filebox_data']
        t_id = pub_data['id']
        t_version = pub_data['version']
        t_upload_list = pub_data['upload_paths']
        t_online_list = pub_data['online_paths']
        if t_upload_list == []:
            return

        t_dict = {"module": self.w_module,
                  "module_type": self.w_module_type,
                  "db": self.w_database,
                  "task_id": t_id,
                  "filebox_data": t_filebox_data,
                  "file_path_list": t_upload_list,
                  'des_file_path_list': t_online_list,
                  'version': t_version}
        pprint.pprint(u"bat_pub: %s" % str(t_dict))

        return self.send_local_http(self.w_database,
                                    self.w_module,
                                    u"filebox_bulk_upload_to_filebox",
                                    t_dict,
                                    u"get")

    def w_drop(self, filebox_id, path_list):
        if not path_list:
            return

        t_dic = {
            u"db": self.w_database,
            u"module_type": self.w_module_type,
            u"task_id": self.w_id[0],
            u"filebox_data": {u"#id": filebox_id},
            u"path_list": path_list
        }
        pprint.pprint("user_pub: %s" % str(t_dic))

        self.send_local_http(self.w_database,
                             self.w_module,
                             u"api_drop",
                             t_dic)

    def w_refresh(self):
        self.client.refresh_all(self.w_database, self.w_module, self.w_module_type)


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args):
        super(FileDialog, self).__init__(*args)
        self.setOption(self.DontUseNativeDialog, True)
        btns = self.findChildren(QtWidgets.QPushButton)
        self.open_btn = [btn for btn in btns if u'open' in str(btn.text()).lower()][0]
        self.open_btn.clicked.disconnect()
        self.open_btn.clicked.connect(self.__open_clicked)
        self.tree = self.findChild(QtWidgets.QTreeView)

        self.files = []

    def __open_clicked(self):
        inds = self.tree.selectionModel().selectedIndexes()
        self.files = []
        for i in inds:
            if i.column() == 0:
                self.files.append(str(self.directory().absolutePath()).replace(u"\\", u"/") +
                                  u"/" +
                                  str(i.data()).replace(u"\\", u"/"))
        self.hide()

    @classmethod
    def get_files_and_dirs(cls, *args):
        dialog = cls(*args)
        dialog.setFileMode(dialog.ExistingFiles)
        dialog.exec_()
        return dialog.files


class RowWidget(QtWidgets.QWidget):
    def __init__(self):
        super(RowWidget, self).__init__()
        """
          添加一行布局，显示当前提交信息，以及一个按钮用于手动提交
          """
        # 按钮
        self.button = QtWidgets.QPushButton(u"手动提交")
        self.button.setEnabled(False)
        # 标题
        self.title = QtWidgets.QLabel()
        # step
        self.__step = QtWidgets.QLabel(u" >> ")
        # 信息
        self.info = QtWidgets.QLabel()

        row_layout = QtWidgets.QHBoxLayout(self)
        row_layout.addWidget(self.button)
        row_layout.addWidget(self.title)
        row_layout.addWidget(self.__step)
        row_layout.addWidget(self.info)
        row_layout.addStretch()


class MainUI(QtWidgets.QDialog):
    user_selected_files = QtCore.Signal(str, list)

    def __init__(self):
        super(MainUI, self).__init__()
        self.__setup_ui()

        self.__row_widgets = {}  # {filebox_id: RowWidget}

    def __setup_ui(self):
        icon_file = os.path.join(os.path.dirname(__file__), u"pub_icon.png")
        self.setWindowIcon(QtGui.QIcon(icon_file))
        self.setMinimumWidth(500)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.pub_progress_bar = QtWidgets.QProgressBar()
        self.label_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addWidget(self.pub_progress_bar)

    def set_range(self, minimum, maximum):
        self.pub_progress_bar.setRange(minimum, maximum)

    def set_value(self, value):
        self.pub_progress_bar.setValue(value)

    def set_user_pub_buttons_enabled(self, bool):
        """
        启用所有用户提交按钮
        """
        for rw in self.__row_widgets.values():
            rw.button.setEnabled(bool)

    def get_row_widget(self, filebox_id):
        return self.__row_widgets.get(filebox_id)

    def user_pub_dialog(self, filebox_id, start_path):
        # for btn in self.__user_pub_buttons:
        #     if btn.filebox_id == filebox_id:
        #         btn.setText(u"等待")

        files = FileDialog.get_files_and_dirs(self,
                                              u"请选择要提交的文件或者文件夹",
                                              start_path)
        self.user_selected_files.emit(filebox_id, files)
        return files

    def add_info(self, text):
        self.label_layout.addWidget(QtWidgets.QLabel(text))

    def set_row_widget_info(self, filebox_id, title=u"", info=u"", info_color=u""):
        row_widget = self.__row_widgets.get(filebox_id)
        if title:
            row_widget.title.setText(title)
        if info:
            row_widget.info.setText(info)
        # 设置文字颜色
        if info_color:
            row_widget.info.setStyleSheet(u"color: %s" % info_color)

    def add_row_widget(self, filebox_id, start_path, title, info, info_color=u""):
        """
          添加一行布局，显示当前提交信息，以及一个按钮用于手动提交
          """
        # 按钮
        RW = RowWidget()
        RW.filebox_id = filebox_id
        RW.start_path = start_path
        RW.button.clicked.connect(lambda: self.user_pub_dialog(RW.filebox_id,
                                                               RW.start_path))

        self.__row_widgets[filebox_id] = RW

        self.set_row_widget_info(filebox_id, title, info, info_color)

        self.label_layout.addWidget(RW)


class Response(MainUI):
    INSTANCE = None

    mainui_set_title = QtCore.Signal(str)
    progress_set_range = QtCore.Signal(int, int)
    progress_set_value = QtCore.Signal(int)
    mainui_add_info = QtCore.Signal(str)
    mainui_row_widget = QtCore.Signal(str, str, str, str, str)
    mainui_pub_buttons_enabled = QtCore.Signal(bool)

    def __init__(self):
        super(Response, self).__init__()
        self.cgtww = CGTWWapper()

        self.__setup_connect()

    def __setup_connect(self):
        self.mainui_set_title.connect(self.setWindowTitle)
        self.progress_set_range.connect(self.set_range)
        self.progress_set_value.connect(self.set_value)
        self.mainui_add_info.connect(self.add_info)
        self.mainui_row_widget.connect(self.add_row_widget)
        self.user_selected_files.connect(self.user_pub)
        self.mainui_pub_buttons_enabled.connect(self.set_user_pub_buttons_enabled)

    def filter_data(self, filebox_data_list, pub_sign):
        """
        筛选出指定标识的文件框数据
        标识的类型在脚本参数 pub_sign 中设置
        """
        # list, 标识列表，文件框标识包含此列表里字段的会被触发提交操作
        # 提交顺序为列表顺序
        # 文件筐标识命名时，用下划线区分不同标识
        if not pub_sign:
            return []
        else:
            pub_sign = eval(pub_sign)

        # 记录每个标记的索引值，filebox 的数据将按照此索引值排序
        # key: filebox_sign, value: filebox_index
        pub_sign_dict = {}
        for ps in pub_sign:
            pub_sign_dict[ps] = pub_sign.index(ps)

        new_filebox_data = []
        for fd in filebox_data_list:
            f_sign = fd[u"sign"].split(u"_")
            for ps, i in pub_sign_dict.items():
                if ps in f_sign:
                    new_filebox_data.insert(i, fd)

        return new_filebox_data

    def get_start_path(self, path):
        """
        一直切割路径直到找到一个存在的根路径
        """
        # 获取启示路径
        # 如果路径不存在就获取上一级
        # 知道层级只剩最后一级时，跳出循环
        start_path = path.replace(u"\\", u"/")
        while not os.path.isdir(start_path):
            start_path = os.path.dirname(start_path)
            if len(start_path.split(u"/")) <= 2:
                break
        return start_path

    def user_pub(self, filebox_id, start_path):
        self.cgtww.w_drop(filebox_id, start_path)
        self.set_row_widget_info(filebox_id=filebox_id,
                                 info=u"用户已手动提交",
                                 info_color=u"Blue")

    def pub(self):
        # 设置标题
        self.mainui_set_title.emit(u"正在读取任务....")
        try:
            task_info = self.cgtww.w_get_task_info()[0]
            self.mainui_set_title.emit(
                u"{seq}/{shot}/{pipeline}/{task}/{artist}".format(seq=task_info[u"seq.entity"],
                                                                  shot=task_info[u"shot.entity"],
                                                                  pipeline=task_info[
                                                                      u"pipeline.entity"],
                                                                  task=task_info[u"task.entity"],
                                                                  artist=task_info[
                                                                      u"task.artist"])
            )
        except Exception as e:
            self.mainui_set_title.emit(e)
        # 获取所有 filebox 数据
        filebox_data_list = self.cgtww.w_get_filebox_data()
        if not filebox_data_list:
            self.mainui_add_info.emit(u"没有获取提交框'")
            return
        # 获取 pub_sign 参数
        pub_sign = self.cgtww.client.get_argv_key(u"pub_sign")
        if not pub_sign:
            self.mainui_add_info.emit(u'未设置提交标识')
            return
        # 筛选数据
        filebox_data_list = self.filter_data(filebox_data_list, pub_sign)
        if not filebox_data_list:
            self.mainui_add_info.emit(u'未获取到指定标识的提交框')
            return

        # 设置进度条最大最小值
        self.progress_set_range.emit(0, len(filebox_data_list))

        progress_bar_value = 1
        for fd in filebox_data_list:
            # 获取提交信息
            CFI = VersionFilesInfo(a_tw=self.cgtww,
                                   a_database=self.cgtww.w_database,
                                   a_module=self.cgtww.w_module,
                                   a_module_type=self.cgtww.w_module,
                                   a_id_list=self.cgtww.w_id,
                                   a_filebox_id=fd.get(u"#id"),
                                   a_func=self.cgtww.task)
            # 提交
            pub_data = CFI.get()
            filebox_data = pub_data.get(u"filebox_data")  # CFI.get() 包含更多filebox信息
            rls = self.cgtww.w_pub(pub_data)
            if isinstance(rls, bool) and rls:
                self.mainui_row_widget.emit(filebox_data[u"#id"],
                                            self.get_start_path(filebox_data[u"path"]),
                                            filebox_data.get(u"title"),
                                            u"提交成功",
                                            u"Green"
                                            )
            else:
                if not rls:
                    self.mainui_row_widget.emit(filebox_data[u"#id"],
                                                self.get_start_path(filebox_data[u"path"]),
                                                filebox_data.get(u"title"),
                                                u"未检测到需要提交的文件",
                                                u"Red"
                                                )
                else:
                    self.mainui_row_widget.emit(filebox_data[u"#id"],
                                                self.get_start_path(filebox_data[u"path"]),
                                                u"%s >> %s" % (filebox_data.get(u"title"),
                                                               rls),
                                                u"Red"
                                                )

            # 进度条+1
            self.progress_set_value.emit(progress_bar_value)
            progress_bar_value += 1

        # 刷新
        self.cgtww.w_refresh()
        self.mainui_pub_buttons_enabled.emit(True)

    def _pub(self):
        pub_threading = threading.Thread(target=self.pub, args=())
        pub_threading.start()

    @classmethod
    def start(cls):
        # 显示进度条
        app = QtWidgets.QApplication(sys.argv)
        if not cls.INSTANCE:
            cls.INSTANCE = cls()
        # 显示
        cls.INSTANCE.show()
        cls.INSTANCE.raise_()
        # 提交
        cls.INSTANCE._pub()
        sys.exit(app.exec_())

    def closeEvent(self, event):
        self.cgtww.w_refresh()
        event.accept()


if __name__ == u"__main__":
    Response.start()
