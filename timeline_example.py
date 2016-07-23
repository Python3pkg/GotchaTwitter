from gotchatwitter import GotchaTwitter
import sys
from glob import glob


if __name__ == '__main__':
    argvs = sys.argv[1:]
    inp = argvs[0]

    try:
        start = argvs[1]
    except:
        start = ''

    for file in glob(inp):
        with GotchaTwitter('timeline', file, output_fp='~/Downloads/test.csv', output_mode='w',
                           date_since='2016-02-06', date_until='2016-02-10') as gt:
			try:
				gt.crawl()
			except KeyboardInterrupt:
				break

file = ['phantomkidding']
with GotchaTwitter('timeline', file, '/Users/cchen/Downloads/test.csv') as gt:
	gt = gt.set_output(save_mode='w', has_header=True) \
		.set_notifier('pushbullet', access_token='o.X7MEj0qDukl4uhj8EZ28K5tAY0P5c0c0')
	gt.crawl()