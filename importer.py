#!/usr/bin/env python

from datetime import datetime, timedelta
import glob
import os
import shutil

# CARD_DIRECTORY = r"H:\DCIM\100EOS7D"
CARD_DIRECTORY = r"E:\Imports"
""" The directory to search for images """

ARCHVE_DIRECTORY = r"E:\Photo Archive"
""" The root directory of the archive """

TMP_DIRECTORY = "tmp"
""" A temporary work directory

    This should preferably be on the same filesystem as the archive
"""

EVENT_SPACING = timedelta(hours=3)
""" Minimum time between events """

def timestamp_for_path(file_path):
    """ Return the creation time for the file_path as datetime """
    timestamp = os.path.getmtime(file_path)
    date_object = datetime.fromtimestamp(timestamp)

    return date_object


def event_path_from_timestamp(timestamp):
    path_format = os.path.join("%Y", "%m %B", "%Y-%m-%d %H.%M")
    return timestamp.strftime(path_format)


def copy_file(from_path, to_path):
    print("cp '%s' '%s'" % (from_path, to_path))
    if os.path.exists(to_path):
        raise Exception("Could not copy file, destination exists")
    # shutil.copy2(from_path, to_path)


def move_file(from_path, to_path):
    print("mv '%s' '%s'" % (from_path, to_path))
    if os.path.exists(to_path):
        raise Exception("Could not move file, destination exists")

    shutil.move(from_path, to_path)


def copy_to_archive(from_path=CARD_DIRECTORY, to_path=ARCHVE_DIRECTORY):
    filename_format = "%Y-%m-%d %H.%M.%S "
    card_glob = os.path.join(from_path, "**", "*")

    previous_timestamp = datetime(1,1,1)
    event_path = ""
    files = [{"path": file_path, "timestamp": timestamp_for_path(file_path)}
             for file_path in glob.iglob(card_glob, recursive=True)
             if os.path.isfile(file_path)]
    for file_data in sorted(files, key=lambda x: x.get("timestamp")):
        file_path = file_data.get("path")
        if not os.path.isfile(file_path):
            continue

        filename = os.path.basename(file_path)

        current_timestamp = timestamp_for_path(file_path)
        if (current_timestamp - previous_timestamp) > EVENT_SPACING:
            event_path = os.path.join(
                    to_path,
                    event_path_from_timestamp(current_timestamp)
            )
            print(event_path)
            if os.path.exists(event_path):
                if not os.path.isdir(event_path):
                    raise Exception("Could not create event directory")
            else:
                os.makedirs(event_path)

        target_filename = (current_timestamp.strftime(filename_format) +
                            filename)
        target_path = os.path.join(to_path, event_path, target_filename)

        copy_file(file_path, target_path)

        previous_timestamp = current_timestamp


if __name__ == "__main__":
    copy_to_archive()
