# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/26 17:23
"""
import glob
import os.path
import re
import shutil
import filecmp


def blocks_list(ma_file):
    # 将 ma 文件切分为列表
    separators = ["requires", "file -r ", "file -rdi ",
                  "createNode ", "requires ", "currentUnit ",
                  "fileInfo ", "select ", "connectAttr ",
                  "dataStructure ", "// End of "]
    regular_exp = "(" + "|".join(map(re.escape, separators)) + ")"

    with open(ma_file, "r") as f:
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

def tran_assets(src_file):
    print("#### tran sourceimages: ", src_file)

    new_ma_context = ""
    for b in blocks_list(src_file):
        if b.startswith("createNode file -n "):
            fs = re.findall(r"[\S\s]+? \"string\" \"(.+?\..+?)\"", b)  # get abc file
            if fs:
                for tex_file in fs:
                    # 转为现在资产路径
                    new_tex_file = get_sourceimages_file(tex_file)
                    if os.path.exists(new_tex_file):
                        print(tex_file, "== replace ==", new_tex_file)
                        b = b.replace(tex_file, new_tex_file)
        new_ma_context += b

    with open(src_file, "w") as new_f:
        new_f.write(new_ma_context)

def get_new_asset_file(asset_f):
    # I:/dsf/Asset/CH/Yu_ZhenS_b/RIG/dsf_Yu_ZhenS_b_RIG.ma
    asset_type = asset_f.split("/")[3]  # CH
    asset_name = asset_f.split("/")[4]  # Yu_ZhenS_b
    asset_step = asset_f.split("/")[5]  # RIG_eye

    # I:/dsf.bak/Asset/CH/Yu_ZhenS_b/RIG/Yu_ZhenS_b.rig.RIG/Yu_ZhenS_b.ma
    bak_file = "I:/dsf.bak/Asset/%s/%s/%s/%s.%s.%s/%s.ma" % (asset_type,
                                                             asset_name,
                                                             asset_step.lower().split("_")[0],
                                                             asset_name,
                                                             asset_step.lower().split("_")[0],
                                                             asset_step.upper(),
                                                             asset_name)
    if not os.path.isfile(bak_file):
        print("not found %s" % bak_file)
        return bak_file

    copy_dst_file = bak_file.replace("I:/dsf.bak", "Z:/DS/Temp/dsf")

    copy_dst_p = os.path.dirname(copy_dst_file)
    if not os.path.exists(copy_dst_p):
        os.makedirs(copy_dst_p)

    if not os.path.exists(copy_dst_file):
        print("copy %s ==> %s" % (bak_file, copy_dst_file))
        shutil.copyfile(bak_file, copy_dst_file)

        # 拷贝贴图
        tran_assets(copy_dst_file)

    return copy_dst_file


def tran(src_file):
    base_name = os.path.basename(src_file)
    pure_name = os.path.splitext(base_name)[0]
    ext = os.path.splitext(base_name)[-1]
    f_path = os.path.dirname(src_file)
    new_file = os.path.join(f_path, "%s.%s%s" % (pure_name, "tran", ext))

    # if os.path.exists(new_file):
    #     return

    print("@@@@@: ", new_file)

    new_ma_context = ""
    for b in blocks_list(src_file):
        if b.startswith("file -r ") or b.startswith("file -rdi "):
            reference_file = re.findall(r"\"[a-zA-Z]+\"[\s\S]* \"(.+?)\"", b)[0]  # get reference file
            new_reference_file = get_new_asset_file(reference_file)
            b = b.replace(reference_file, new_reference_file)

        new_ma_context += b

    with open(new_file, "w") as new_f:
        new_f.write(new_ma_context)


copyed_sourceimages_paths = []
def get_sourceimages_file(src_file):
    # I:/dsf/Asset/CH/HT_ZhenS/RIG/sourceimages/dsf_HT_ZhenS_fur_baseclr.jpg
    if "sourceimages" not in src_file:
        return src_file

    old_sourceimages_path = src_file.split("sourceimages")[0] + "sourceimages"  # I:/dsf/Asset/CH/HT_ZhenS/RIG/sourceimages
    asset_type = src_file.split("/")[3]  # CH
    asset_name = src_file.split("/")[4]  # HT_ZhenS
    asset_step = src_file.split("/")[5]  # RIG

    bak_sourceimages_path = "I:/dsf.bak/Asset/%s/%s/%s/%s.%s.%s/sourceimages" % (asset_type,
                                                                                 asset_name,
                                                                                 asset_step.lower().split("_")[0],
                                                                                 asset_name,
                                                                                 asset_step.lower().split("_")[0],
                                                                                 asset_step.upper())
    if not os.path.exists(bak_sourceimages_path):
        print("not found %s" % bak_sourceimages_path)
        return src_file

    # I:/dsf.bak/Asset/CH/HT_ZhenS/rig/HT_ZhenS.rig.RIG
    dst_sourceimages_path = bak_sourceimages_path.replace("I:/dsf.bak", "Z:/DS/Temp/dsf")
    # 拷贝贴图
    if dst_sourceimages_path not in copyed_sourceimages_paths:
        # 根路径
        dst_sourceimages_root_path = os.path.dirname(dst_sourceimages_path)
        if not os.path.exists(dst_sourceimages_root_path):
            os.makedirs(dst_sourceimages_root_path)

        # 移除贴图
        if os.path.isdir(dst_sourceimages_path):
            shutil.rmtree(dst_sourceimages_path)
        print("%s =copy=> %s" % (bak_sourceimages_path, dst_sourceimages_path))
        shutil.copytree(bak_sourceimages_path, dst_sourceimages_path)
        copyed_sourceimages_paths.append(dst_sourceimages_path)

    new_file = src_file.replace(old_sourceimages_path, dst_sourceimages_path)
    return new_file


# p = "I:/dsf/Asset/CH/HT_ZhenS/RIG/sourceimages/dsf_HT_ZhenS_fur_baseclr.jpg"
# get_sourceimages_file(p)

# 拷贝资产材质
# p = "Z:/DS/Temp/dsf/Asset/PROP/TZ/RIG/TZ.rig.RIG/TZ.ma"
# tran_assets(p)

# # 批量拷贝资产贴图
# for ma_file in glob.glob("Z:/DS/Temp/dsf/Asset/*/*/*/*/*.ma"):
#     # 备份源文件
#     file_name = os.path.basename(ma_file)
#     if file_name.startswith("orig."):
#         continue
#
#     print("Asset File:", os.path.basename(ma_file))
#
#     file_path = os.path.dirname(ma_file)
#     orig_file = file_path + "/orig." + file_name
#
#     if os.path.exists(orig_file):
#         shutil.copy2(orig_file, ma_file)
#     else:
#         print("backup %s ==> %s" % (ma_file, orig_file))
#         shutil.copy2(ma_file, orig_file)
#
#     tran_assets(ma_file)

tran("Z:/DS/Temp/ani/27_008/an/27_008.an.An.v107/27_008.an.An.v107.ma")

# for src_file in glob.glob("Z:/DS/Temp/ani/*/*/*.ma"):
#     if ".tran." in os.path.basename(src_file):
#         continue
#
#     tran(src_file)
