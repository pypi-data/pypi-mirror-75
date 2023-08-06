# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent.settings_state import SettingsState
from contrast.applies.protect.applies_pt_rule import apply_rule as protect_rule


def apply_rule(module, method, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled():
        protect_rule(context, method, args, kwargs)

    return orig_func(*args, **kwargs)
