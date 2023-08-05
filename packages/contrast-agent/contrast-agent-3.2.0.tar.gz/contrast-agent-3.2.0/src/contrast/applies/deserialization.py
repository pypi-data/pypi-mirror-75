# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import six

import contrast
from contrast.agent.protect.rule.deserialization_rule import Deserialization
from contrast.agent.settings_state import SettingsState
from contrast.utils.decorators import fail_safely
from contrast.utils.stack_trace_utils import StackTraceUtils


@fail_safely("Failed to run protect Deserialization Rule")
def protect_rule(context, value, deserializer):
    if context is None:
        return

    if not value or not isinstance(value, (six.string_types, six.binary_type)):
        return

    rule = SettingsState().defend_rules[Deserialization.NAME]

    if rule is None or not rule.enabled:
        return

    stack_elements = StackTraceUtils.build(ignore=True)

    value = six.ensure_text(value)
    rule.infilter(
        context, value, deserializer=deserializer, stack_elements=stack_elements
    )


def apply_rule(orig_func, deserializer, value, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context and SettingsState().is_protect_enabled():
        protect_rule(context, value, deserializer)

    return orig_func(*args, **kwargs)
