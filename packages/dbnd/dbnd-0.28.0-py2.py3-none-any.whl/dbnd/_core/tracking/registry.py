"""
Tracking store backends registry
"""

import logging
import typing

from dbnd._core.errors import friendly_error
from dbnd._core.plugin.dbnd_plugins import assert_web_enabled
from dbnd._core.tracking.backends import (
    CompositeTrackingStore,
    ConsoleStore,
    FileTrackingStore,
    TbSummaryFileStore,
    TrackingStore,
    TrackingStoreThroughChannel,
)
from dbnd._core.tracking.backends.channels import (
    ConsoleDebugTrackingChannel,
    DisabledTrackingChannel,
    TrackingChannel,
    TrackingWebChannel,
)


logger = logging.getLogger(__name__)


def tracking_store_through_db_channel_builder():
    """
                                                        ctx (+DB)
                                                            |
    DBND -> TrackingStoreThroughChannel -> WebChannel -> ApiClient -> HTTP -> Flask -> Views -x-> TrackingApiHandler -> TrackingDbService -> SQLA -> DB
                                      \ -> DBChannel ---------------------------------------------------------------/
    """
    assert_web_enabled(
        "It is required when trying to use local db connection (tracker_api=db)."
    )
    from dbnd_web.app import activate_dbnd_web_context
    from dbnd_web.api.v1.tracking_api import TrackingApiHandler as DirectDbChannel

    # DirectDbChannel requires DB session, it's available in Flask Context
    activate_dbnd_web_context()
    return TrackingStoreThroughChannel(channel=DirectDbChannel())


_BACKENDS_REGISTRY = {
    "file": FileTrackingStore,
    "console": ConsoleStore,
    "debug": lambda: TrackingStoreThroughChannel(channel=ConsoleDebugTrackingChannel()),
    ("api", "web"): lambda: TrackingStoreThroughChannel(channel=TrackingWebChannel()),
    ("api", "db"): tracking_store_through_db_channel_builder,
    ("api", "disabled"): lambda: TrackingStoreThroughChannel(
        channel=TrackingWebChannel()
    ),
}


def register_store(name, store_builder):
    if name in _BACKENDS_REGISTRY:
        raise Exception("Already registered")
    _BACKENDS_REGISTRY[name] = store_builder


def get_tracking_store(tracking_store_names, api_channel_name, tracker_raise_on_error):
    # type: (...) -> TrackingStore
    tracking_store_instances = []
    for name in tracking_store_names:
        if name == "api":
            name = (name, api_channel_name)
        tracking_store_builder = _BACKENDS_REGISTRY.get(name)
        if tracking_store_builder is None:
            friendly_error.config.wrong_store_name(name)
        instance = tracking_store_builder()
        tracking_store_instances.append(instance)

    return (
        tracking_store_instances[0]
        if len(tracking_store_instances) == 1
        else CompositeTrackingStore(
            tracking_stores=tracking_store_instances,
            raise_on_error=tracker_raise_on_error,
        )
    )
