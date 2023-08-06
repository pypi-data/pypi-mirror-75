# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.extern import six
from contrast.agent.protect.rule.xxe_rule import Xxe
from contrast.agent.settings_state import SettingsState
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


METHOD_TO_KWARG_MAP = {"fromstring": "text", "parseString": "string"}


def apply_rule(module, method, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled():
        xml = get_user_input(method, args, kwargs)
        protect_rule(context, module, xml)

    return orig_func(*args, **kwargs)


@fail_safely("Failed to get user input for XXE Rule")
def get_user_input(method, args, kwargs):
    if args:
        return args[0]
    if kwargs:
        kwarg = METHOD_TO_KWARG_MAP[method]
        return kwargs.get(kwarg)

    return None


@fail_safely("Failed to run protect XXE Rule")
def protect_rule(context, framework, xml):
    if not xml or not framework:
        return

    rule = SettingsState().defend_rules[Xxe.NAME]

    if not rule or not rule.enabled:
        return

    rule.infilter(context, six.ensure_str(xml), framework=framework)
