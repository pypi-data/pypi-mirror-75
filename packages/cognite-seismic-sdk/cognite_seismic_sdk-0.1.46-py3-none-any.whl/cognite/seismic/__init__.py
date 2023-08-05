# Copyright 2019 Cognite AS

from cognite.seismic._api_client import CogniteSeismicClient

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

try:
    __version__ = importlib_metadata.version(__name__)
except:
    __version__ = "0.0.1local"
