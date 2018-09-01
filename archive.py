import datetime as dt
import fnmatch
import glob
import logging
import os
import re
import shutil
import uuid
import zipfile
from pathlib import Path

ARCHIVE_PATTERN = '{name}_{date}_{rand}'
ARCHIVE_ZIP_SUFFIX = '.archive.zip'
ARCHIVE_PARSE_PATTERN = \
    r'(?P<name>.*?)_(?P<y>[0-9]{4})(?P<m>[0-9]{2})(?P<d>[0-9]{2})_(?P<rand_str>.{6})' + ARCHIVE_ZIP_SUFFIX


def _zipdir(path, zf):
    for root, dirs, files in os.walk(path):
        for f in files:
            zf.write(os.path.join(root, f), arcname=os.path.join(os.path.relpath(root, path), f))


def archive_directory(name, in_dir, out_dir, ttl=7, file_masks=['*'], purge=False,
                      pre_exec=None, pre_exec_args=[], post_exec=None, post_exec_args=[]):
    """Archive files in a directory.

        Arguments:
        name        -- the name of this archive task
        in_dir      -- the directory to archive
        out_dir     -- the directory to store archived zip file
        Keyword arguments:
        ttl         -- time-to-live for the archived zip file, in day
        file_masks  -- list of file mask to filter files to archive
        purge       -- whether to clean the content within in_dir
        pre_exec    -- function to execute before the archive task
        post_exec   -- function to execute after the archive task
    """

    if in_dir is None or out_dir is None:
        raise ValueError("Output/Input directory is None.")

    _log = logging.getLogger('archive_dir')

    date_str = dt.date.today().strftime('%Y%m%d')
    archive_workspace = os.path.join(out_dir,
                                     ARCHIVE_PATTERN.format(name=name, date=date_str, rand=uuid.uuid4().hex[:6]))
    archive_file = archive_workspace + ARCHIVE_ZIP_SUFFIX

    in_path = Path(in_dir)
    out_path = Path(out_dir)
    if out_path in in_path.parents:
        raise ValueError("Output directory cannot be under input directory.")
    if os.path.normpath(in_dir.lower()) == os.path.normpath(out_dir.lower()):
        raise ValueError("Input directory cannot be same as output directory.")

    if pre_exec is not None:
        _log.info("%s - Pre-executing task...", name)
        ret = pre_exec(*pre_exec_args)
        _log.info("%s - Pre-executed task, ret=%s", name, str(ret))

    if os.path.exists(in_dir):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        os.makedirs(archive_workspace)

        pending_files = []

        # calculate files to archive and copy them
        for root, dirs, files in os.walk(in_dir):
            for f in files:
                matched = False
                for pat in file_masks:
                    matched = fnmatch.fnmatch(f, pat)
                    print(matched)
                    if matched:
                        break

                if matched:
                    path = os.path.join(root, f)
                    pending_files.append(path)

                    # maintain folder structure
                    relative_path = os.path.relpath(path, in_dir)
                    out_sub_folder = os.path.join(archive_workspace, os.path.split(relative_path)[0])
                    if not os.path.exists(out_sub_folder):
                        os.makedirs(out_sub_folder)

                    # copy file
                    shutil.copy(path, os.path.join(out_sub_folder, f))

        _log.info("%s - Found %d files", name, len(pending_files))

        # zip the tmp folder
        zf = zipfile.ZipFile(archive_file, "w")
        _zipdir(archive_workspace, zf)
        zf.close()

        # remove temp workspace
        shutil.rmtree(archive_workspace)

        _clean_archive(out_dir, ttl)

        if purge:
            for f in os.listdir(in_dir):
                path = os.path.join(in_dir, f)
                if os.path.isfile(path):
                    os.remove(path)
                if os.path.isdir(path):
                    shutil.rmtree(path)

        if post_exec is not None:
            _log.info("%s - Post-executing task...", name)
            ret = post_exec(*post_exec_args)
            _log.info("%s - Post-executed task, ret=%s", name, str(ret))

        _log.info("%s - Archived and clean.", name)
    else:
        raise ValueError("Input directory not exist")


def _clean_archive(archive_dir, ttl):
    _log = logging.getLogger('clean_archive')
    files = glob.glob(os.path.join(archive_dir, '*' + ARCHIVE_ZIP_SUFFIX))
    today = dt.date.today()

    for f in files:
        file_date = _parse_filename_to_date(os.path.basename(f))
        delta = today - file_date
        if delta.days > ttl:
            os.remove(f)
            _log.info("Removed %s", f)


def _parse_filename_to_date(name):
    match = re.match(ARCHIVE_PARSE_PATTERN, name)

    if match is None:
        return None

    return dt.date(int(match.group('y')), int(match.group('m')), int(match.group('d')))


def main():
    archive_directory("test", '/Users/123/Documents/Python/TESTER/archive/in', '/Users/123/Documents/Python/TESTER/archive/out', file_masks='*.py')


if __name__ == "__main__":
    main()
