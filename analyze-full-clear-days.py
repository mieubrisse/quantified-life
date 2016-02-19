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
 
def _calculate_runs(datapoints):
    """
    Helper function to calculate runs of:
    0. streaks - consecutive days of full-clears
    1. droughts - consecutive days 

    Args:
    datapoints -- A list of datapoints with at least one element
    """
    current_streak = None
    streaks = []

    prev_datapoint = None
    for datapoint in datapoints:
        date = datapoint[_DATE_KEY]
        if prev_datapoint is not None:
            prev_date = prev_datapoint[_DATE_KEY]
            
            if (date - prev_date).days == 1:
                if current_streak is None:
                    current_streak = [prev_datapoint, datapoint]
                    streaks.append(current_streak)
                else:
                    current_streak[1] = datapoint
            else:
                current_streak = None

        prev_datapoint = datapoint

    # For convenience, we'll calculate lengths
    streaks = [(streak[0], streak[1], (streak[1][_DATE_KEY] - streak[0][_DATE_KEY]).days + 1) for streak in streaks]

    # TODO Implmement droughts
    # We now have a dict of streaks as (start, end) pairs, so we can calculate droughts from there
    return (streaks, [])


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

    """
    days_of_week = [datapoint[_DATE_KEY].weekday() for datapoint in datapoints]
    plt.hist(days_of_week, 7)
    plt.show()
    """

    streaks, droughts = _calculate_runs(datapoints)
    sorted_streaks = sorted(streaks, key=lambda streak: streak[2])
    longest_streak = sorted_streaks[-1]
    print "Longest streak: {} days between {} and {}".format(longest_streak[2], longest_streak[0][_DATE_KEY], longest_streak[1][_DATE_KEY])
 
    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
