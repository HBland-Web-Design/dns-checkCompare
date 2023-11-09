#!/bin/python3
import argparse
from pathlib import Path
import cache
import alert
import resolve_query

###
# Load Checks
###
def getChecks():
    f = open(Path('checks').resolve(), 'r')
    
    uChecks = f.readlines()
    # Create data dictionary
    checks = []
    # loop through all checks and add to dictionary
    for check in uChecks:
        if check.startswith('#'):
            continue

        checkData = {}
        checkData["record"] = check.split(";")[0]
        checkData["recordType"] = check.split(";")[1]

        checks.append(checkData)

    f.close()
    
    return checks

###
# Load Environment Variables
###
def loadENV():

    f = open(Path('.env').resolve(), 'r')

    uENV = f.readlines()
    cENV={}

    for envVar in uENV:
        if envVar.startswith('CACHE_LOCATION'):
            cENV["CACHE_LOCATION"] = envVar.split("=")[1]
        elif envVar.startswith('CHECKS_LOCATION'):
            cENV["CHECKS_LOCATION"] = envVar.split("=")[1]
        elif envVar.startswith('TENNANT_ID'):
            cENV["MS_TENNANT_ID"] = envVar.split("=")[1]
        elif envVar.startswith('CLIENT_ID'):
            cENV["MS_CLIENT_ID"] = envVar.split("=")[1]
        elif envVar.startswith('CLIENT_SECRET'):
            cENV["MS_CLIENT_SECRET"] = envVar.split("=")[1]
        else:
            continue

    f.close()

    return cENV

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
    env =loadENV()

    checks = getChecks()

    for check in checks:
        record = check["record"]
        recordType = check["recordType"]

        result = resolveQuery(record, recordType)

    resolve_query()

    cache = load_cache()

    if cache == FileNotFoundError:
        save_cache(checks)

###
# Start the checks
###
if __name__ == '__main__':
    main()