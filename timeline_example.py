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
		gt = GotchaTwitter('timeline', file, '/Volumes/cchen224/test.csv',
                           date_since='2016-02-06', date_until='2016-02-10')
		# a = TwitterCrawler('timeline').set_input(file, start_value=start).set_output(file + '.csv').set_progress_bar(2).set_notifier('gmail').set_date_range('2016-02-06', '2016-02-10')
		#a = TwitterCrawler('info').set_input(file).set_output(file + '.csv').set_notifier('gmail')
		try:
			gt.crawl()
		except KeyboardInterrupt:
			break
