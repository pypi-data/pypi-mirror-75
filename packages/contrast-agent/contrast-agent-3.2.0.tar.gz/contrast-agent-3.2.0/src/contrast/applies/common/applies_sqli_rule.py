# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
NOTE: This API is deprecated in favor of the one provided by
contrast.applies.sqli. It should be removed once all SQL patches have been
updated to use the new rule.
"""
import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.settings_state import SettingsState
from contrast.applies.assess.applies_sqli_rule import apply_rule as assess_rule
from contrast.applies.protect.applies_sqli_rule import apply_rule as protect_rule


def apply_rule_sqlalchemy(database, action, orig_func, sql, obj, args, kwargs):
    """
    Universal method to run Protect and Assess on a patched function for SQl Alchemy

    Protect must occur first so we can block prior to original function if need be

    Assess must occur after so we can check the result of the function

    :param database: database being used
    :param action: method name used in driver
    :param orig_func: original patched function
    :param sql: str query
    :param obj: driver object, Example: Cursor()
    :param args: args used in action
    :param kwargs: kwargs used in action
    :return: result of original function
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context and SettingsState().is_protect_enabled():
        protect_rule(context, database, action, sql)

    try:
        result = orig_func(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        if not skip_analysis(context):
            with scope.contrast_scope():
                assess_rule(context, database, action, sql, obj, result, args, kwargs)

    return result
