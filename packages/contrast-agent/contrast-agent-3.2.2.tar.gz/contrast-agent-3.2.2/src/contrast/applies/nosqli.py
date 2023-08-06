# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import json
import contrast
from contrast.extern import six
from contrast.utils.decorators import fail_safely
from contrast.agent.settings_state import SettingsState
import logging

logger = logging.getLogger("contrast")


def apply_rule(database, method, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    query = get_query(method, args, kwargs)

    if context and SettingsState().is_protect_enabled():
        protect_rule(database, method, query)

    return orig_func(*args, **kwargs)


def get_query(method, args, kwargs):
    query = None
    if len(args) > 1:
        query = args[1]
        # TODO: PYT-873 update method needs args[2]?
    elif kwargs:
        query = _get_query_from_kwargs(kwargs, method)

    return query


def _get_query_from_kwargs(kwargs, method):
    if method == "find":
        query = kwargs.get("filter")
    elif method == "insert_one" or "update" in method:
        query = kwargs.get("document")
    elif method == "insert_many":
        query = kwargs.get("documents")
    elif "delete" in method:
        query = kwargs.get("criteria")

    return query


@fail_safely("Failed to run protect NoSQLi Rule")
def protect_rule(database, method, sql):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if sql is None or context is None:
        return

    context.activity.query_count += 1
    context.activity.technologies[database] = True

    rule = SettingsState().defend_rules["nosql-injection"]

    if rule is None or not rule.enabled:
        logger.debug("No nosql-injection rule to apply!")
        return

    if not isinstance(sql, (str, bytes)):
        sql = nosql_to_json(sql)
        if sql is None:
            return

    log_sql_query(method, sql)

    rule.infilter(context, sql, database=database)


@fail_safely("Failed to convert nosql input to JSON")
def nosql_to_json(nosql):
    try:
        return json.dumps(nosql)
    except TypeError:
        # may encounter TypeError: Object of type ObjectId is not JSON serializable
        # so let's just make it a string
        return str(nosql)


@fail_safely("Failed to log query for protect NoSQLi Rule", log_level="debug")
def log_sql_query(method, sql_query):
    """
    Attempt to log the sql query but do not fail if unable to do so.
    """
    logger.debug(
        "Applying Nosql injection rule %s=%s",
        method,
        six.ensure_str(sql_query, errors="replace"),
    )
