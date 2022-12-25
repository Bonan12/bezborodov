from cProfile import Profile
import datefinder
from datetime import datetime
from dateutil.parser import parse
import pandas

data = pandas.read_csv('vacancies_by_year.csv', usecols=['published_at'])['published_at'].tolist()


def profile_it(func):
	def profiling(date_list):
		profile = Profile()
		profile.enable()
		for date in date_list:
			func(date)
		profile.disable()
		print('Статистика по функции', func.__name__)
		profile.print_stats(1)
	return profiling


def datetime_test(date):
	date = datetime.strptime(date[:10], '%Y-%m-%d').date()
	return f'{date.day}.{date.month}.{date.year}'


def slice_test(date):
	return f'{date[8:10]}.{date[5:7]}.{date[:4]}'


def split_test(date):
	date = date.split('T')[0].split('-')
	year, month, day = date
	return f'{day}.{month}.{year}'


def datefinder_test(date):
	date = str(list(datefinder.find_dates(date))[0])
	return f'{date[8:10]}.{date[5:7]}.{date[:4]}'


def test_parsing_with_format(date):
	return '{0[2]}.{0[1]}.{0[0]}'.format(date[:10].split('-'))


def test_parsing_dateutil_parse(date):
	date = parse(date)
	return f'{date.day}.{date.month}.{date.year}'


if __name__ == '__main__':
	profiler = profile_it(test_parsing_dateutil_parse)
	profiler(data)
