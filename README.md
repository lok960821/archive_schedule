### Envirement Required
- python 3.X

### install

```bash 
pip3 install schedule
```

### How to use
```bash
rewrite in "archive_main.py"

routine.pre_filter_day_backup(mins, filepath, backup_path)
#[mins, filepath, backup_path]
# filepath = the file path need to be backup(filter by day)
# backup path = move the file into the path which is empty
# Xday = X * 60 * 24
# file modify time X day 

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
```

