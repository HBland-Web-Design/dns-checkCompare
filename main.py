#!/bin/python3
import argparse
import cache
import alert
import resolve_query

###
# Load Checks
###
def getChecks():

    return

###
# Load Environment Variables
###
def loadENV():

    return 

###
# Load Arguments
###
def getArgs():
    parser = argparse.ArgumentParser(
                    prog='HBWD DNS CheckCompare',
                    description='Checks a list of DNS Records and Alerts when different to Known Good Cache',
                    epilog='WIKI Available at the REPO https://github.com/HBland-Web-Design/dns-checkCompare')
    parser.add_argument('-e', '--environment',
                        action='', required=False,
                        nargs=1, default=None, 
                        help='Overide Default Environment File')
    parser.add_argument('-r', '--reset',
                        action='', required=False,
                        nargs=1, default=None, 
                        help='Resets the Cache to new known good')
    # parser.add_argument('-r', '--reset',
    #                     action='', required=False,
    #                     nargs=1, default=None, 
    #                     help='Resets the Cache to known good')
    return parser.parse_args()

###
# Main Load
###
def main():
    args = getArgs()
    env = loadEnv()

    checks = getChecks()

###
# Start the checks
###
if __name__ == '__main__':
    main()