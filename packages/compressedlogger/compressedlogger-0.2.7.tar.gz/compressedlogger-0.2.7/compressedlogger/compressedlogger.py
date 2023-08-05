from typing import BinaryIO
from logging import LogRecord, Handler
import gzip, os, pathlib, re, datetime


class CompressedLogger(Handler):
    """
    Simple Logging Handler for the python logging module

    This CompressedLogger is a handler that can be used in the python
    built-in logging module. It writes the log directly into
    a compressed *.gz file using the gzip module.

    Due to gzip compression the actual log file is updated in steps
    of about 200kb, therefore the log rotation based on file size
    can be delayed by some kb.
    """
    def __init__(self, log_path: str, filename: str, single_max_size: int, overall_size: int, header: str = ""):
        """
        :param log_path: path where the log files should be stored
        :param filename: base name of the logfile
        :param single_max_size: maximum size in MB of a single zipped file
        :param overall_size: maximum cumulative size of all written logfiles
        :param header: header that is written into every new logfile on rotation
        """
        Handler.__init__(self)
        self.filename = filename
        self.base_path = self.ensure_path(log_path)
        self.single_max_size: int = single_max_size * 1024 * 1024
        self.overall_size: int = overall_size * 1024 * 1024
        self.header: str = header
        self.log_file: BinaryIO = None
        self.gzip_file: gzip.GzipFile = None
        self.current_archive_path: str = ""
        self.current_log_ts: datetime.datetime = datetime.datetime.now()
        self._open_new_log_file()
        self._delete_old_logs()

    @staticmethod
    def ensure_path(path: str):
        if not os.path.exists(path):
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return pathlib.Path(path)

    def close(self):
        self._delete_old_logs()
        if self.gzip_file is not None:
            self.gzip_file.close()
        if self.log_file is not None:
            self.log_file.close()

    def emit(self, record: LogRecord) -> None:
        """
        Emit the record

        Output the record to the file, rotates the log file if necessary
        """
        if self.log_file is None or self.gzip_file is None:
            return
        if self._rotate_log():
            self._open_new_log_file()
            self._delete_old_logs()

        msg = (self.format(record) + "\n").encode()
        self.gzip_file.write(msg)

    def _open_new_log_file(self):
        """
        Close the current logfile and open a new one

        """

        if self.gzip_file is not None:
            self.gzip_file.close()
        if self.log_file is not None:
            self.log_file.close()
        self.current_archive_path = self._next_archive_name()
        self.log_file = open(self.current_archive_path, 'wb')
        self.gzip_file = gzip.GzipFile(filename=self.filename,
                                       fileobj=self.log_file)
        if len(self.header) > 0:
            self.gzip_file.write((self.header + "\n").encode())
        self.current_log_ts = datetime.datetime.now()

    def _delete_old_logs(self):
        """
        Remove old log files when overall_size limit was reached

        This function removes the oldest log files until the
        cumulative size of all log files is below the overall_size
        """
        if self.overall_size == -1:
            return
        total_size = 0
        log_files = [str(x) for x in self.base_path.glob("*")]
        for file in log_files:
            total_size += os.path.getsize(file)
        if len(log_files) == 0:
            return

        log_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
        while total_size > self.overall_size:
            del_file = log_files.pop()
            total_size -= os.path.getsize(del_file)
            os.remove(del_file)

    def _rotate_log(self) -> bool:
        """
        Check whether the logfile should rotate or not

        returns 'true' if the current log files size exceeds a given size
        or if the day has changed.
        """
        if self.single_max_size != -1 and self.log_file.tell() >= self.single_max_size:
            return True
        if self.current_log_ts.date() < datetime.datetime.now().date():
            return True
        return False

    def _next_archive_name(self) -> str:
        """
        Creates a logname base on the filename given on init.
        This creates a file name based on following scheme:
            {filename}-{current_date}.{log_number}.gz
            e.g. logfile-2020-07-10.1.gz
        """
        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        base_name = str(self.base_path / self.filename) + "-" + todays_date
        new_name = base_name + "." + self._get_next_log_id() + "." + "gz"
        return new_name

    def _get_next_log_id(self):
        """
        Checks the logs that were written on the current date
        and returns the next following log_id
        """
        todays_logs = [str(x) for x in self.base_path.glob("*")]
        used_ids = set()
        for log in todays_logs:
            used_ids.update(re.findall("[.][0-9]*[.]", log))
        if len(used_ids) == 0:
            return "1"
        max_id = 1
        for log_id in used_ids:
            try:
                other_id = int(log_id.replace(".", ""))
            except ValueError:
                other_id = 1
            max_id = max(max_id, other_id)
        return str(max_id + 1)


