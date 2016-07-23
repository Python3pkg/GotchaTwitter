import csv
import warnings
import traceback
from tqdm import tqdm
from requestsplus import RequestsPlus
from parser_utils import *
from parser_timeline import parse_user_timeline
from reader_utils import *
from datetime import datetime


class GotchaTwitter:

    def __init__(self, job, inputs, output_fp=None, **kwargs):
        """
        :param job: ['timeline', 'user', 'tweet', 'threads']
        :param inputs: Can use either list or filepath
        :param output_fp: Default <input_fp>.<job>

        :param input_column: Default 0. Can use either integer or dictionary. e.g. {'tid': 1, 'uid': 0}.
        :param input_delimiter: Default ','
        :param input_start_from: Default None

        :param output_delimiter: Default ','
        :param output_mode: Default 'a'
        """
        self._job, self._output_extension = read_job(job)

        self._input_column = kwargs.get('input_column', 0)
        self._input_delimiter = kwargs.get('input_delimiter', ',')
        self._input_start_from = kwargs.get('start_from')
        self._inputs = inputs

        self._output_fp = output_fp
        self._output_delimiter = kwargs.get('output_delimiter', ',')
        self._output_mode = kwargs.get('output_mode', 'a')
        self._output_header = read_header(self._job, kwargs.get('output_header'))
        self._output_has_header = True if self._output_mode == 'w' else False

        self._connector = RequestsPlus(header=HEADERS)

        self._notifier = read_notifier(kwargs.get('notifier'), kwargs.get('notifier_creadential_fp'))

        self._parser_conf = kwargs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __hash__(self):
        return id(self)

    def close(self):
        self._notifier.notify(self._input_fp + self._output_extension + 'is done!',
                              datetime.now().strftime('%Y-%m-%d %H:%M%S'))

    def parse(self, item):
        parsers = {'timeline': parse_user_timeline(item, self._connector, self._output_header, **self._parser_conf)}
        return parsers.get(self._job)

    def crawl(self):
        self._input_fp, self._input = \
            read_input(self._inputs, self._input_column, self._input_delimiter, self._input_start_from)
        self._output_fp = self._output_fp if self._output_fp else self._input_fp + self._output_extension

        with tqdm(self._input) as _inputs, open(self._output_fp, self._output_mode) as o, open('error.log', 'a') as el:
            csvwriter = csv.writer(o, delimiter=self._output_delimiter)

            if self._output_has_header:
                csvwriter.writerow(self._output_header)

            for _input in _inputs:
                _inputs.set_description(_input)

                try:
                    parsed_items = self.parse(_input)
                    for parsed_item in parsed_items:
                        try:
                            if parsed_item:
                                csvwriter.writerow(parsed_item)
                        except:
                            print parsed_item
                except KeyboardInterrupt:
                    break
                except:
                    el.write(_input + '\n')
                    print traceback.format_exc()

    def set_input(self, input_column=0, input_delimiter=',', input_start_from=None):
        self._input_column = input_column
        self._input_delimiter = input_delimiter
        self._input_start_from = input_start_from
        return self

    def set_output(self, header=None, save_mode='a', delimiter=',', has_header=True):
        self._output_header = read_header(self._job, header)
        self._output_mode = save_mode
        self._output_delimiter = delimiter
        self._output_has_header = has_header
        return self

    def set_notifier(self, notifier_type, credential_fp=None, access_token=None):
        self._notifier = read_notifier(notifier_type, credential_fp, access_token)
        return self

    def set_parser(self, **conf):
        self._parser_conf = conf
        return self