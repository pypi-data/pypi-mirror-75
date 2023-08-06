# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
from contrast.extern.wrapt import register_post_import_hook
from contrast.agent.assess import patch_manager
from contrast.applies.xxe import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance


MODULE = "xml.dom.pulldom"
PARSE = "parse"
PARSESTRING = "parseString"


def parse(original_parse, patch_policy=None, *args, **kwargs):
    return apply_rule(MODULE, PARSE, original_parse, args, kwargs)


def parse_string(original_parsestring, patch_policy=None, *args, **kwargs):
    return apply_rule(MODULE, PARSESTRING, original_parsestring, args, kwargs)


def patch_pulldom(pulldom_module):
    # TODO: PYT-916 add after file/io support
    # patch_cls_or_instance(pulldom_module, PARSE, parse_string)
    patch_cls_or_instance(pulldom_module, PARSESTRING, parse_string)


def register_patches():
    register_post_import_hook(patch_pulldom, MODULE)


def reverse_patches():
    xml_pulldon = sys.modules.get(MODULE)
    if not xml_pulldon:
        return

    patch_manager.reverse_patches_by_owner(xml_pulldon)
