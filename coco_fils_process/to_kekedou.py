# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/8/4 10:14
"""
import glob
import json
import os.path
import re
import shutil
import pprint
import datetime
import time

from oct.pipeline.path import symlink
import shotgun_api3

sg = shotgun_api3.Shotgun('http://sg.ds.com/',
                          script_name='Generic',
                          api_key="kalyywr~ayDzxsum3bshirqea")

project_name = "NZT"

kekedou_asset_type_map = {'chr': 'char',
                          'prp': 'prop',
                          'asb': 'set',
                          'env': 'elem',
                          "crd": "char"}

kekedou_task_name_map = {"animation": "animation",
                         "blocking": "animation",
                         "rough_layout": "lay"}

# current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join("D:/yangtao/work/temp/loast_assets_log/error_log.log")

ignore_drive = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'x', 'y', 'z']  # 保留 i 和 w


def get_kekedou_task_name(oct_task_name):
    for task_name in kekedou_task_name_map:
        if oct_task_name in task_name:
            return kekedou_task_name_map[task_name]


def get_kekedou_asset_version(version_name):
    filters = [["project.Project.name", "is", project_name],
               ["code", "is", version_name]]
    fields = ["client_code"]

    client_code = sg.find_one("Version", filters, fields)["client_code"]
    if not client_code:
        client_code = "NoClientCode.v001"

    return client_code


def get_ani_file_from_shot(oct_shot_name):
    version_name = "%s.ani.animation" % oct_shot_name
    filters = [["project.Project.name", "is", project_name],
               ["code", "starts_with", version_name]]
    fields = ["code", "sg_path_to_geometry"]

    geo_path_list = []
    for v in sg.find("Version", filters, fields):
        geo_path_list.append(v["sg_path_to_geometry"])

    geo_path_list = sorted(geo_path_list)

    if geo_path_list:
        return geo_path_list[-1]


def get_ani_file_from_seq(oct_seq_name):
    filters = [["project.Project.name", "is", project_name],
               ["code", "is", oct_seq_name]]
    fields = ["code", "shots"]

    shot_e_list = []
    for v in sg.find("Sequence", filters, fields):
        shot_e_list += v["shots"]

    geo_path_list = []
    for shot_e in shot_e_list:
        shot_name = shot_e["name"]
        ani_file = get_ani_file_from_shot(shot_name)
        if ani_file:
            geo_path_list.append(ani_file)

    return geo_path_list


def get_asset_data(ma_file):
    # print("--- Asset FIle %s" % ma_file)
    tokens = ma_file.split('/')
    entity_type = tokens[3]  # asset
    if entity_type != "asset":
        print("Not Asset [%s]" % ma_file)
        with open(log_file, 'a') as f:
            f.write("Not Asset: " + ma_file + "\n")
        return

    asset_type = kekedou_asset_type_map[tokens[4]]  # asset_type

    if tokens[5] == os.path.splitext(tokens[-1])[0] == tokens[7].split('.')[0]:  # c130001boary
        asset_name = tokens[5]
    else:
        return

    if tokens[6] == tokens[7].split('.')[1]:
        step = tokens[6]
    else:
        return

    task_name = tokens[7].split('.')[2]

    if len(tokens[7].split('.')) == 4:  # c132001bobcaty.rig.rigging.v007
        ver = get_kekedou_asset_version(tokens[7]).rsplit('.', 1)[-1]
    else:
        ver = None  # c132001bobcaty.rig.rigging

    return {"entity_type": entity_type, "asset_type": asset_type,
            "asset_name": asset_name, "step": step,
            "task_name": task_name, "ver": ver}


def process_reference(reference_file):
    # 已经替换
    if reference_file.startswith("$SERVER_ROOT/NZT"):
        return reference_file

    # 项目外的盘符引用移除
    drive_name = reference_file.split(":", 1)[0]
    if drive_name.lower() in ignore_drive:
        print("Error Path: [%s]" % reference_file)
        with open(log_file, 'a') as f:
            f.write("Error Path: " + reference_file + "\n")
        return ""

    # 固定替换
    replace_map = {"I:/projects/nzt/asset/chr/c049003szddbbl/rig/c049003szddbbl.rig.rigging/c049003szddbbl.ma":
                       "$SERVER_ROOT/NZT/assets/char/c049002szddb/assembly/rig/main/ok/c049002szddb_rig_main.ma",
                   "W:/projects/nzt/misc/configs/maya/kekedou/camera_template.ma":
                       "$SERVER_ROOT/NZT/shots/_resources/rig/camRig.ma",
                   "I:/projects/nzt/from_kekedou/NZT/shots/_resources/rig/camRig.ma":
                       "$SERVER_ROOT/NZT/shots/_resources/rig/camRig.ma"}

    for src_file, dst_file in replace_map.items():
        if src_file in reference_file:
            reference_file = reference_file.replace(src_file, dst_file)
            return reference_file

    # 资产替换
    asset_data = get_asset_data(reference_file)
    if asset_data:
        if asset_data["entity_type"] == "asset":
            if asset_data["ver"]:
                coco_asset_f = "I:/projects/nzt/from_kekedou/NZT/assets/"
            else:
                coco_asset_f = "I:/projects/nzt/to_kekedou/NZT/assets/"

            if asset_data["step"] == 'rig':
                coco_asset_f += "{asset_type}/{asset_name}/assembly/{step}/main/ok/"
                if asset_data["ver"]:
                    coco_asset_f += asset_data["ver"] + "/"
                coco_asset_f += "{asset_name}_rig_main.ma"
            else:
                coco_asset_f += "{asset_type}/{asset_name}/{step}/geo/main/ok/{asset_name}_geo_main.ma"

            coco_asset_f = coco_asset_f.format(asset_name=asset_data["asset_name"],
                                               asset_type=asset_data["asset_type"],
                                               step=asset_data["step"])

            if not os.path.isfile(coco_asset_f):
                print("Can not find [%s]" % coco_asset_f)
                with open(log_file, 'a') as f:
                    f.write("Can not find: " + coco_asset_f + "\n")

            reference_file = coco_asset_f

    reference_file = reference_file.replace("I:/projects/nzt/to_kekedou", "$SERVER_ROOT")
    reference_file = reference_file.replace("I:/projects/nzt/from_kekedou", "$SERVER_ROOT")

    if reference_file.startswith("$SERVER_ROOT/NZT"):
        return reference_file


def get_kekedou_shot_name(oct_shot_name):
    proj = {'type': 'Project', 'id': 107}
    shot_e = sg.find_one('Shot', filters=[['project', 'is', proj],
                                          ['code', 'is', oct_shot_name]],
                         fields=['sg_client_shot_name'])
    if shot_e:
        return shot_e['sg_client_shot_name']
    else:
        print("Can not find [%s]" % oct_shot_name)


def get_translated_data(oct_shot_name):
    proj = {'type': 'Project', 'id': 107}
    shot_e = sg.find_one('Shot', filters=[['project', 'is', proj],
                                          ['code', 'is', oct_shot_name]],
                         fields=['sg_translated_data'])
    if shot_e:
        if shot_e['sg_translated_data']:
            return eval(shot_e['sg_translated_data'])
        else:
            return 0.0, 0.0, 0.0
    else:
        print("Can not find [%s]" % oct_shot_name)


class OCTToKEKEDOU(object):
    def __init__(self, ma_file):
        self.ma_file = ma_file
        self.file_dir = os.path.dirname(self.ma_file)
        self.file_stm = os.path.splitext(os.path.basename(self.ma_file))[0]
        self.dst_dir = "I:/projects/nzt/to_kekedou/NZT/shots"
        # 创建目标路径
        self.ma_file_name = self.ma_file.split('/')[-1]
        self.cache_dir = "I:/projects/nzt/cache"
        self.ext = os.path.splitext(self.ma_file_name)[-1]

        self.oct_shot_name = self.ma_file_name.split('.')[0]
        self.oct_seq_name = self.oct_shot_name[:3]
        self.oct_step = self.ma_file_name.split('.')[1]
        self.oct_task_name = self.ma_file_name.split('.')[2]
        self.oct_version_name = os.path.splitext(self.ma_file_name)[0]

        self.kekedou_shot_name = get_kekedou_shot_name(self.oct_shot_name)
        self.kekedou_seq_name = self.kekedou_shot_name[:3]
        self.kekedou_step = self.ma_file_name.split('.')[1]
        self.kekedou_task_name = get_kekedou_task_name(self.oct_task_name)
        self.kkedou_version_name = "%s_%s_%s" % (self.kekedou_shot_name,
                                                 self.kekedou_step,
                                                 self.kekedou_task_name)
        self.kekedou_ma_file_name = self.kkedou_version_name + self.ext
        self.kekedou_mov_file_name = self.kkedou_version_name + ".mov"

        self.__ref_replace_map = {}  # src_file: dst_file  替换路径的映射表，缓存路径用

    @property
    def dst_version_dir(self):
        dst_shot_dir = "/".join([self.dst_dir,
                                 self.kekedou_seq_name,
                                 self.kekedou_shot_name,
                                 "ani",
                                 self.kekedou_task_name,
                                 "ok"])
        if not os.path.isdir(dst_shot_dir):
            os.makedirs(dst_shot_dir)

        return dst_shot_dir

    @property
    def blocks_list(self):
        # 将 ma 文件切分为列表
        separators = ["requires", "file -r ", "file -rdi ",
                      "createNode ", "requires ", "currentUnit ",
                      "fileInfo ", "select ", "connectAttr ",
                      "dataStructure ", "// End of "]
        regular_exp = "(" + "|".join(map(re.escape, separators)) + ")"

        with open(self.ma_file, "r") as f:
            blocks_list = re.split(regular_exp, f.read())

        # ["dataStructure-fmt", ""raw" -as "name=notes_bushes_parShape:string=value"";]
        # ↓
        # ["dataStructure-fmt "raw" -as "name=notes_bushes_parShape:string=value"";]
        new_blocks = []
        skip = False
        for i, b in enumerate(blocks_list):
            if skip:
                skip = False
                continue

            if b in separators:
                skip = True
                new_blocks.append(b + blocks_list[i + 1])
            else:
                new_blocks.append(b)

        return new_blocks

    def copy_reference(self, copyfile):
        kekedou_ref_p = self.dst_version_dir + "/reference"
        if not os.path.exists(kekedou_ref_p):
            os.makedirs(kekedou_ref_p)

        dst_file = os.path.join(kekedou_ref_p, os.path.basename(copyfile))
        dst_file = dst_file.replace("\\", "/")

        print("%s =copy=> %s" % (copyfile, dst_file))
        shutil.copy2(copyfile, dst_file)
        return dst_file

    def copy_preview(self):
        preview_f = self.file_dir + "/preview/" + self.file_stm + ".mov"
        if os.path.exists(preview_f):
            kekedou_preview_f = self.dst_version_dir + "/" + self.kekedou_mov_file_name
            print("%s =copy=> %s" % (preview_f, kekedou_preview_f))
            shutil.copy2(preview_f, kekedou_preview_f)

    def link_preview(self):
        preview_f = self.file_dir + "/preview/" + self.file_stm + ".mov"
        if os.path.exists(preview_f):
            kekedou_preview_f = self.dst_version_dir + "/" + self.kekedou_mov_file_name
            print("%s =link=> %s" % (preview_f, kekedou_preview_f))
            symlink(preview_f, kekedou_preview_f, exist_remove=True)

    def copy_components_json(self):
        components_json = self.file_dir + "/shot_components.json"
        if os.path.exists(components_json):
            kekedou_components_json = self.dst_version_dir + "/%s_shot_components.json" % self.kekedou_shot_name
            print("%s =copy=> %s" % (components_json, kekedou_components_json))
            shutil.copy2(components_json, kekedou_components_json)

    def link_components_json(self):
        components_json = self.file_dir + "/shot_components.json"
        if os.path.exists(components_json):
            kekedou_components_json = self.dst_version_dir + "/%s_shot_components.json" % self.kekedou_shot_name
            print("%s =link=> %s" % (components_json, kekedou_components_json))
            symlink(components_json, kekedou_components_json, exist_remove=True)

    def copy_resource(self, resource_folder=("sourceimages", "cache", "sound")):
        for copy_dir in resource_folder:
            sr_p = self.file_dir + "/" + copy_dir
            if not os.path.isdir(sr_p):
                print("Can not find %s folder: %s" % (copy_dir, sr_p))
                return

            if os.path.isdir(sr_p):
                dst_p = self.dst_version_dir + "/" + copy_dir
                if os.path.exists(dst_p):
                    shutil.rmtree(dst_p)

                print("%s =copy=> %s" % (sr_p, self.dst_version_dir))
                shutil.copytree(sr_p, dst_p)

    def link_resource(self, resource_folder=("sourceimages", "cache", "sound")):
        for copy_dir in resource_folder:
            sr_p = self.file_dir + "/" + copy_dir
            if not os.path.isdir(sr_p):
                print("Can not find %s folder: %s" % (copy_dir, sr_p))
                continue

            dst_p = self.dst_version_dir + "/" + copy_dir

            print("%s =link=> %s" % (sr_p, dst_p))
            symlink(sr_p, dst_p, exist_remove=True)

    def link_cache(self):
        caches_name = []
        cache_folder = self.file_dir + "/cache"
        if not os.path.isdir(cache_folder):
            print("Can not find cache folder: %s" % cache_folder)
            return

        for f_name in os.listdir(self.file_dir + "/cache"):
            if f_name.endswith(".abc"):
                caches_name.append(os.path.splitext(f_name)[0])

        cache_path = "/".join([self.cache_dir,
                               self.oct_seq_name,
                               self.oct_shot_name])  # I:/projects/nzt/cache
        for c_name in caches_name:
            # I:/projects/nzt/cache/i20/i20310/c001006nzab/i20310.ani.animation.v003/c001006nzab.abc
            cache_version_path = "/".join([cache_path,
                                           c_name,
                                           self.oct_version_name])

            dst_abc_path = self.dst_version_dir + "/cache"
            # I:/projects/nzt/from_kekedou/NZT/shots/mls/mls126/ani/animation/ok/cache
            if not os.path.isdir(dst_abc_path):
                os.makedirs(dst_abc_path)

            for cache_ext in [".abc", ".usd"]:
                src_abc_file = cache_version_path + "/" + c_name + cache_ext
                dst_abc_file = dst_abc_path + "/" + c_name + cache_ext

                origin_cache_file_glob_str = "/".join([cache_path,
                                                       c_name,
                                                       self.oct_version_name,
                                                       "origin.%s*" % c_name + cache_ext])
                origin_files = glob.glob(origin_cache_file_glob_str)
                if origin_files:
                    src_abc_file = sorted(origin_files)[-1]

                # 哪吒大小写问题
                src_abc_file = src_abc_file.replace("/c001001nzkid/", "/c001001nzKid/")

                if os.path.exists(src_abc_file):
                    print(src_abc_file, "=link=>", dst_abc_file)
                    # time.sleep(1)
                    symlink(src_abc_file, dst_abc_file, exist_remove=True)

    def export_translated_data(self):
        kekedou_components_json = self.dst_version_dir + "/%s_translated_data.json" % self.kekedou_shot_name
        with open(kekedou_components_json, "w") as f:
            f.write(json.dumps(get_translated_data(self.oct_shot_name)))

    def oct_to_kekedou(self,
                       dst_dir=None,
                       ma_file=True,
                       preview=True,
                       components_json=True,
                       translated_data=False,
                       source_images=True,
                       cache=True,
                       sound=True):
        print("start >>>>>>> ")

        if dst_dir:
            self.dst_dir = dst_dir

        print("Shot Name: ", self.oct_shot_name)
        print("Dst Version Path: ", self.dst_version_dir)
        print("---------------------")

        # 拷贝预览贴图
        resource_folder = []
        if source_images:
            resource_folder.append("sourceimages")
        if sound:
            resource_folder.append("sound")
        self.copy_resource(resource_folder=resource_folder)

        # 拷贝预览
        if preview:
            self.copy_preview()

        # 链接原始ABC缓存到目标路径
        if cache:
            self.link_cache()

        if components_json:
            self.copy_components_json()

        if translated_data:
            self.export_translated_data()

        if ma_file:
            dst_shot_f = self.dst_version_dir + "/" + self.kekedou_ma_file_name
            # 保存文件
            with open(dst_shot_f, "w") as f:
                for b in self.blocks_list:
                    # 转换内容
                    b = self.convert_block(b)
                    if b:
                        f.write(b)

        print("---------------------")
        print("END <<<<<<<<<")

    def convert_block(self, b):
        reference_cam = False
        # 处理引用文件
        if b.startswith("file -r ") or b.startswith("file -rdi "):
            reference_file = re.findall(r"\"[a-zA-Z]+\"[\s\S]* \"(.+?)\"", b)[0]  # get reference file

            if reference_file.endswith("camRig.ma") or reference_file.endswith("camera_template.ma"):
                reference_cam = True

            if reference_file not in self.__ref_replace_map.keys():
                if reference_file not in self.__ref_replace_map.keys():
                    process_reference_file =  process_reference(reference_file)
                    if process_reference_file:
                        self.__ref_replace_map[reference_file] = process_reference_file

            # 拷贝参考引用到引用文件夹
            if reference_file not in self.__ref_replace_map.keys():
                #print("\nReference: %s\n" % reference_file)
                to_kekedou_file = self.copy_reference(reference_file)
                to_kekedou_file = to_kekedou_file.replace("I:/projects/nzt/to_kekedou", "$SERVER_ROOT")
                self.__ref_replace_map[reference_file] = to_kekedou_file

            b = b.replace(reference_file, self.__ref_replace_map[reference_file])

        # sound
        elif b.startswith("createNode audio -n "):
            wav_files = re.findall(r'\"string" "(.+\.wav)\";', b)  # get sound
            for wav_f in wav_files:
                kekedou_wav_file = self.dst_version_dir + "/sound/" + wav_f.split("/sound/")[-1]
                kekedou_wav_file = kekedou_wav_file.replace("I:/projects/nzt/to_kekedou", "$SERVER_ROOT")
                b = b.replace(wav_f, kekedou_wav_file)

        # 处理 abc 缓存
        elif b.startswith("createNode AlembicNode -n "):
            fs = re.findall(r"[\S\s]+? \"string\" \"(.+?\.abc)\"", b)  # get abc file
            fs += re.findall(r"[\S\s]+? \"stringArray\" \d \"(.+?\.abc)\"", b)
            if fs:
                for abc_file in fs:
                    if os.path.exists(abc_file):
                        dst_abc_folder = self.dst_version_dir + "/reference/cache"
                        if not os.path.exists(dst_abc_folder):
                            os.makedirs(dst_abc_folder)
                        dst_abc_file = dst_abc_folder + "/" + os.path.basename(abc_file)
                        print("%s =copy=> %s" % (abc_file, dst_abc_file))
                        if not os.path.exists(dst_abc_file):
                            shutil.copy2(abc_file, dst_abc_file)
                        b = b.replace(abc_file, dst_abc_file)

        # 处理参考文件
        elif b.startswith("createNode file -n") or \
                b.startswith("createNode gpuCache -n") or \
                b.startswith("createNode movie -n"):
            fs = re.findall(r"[\S\s]+? \"string\" \"(.+?\..+?)\"", b)  # get abc file
            if fs:
                for ref_file in fs:
                    if not ref_file:
                        continue

                    if "I:/projects/nzt/to_kekedou" in ref_file:
                        continue

                    if "I:/projects/nzt/from_kekedou" in ref_file:
                        continue

                    dst_ref_folder = self.dst_version_dir + "/reference"
                    if not os.path.exists(dst_ref_folder):
                        os.makedirs(dst_ref_folder)

                    if os.path.exists(ref_file):
                        glob_str = os.path.dirname(ref_file) + "/" + os.path.basename(ref_file)[:2] + "*"
                        all_ref_files = glob.glob(glob_str)
                        for src_ref_file in all_ref_files:
                            dst_ref_file = dst_ref_folder + "/" + os.path.basename(src_ref_file)
                            print("%s =copy=> %s" % (ref_file, dst_ref_folder + "/" + os.path.basename(ref_file)))
                            if not os.path.exists(dst_ref_file):
                                shutil.copy2(src_ref_file, dst_ref_file)

                        b = b.replace(ref_file, dst_ref_folder + "/" + os.path.basename(ref_file))

                    else:
                        if "<f>" in os.path.basename(ref_file):
                            glob_str = os.path.dirname(ref_file) + "/" + os.path.basename(ref_file).split("<f>")[0] + "*"
                            all_ref_files = glob.glob(glob_str)
                            for src_ref_file in all_ref_files:
                                dst_ref_file = dst_ref_folder + "/" + os.path.basename(src_ref_file)
                                print("%s =copy=> %s" % (src_ref_file, dst_ref_file))
                                if not os.path.exists(dst_ref_file):
                                    shutil.copy2(src_ref_file, dst_ref_file)

                            b = b.replace(os.path.dirname(ref_file), os.path.dirname(dst_ref_file))

        # 删除本地创建的相机
        if b.startswith("createNode camera -n "):
            if reference_cam:
                b = ""
            else:
                if "cam_rig:camAniShape" in b:
                    pass
                elif "cam_rig:camShape" in b:
                    pass
                else:
                    b = ""

        b = b.replace("I:/projects/nzt/from_kekedou", "$SERVER_ROOT")
        b = b.replace("I:/projects/nzt/to_kekedou", "$SERVER_ROOT")
        return b


if __name__ == "__main__":
    b = '	setAttr ".f" -type "string" "I:/projects/nzt/shot/i20/i20010/ani/i20010.ani.animation.v001/sound/i20.aud.audio.v001/i20010.wav";'
    audit = re.findall(r'\"string" "(.+\.wav)\";', b)[0]
    print(audit)
    # a = get_translated_data("i10240")
    # print(a)
    # oct_shot_list = ["i20590", "i20590", "i20610",
    #                  "i20880", "i20980", "i20995",
    #                  "i20640", "i20730", "i20940", "i10120"]
    #
    # for shot_name in oct_shot_list:
    #     pub_file = get_ani_file_from_shot(shot_name)
    #     print(pub_file)
    #     otok = OCTToKEKEDOU(pub_file)
    #     otok.oct_from_kekedou(cover=True)
