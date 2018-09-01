import time
import schedule
import logging
import custom_routine as routine
from archive import archive_directory


formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s | %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logging.getLogger('').setLevel(logging.INFO)
logging.getLogger('').addHandler(sh)
_log = logging.getLogger('schedule')


def _setup_tasks():
    """
        # Sample usage
        # The task below will archive every day at 0 o'clock
        # , with the archived files able to be kept at least 7 days.
        # For detail usage, refer to the docstring at archive.archive_directory.

        schedule.every().day.at('00:00').do(
            archive_directory,
            name="test",
            in_dir='/home/ting/archive_test/in',
            out_dir='/home/ting/archive_test/out',
            ttl=7,
            file_masks='*.py',
            pre_exec=lambda : "Hello",
            post_exec=lambda : "World"
        )
        """

    # backup document
    schedule.every().day.at('01:05').do(
        archive_directory,
        name="document",
        in_dir='/Users/123/Documents/Python/TESTER/tmp',
        out_dir='/Users/123/Documents/Python/TESTER/archive',
        ttl= 30,
        purge= True,
        file_masks=['*'],
        pre_exec= routine.pre_filter_day_backup,
        pre_exec_args=[3*60*24,"/Users/123/Documents/Python/TESTER/inspection/reports","/Users/123/Documents/Python/TESTER/tmp"]
        # [mins, filepath, backup path]
        # filepath = the file path need to be backup(filter by day)
        # backup path = move the file into the path which is empty
        # Xday = X * 60 * 24
        # file modify time X day 
    )


if __name__ == "__main__":
    _setup_tasks()

    # DEBUG
    schedule.run_all()
    exit(0)

    [_log.info("JOB - %s", str(job)) for job in schedule.jobs]
    TEN_MINUTES = 60 * 10
    count = 1
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            _log.exception(e)
        finally:
            if count == TEN_MINUTES:
                [_log.info("JOB - %s", str(job)) for job in schedule.jobs]
                count = 0
            time.sleep(1)
            count += 1
