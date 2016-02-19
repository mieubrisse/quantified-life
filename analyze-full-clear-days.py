"""
Description: Takes in a set of full-clear days and performs analysis on it
Author: mieubrisse
"""
 
import sys
import argparse
import json
import parsedatetime
import matplotlib.pyplot as plt
import datetime
 
_INPUT_FILEPATH_ARGVAR = "input_filepath"

_DATE_STR_KEY = "date"
_DATE_KEY = "datetime"
 
def _parse_args(argv):
    """ Parses args into a dict of ARGVAR=value, or None if the argument wasn't supplied """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(_INPUT_FILEPATH_ARGVAR, metavar="<input file>", help="JSON file containing an array of datapoints of the form {\"date\": \"February 12, 2016\"}")
    return vars(parser.parse_args(argv))
 
def _print_error(msg):
    sys.stderr.write('Error: ' + msg + '\n')
 
def _validate_args(args):
    """ Performs validation on the given args dict, returning a non-zero exit code if errors were found or None if all is well """
    return None
 
def main(argv):
    args = _parse_args(map(str, argv))
    err = _validate_args(args)
    if err is not None:
        return err

    input_filepath = args[_INPUT_FILEPATH_ARGVAR]

    with open(input_filepath) as input_fp:
        datapoints = json.load(input_fp)
    
    # Parse human-friendly date into Python-friendly one
    cal = parsedatetime.Calendar()
    for datapoint in datapoints:
        parsed_date, parse_type = cal.parse(datapoint[_DATE_STR_KEY])
        datapoint[_DATE_KEY] = datetime.date(parsed_date[0], parsed_date[1], parsed_date[2]) if parse_type == 1 else None

    days_of_week = [datapoint[_DATE_KEY].weekday() for datapoint in datapoints]
    plt.hist(days_of_week, 7)
    plt.show()
 
    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
