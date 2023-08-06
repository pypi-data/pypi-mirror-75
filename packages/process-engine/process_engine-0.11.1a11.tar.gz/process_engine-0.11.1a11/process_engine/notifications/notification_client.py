import logging 

from ..core import base_client

class NotifcationClient(base_client.BaseClient):
    def __init__(self, url, session=None, identity=None):
        super(NotifcationClient, self).__init__(url, session, identity)

    # siehe https://docs.google.com/document/d/1Vtx310N4B4MFSWeso_OfFmyKFXPvd6ZWGnjAm2fSI1s/edit#
    def on_process_started(self, callback):
        pass


