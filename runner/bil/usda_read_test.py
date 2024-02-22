# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Author     ：YangTao
Time       ：2023/9/4 14:38
"""
import pprint

from toolsets.tools.flo.usd_reader import usd_modifier
from toolsets.tools.flo.usd_reader import usd_reader
from toolsets.tools.flo.usd_creation import cache_usd_creator



def remove_cache_usd_variant(usda_file, v_name):
    from toolsets.tools.flo.usd_reader import usd_modifier
    from toolsets.tools.flo.usd_reader import usd_reader

    variant_name = "cacheVariant"
    prim_path = "/high"
    version_name = v_name.replace('.', '-')

    usdr = usd_reader.UsdReader()
    usdr.usd_file = usda_file
    usd_info = usdr.list_variants(variant_key=variant_name)
    if version_name in usd_info:
        source = usd_modifier.Sdf.Layer.FindOrOpen(usda_file)
        usd_modifier.Sdf.Layer.ReloadLayers(usd_modifier.Sdf.Layer.GetLoadedLayers())
        prim = source.pseudoRoot.GetPrimAtPath(prim_path)

        usd_modifier.remove_variant(prim=prim,
                                    variant_set_name=variant_name,
                                    variant_name=version_name)

        print(prim, variant_name, version_name)
        usdr.stage.GetRootLayer().Save()

    del usdr.stage

comp = "lion_dance_big"
v_name = "n10160.ani.animation.v013"
entity_code = "n10160"
proj = "bil"

# from toolsets.tools.flo.usd_creation import cache_usd_creator
# creator = cache_usd_creator.AnimatedCacheUsdCreator(comp, v_name, entity_code, proj)
# usda_file = creator.get_cache_root_usd()
# remove_cache_usd_variant(usda_file, v_name)

usda_file = "I:/projects/bil/cache/n10/n10160/cam/cam.usda"
usdr = usd_reader.UsdReader()
usdr.usd_file = usda_file
