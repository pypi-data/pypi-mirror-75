#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import signal
import traceback

from dci_downloader import api
from dci_downloader import downloader
from dci_downloader.settings import get_settings, exit_if_settings_invalid
from dci_downloader.fs import create_temp_file


def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(130)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def download_components(settings, api, downloader, cert, key):
    if "component_id" in settings and settings["component_id"]:
        component_id = settings["component_id"]
        component = api.get_component_by_id(component_id)
        topic_id = component["topic_id"]
        topic = api.get_topic_by_id(topic_id)
        components = [component]
    else:
        topic = api.get_topic(settings["name"])
        components = api.get_components(topic)
    for component in components:
        downloader.download_component(topic, component, settings, cert, key)


def main():
    settings = get_settings(sys_args=sys.argv[1:], env_variables=dict(os.environ))
    exit_if_settings_invalid(settings)
    keys = api.get_keys(settings["remoteci_id"])
    if keys is None:
        print("Can't get certificate's keys, contact DCI administrator")
        sys.exit(0)
    cert = create_temp_file(keys["cert"]).name
    key = create_temp_file(keys["key"]).name
    return_code = 0
    for topic_settings in settings["topics"]:
        topic_name = topic_settings["name"]
        try:
            topic = api.get_topic(topic_name)
            if topic is None:
                raise Exception("Topic name %s not found" % topic_name)
            download_components(topic_settings, api, downloader, cert, key)
        except Exception:
            print("Exception when downloading components for %s" % topic_name)
            traceback.print_exc()
            return_code = 1
    os.unlink(cert)
    os.unlink(key)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
