#!/usr/bin/env python3

import argparse

import anna.worker

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='End-to-end testing using selenium')
	parser.add_argument('-d', '--driver', required=True, help='The name of the driver to use. Currently only supports '
															  'chrome, firefox & ie. However, if run using the '
															  'API, you\'ll only be able to test chrome & firefox '
															  'since there isn\'t a docker container for selenium with '
															  'ie.')
	parser.add_argument('-s', '--site', required=True,
						help='Names of the sites to test (separate by space).')
	parser.add_argument('-v', '--verbose', action='store_true', help='Print exceptions and stack traces while running.')
	parser.add_argument('-H', '--headless', action='store_true', help='Run drivers in headless mode.')
	parser.add_argument('-r', '--resolution', required=False, help='Set the driver resolution (defaults to 1920x1080).')
	parser.add_argument('-i', '--id', required=True, help='Set the job id.')
	parser.add_argument('--host', required=False, help='Set the API host.')
	parser.add_argument('-t', '--token', required=False, help='Set the API token.')
	args = vars(parser.parse_args())
	worker = anna.worker.Worker(args)
	worker.run()
	worker.close()
	if not worker.passed:
		raise ValueError('failed')
