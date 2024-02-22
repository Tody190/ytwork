# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/4 10:17
"""

import re
import glob
from pathlib2 import Path


class AssetFile:
    def __init__(self, asset_file):
        self.asset_file = asset_file

        self.name = None  # c001006nzab.rig.rigging
        self.file_name = None  # c001006nzab.rig.rigging.ma
        self.version_num = None  # 1
        self.step = None  # rig
        self.task = None  # rigging
        self.reference_file = None
        self.new_reference_file = None  # 需要替换的路径
        self.version_file = None  # I:/projects/nzt/asset/chr/c049001szd/rig/c049001szd.rig.rigging.v020/c049001szd.ma
        self.version_path = None
        self.version_name = None  # c001006nzab.rig.rigging.v026
        self.mesh_xml_file = None

        self.maya_node = None  # maya reference node

        self.__init_data()

    def __init_data(self):
        pattern_str = r'.+\\%s\.(.+)\.(.+)\.v(\d+)\\.+' % str(self.asset_file.stem)  # c001006nzab.rig.rigging.v009
        pattern_str += r'|'
        pattern_str += r'.+\\%s\.(.+)\.(.+)\\.+' % str(self.asset_file.stem)  # c001006nzab.rig.rigging
        _result = re.search(pattern_str, str(self.asset_file))
        if _result:
            self.name = self.asset_file.stem
            self.file_name = self.asset_file.name
            result = _result.groups()
            # 使用带版本号资产的取版本号
            if result[1]:  # result = ('rig', 'rigging', '001', '', '')
                self.version_num = int(result[2])
                self.step = result[0]
                self.task = result[1]
                self.reference_file = self.asset_file
                self.version_file = self.asset_file
                self.version_path = Path(self.version_file).parent  # 版本文件夹路径

            # 使用无版本号资产，最大版本文件即为它的版本
            else:  # result = ('', '', '', 'rig', 'rigging')
                ver_folder_list = glob.glob('%s.v*' % self.asset_file.parent)
                ver_folder_list = sorted(ver_folder_list, key=lambda v: v.rsplit('.', 1)[-1])

                self.version_path = Path(ver_folder_list[-1])
                self.version_num = int(str(self.version_path).lower().split('.v')[-1])
                self.step = result[3]
                self.task = result[4]
                self.reference_file = self.asset_file
                self.version_file = self.version_path.joinpath(self.asset_file.name)
                self.version_name = self.version_path.name

            # 添加 mesh.xml 信息
            self.mesh_xml_file = self.get_xml(self.version_name)

    def get_xml(self, version_name):
        xml_file = self.version_path.parent.joinpath(r"%s\mesh.xml" % version_name)
        if xml_file.is_file():
            return xml_file


class MaFile:
    def __init__(self, ma_file):
        # W:\projects\nzt\shot\i20\i20730\lay\maya\i20730.lay.rough_layout.v004.ma
        self.maya_file = Path(ma_file)
        self.suffix = self.maya_file.suffix
        self.version_name = self.maya_file.stem  # i20730.lay.rough_layout.v012
        self.name = self.maya_file.name
        self.path = self.maya_file.parent
        self.no_version_num_name = str(self.version_name).rsplit('.v', 1)[0]  # i20730.lay.rough_layout
        self.version_format_num = str(self.version_name).rsplit('.v', 1)[-1]  # 012
        self.shot_name = (str(self.version_name)).split('.', 1)[0]  # i20730
        self.content_name = (str(self.version_name)).split('.')[2]  # rough_layout
        try:
            self.version_num = int(self.version_format_num)  # 12
        except:
            self.version_num = 0
        self.version_str = "v%s" % self.version_format_num  # v012
        # self.shot = str(self.maya_file).split('\\')[5]  # i20180
        # self.seq = str(self.maya_file).split('\\')[4]
        self.shot = self.name.split('.', 1)[0]  # i20180
        self.seq = self.shot[0: 3]  # i2
        self.new_file = None

        self.__file_content = []
        self.__content_blocks = []
        self.__assets = []

    @property
    def file_content(self):
        if self.__file_content:
            return self.__file_content
        else:
            print('Reading file: [%s]' % self.name)
            with open(str(self.maya_file), 'r') as maya_file:
                return maya_file.read()

    @property
    def content_blocks(self):
        '''
        文件切成列表
        :return:
        '''
        if self.__content_blocks:
            return self.__content_blocks
        else:
            block_step = ['requires', 'file -r', 'file -rdi', 'createNode',
                          'currentUnit', 'fileInfo', 'select', 'connectAttr',
                          'dataStructure']

            re_exp = '(' + '|'.join(map(re.escape, block_step)) + ')'
            self.__content_blocks = re.split(re_exp, self.file_content)
            return self.__content_blocks
        # maya文件头
        # file_blocks.append(content_list[0])
        # for i, element in content_list:
        #     if element in the_map.keys():
        #         # 将对应分隔符后面的部分整理成列表
        #         the_map[element].append(content_list[i + 1])
        #
        # return the_map

    @property
    def blocks_map(self):
        """
        """
        the_map = {'requires': [],
                   'file -r': [],
                   'file -rdi': [],
                   'createNode': [],
                   'currentUnit': [],
                   'fileInfo': [],
                   'select': [],
                   'connectAttr': [],
                   'dataStructure': []}

        re_exp = '(' + '|'.join(map(re.escape, the_map.keys())) + ')'

        content_list = re.split(re_exp, self.file_content)
        # maya文件头
        the_map["head"] = [content_list[0]]
        for i, element in enumerate(content_list):
            if element in the_map.keys():
                # 将对应分隔符后面的部分整理成列表
                the_map[element].append(content_list[i + 1])

        return the_map

    @property
    def assets(self):
        if self.__assets:
            return self.__assets

        # for _f in self.blocks_map['file -r']:
        for i, b in enumerate(self.content_blocks):
            if b == 'file -r':
                reference_file = re.findall('-typ[\s\S]*\"(.+?)\"',
                                            self.__content_blocks[i + 1])[0]  # get reference file
                reference_file = Path(reference_file)
                if reference_file.is_file():
                    asset_file = AssetFile(reference_file)
                    self.__assets.append(asset_file)

        return self.__assets

    def get_new_file(self):
        new_version_format_num = str(self.version_num + 1).zfill(len(self.version_format_num))
        return self.maya_file.parent.joinpath('%s.v%s%s' % (self.no_version_num_name,
                                                            new_version_format_num,
                                                            self.suffix))

    def save(self, new=True):
        # 编辑并替换 maya 文件资产路径
        # 保存为新版本文件
        has_new_reference_assets = []
        for asset in self.assets:
            if asset.new_reference_file:
                has_new_reference_assets.append(asset)

        if not has_new_reference_assets:
            print('No update: [%s]' % self.name)
            return

        new_content_blocks = self.content_blocks[:]
        for i, b in enumerate(new_content_blocks):
            if b == 'file -r':
                for asset in has_new_reference_assets:
                    reference_file = str(asset.reference_file).replace('\\', '/')
                    new_reference_file = str(asset.new_reference_file).replace('\\', '/')
                    if reference_file in new_content_blocks[i + 1]:
                        new_content_blocks[i + 1] = new_content_blocks[i + 1].replace(reference_file,
                                                                                      new_reference_file)
                        print('Replace: [%s -> %s]' % (str(asset.reference_file),
                                                       str(asset.new_reference_file.name)))

        # 升级版本号的文件
        if new:
            file_name = self.get_new_file()
            self.new_file = file_name
        else:
            file_name = self.maya_file

        with open(str(file_name), 'w') as f:
            for each_line in new_content_blocks:
                f.write(each_line)

            return file_name
