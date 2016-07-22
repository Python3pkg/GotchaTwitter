import csv
import warnings
from tqdm import tqdm
from requestsplus import RequestsPlus
from parser_utils import *
from parser_timeline import parse_user_timeline
from reader_utils import *


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
        self._job = read_job(job)
        self._input_fp, self._input = self.get_input(inputs, **kwargs)
        self._output_fp = output_fp if output_fp else self._input_fp + '.' + self._job
        self._output_delimiter = kwargs.get('output_delimiter', ',')
        self._output_mode = kwargs.get('output_mode', 'a')
        self._output_header = read_header(self._job, **kwargs)
        self._output_has_header = True if self._output_mode == 'w' else False
        self._connector = RequestsPlus(header=HEADERS)
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __hash__(self):
        return id(self)

    def close(self):
        pass

    @staticmethod
    def get_input(inputs, input_column=0, input_delimiter=',', input_start_from=None, **kwargs):
        # return input_fp, input_list
        input_fp = ''
        if isinstance(inputs, str):
            input_fp = inputs
            with open(input_fp, 'r') as i:
                csvreader = csv.reader(i, delimiter=input_delimiter)
                if isinstance(input_column, int):
                    inputs = [line[input_column] for line in csvreader]
                if isinstance(input_column, dict):
                    inputs = [line[input_column.get('tid', 1)] + '@' +
                              line[input_column.get('uid', input_column.get('screen_name', 0))]
                              for line in csvreader]
        if isinstance(inputs, list):
            input_fp = '_'

        if input_start_from:
            try:
                start_index = inputs.index(input_start_from)
            except:
                warnings.warn('Start from value %s is not found.' % input_start_from, Warning)
                start_index = 0
        else:
            start_index = 0
        return input_fp, inputs[start_index:]

    def parse(self, item):
        parsers = {'timeline': parse_user_timeline(item, self._connector, self._output_header)}
        return parsers.get(self._job)

    def crawl(self):
        with tqdm(self._input) as _inputs, open(self._output_fp, self._output_mode) as o:
            csvwriter = csv.writer(o, delimiter=self._output_delimiter)

            if self._output_has_header:
                csvwriter.writerow(self._output_header)

            for _input in _inputs:
                _inputs.set_description(_input)
                parsed_items = self.parse(_input)

                try:
                    for parsed_item in parsed_items:
                        if parsed_item:
                            csvwriter.writerow(parsed_item)
                except Exception, e:
                    print e



# GotchaTwitter('timeline', ['phantomkidding'], '/Volumes/cchen224/test.csv', output_mode='w').crawl()

