import warnings


def read_job(job):
    extensions = {'timeline': '.tml',
                  'threads': '.trd'}
    if job in set(extensions):
        return job, extensions[job]
    else:
        raise LookupError('Job options:\ttimeline threads')


def read_header(job, **kwargs):
    readers = {'timeline': _read_header_timeline(**kwargs)}
    return readers[job]


def _read_header_timeline(**kwargs):
    default = ['status', 'uid', 'screen_name', 'tid', 'timestamp', 'text', 'media',
               'language', 'n_retweets', 'n_likes',
               'location_id', 'location_name']
    header = kwargs.get('output_header', default)
    other_ = set(header) - set(default)
    if other_:
        warnings.warn('header %s not found' % other_)
    return header