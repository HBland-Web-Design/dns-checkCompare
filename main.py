#!/bin/python3
import argparse
from pathlib import Path
import cache
import alert
import resolve_query
import json
import report
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
        checkData["recordType"] = check.split(";")[1].strip('\n')

        checks.append(checkData)

    f.close()
    
    return checks

###
# Group Results
###
def groupByDomain(checkResults):
    groupedResults = {}
    for item in results:
        key = item.get('domain')
        if key not in grouped_results:
            groupedResults[key] = []
        groupedResults[key].append(item)
    return grouped_results

###
# Load Environment Variables
###
def loadENV(envPath):

    if envPath != None:
        f = open(envPath, 'r')
    else:
        f = open(Path('.env').resolve(), 'r')

    uENV = f.readlines()
    cENV={}

    for envVar in uENV:
        if envVar.startswith('CACHE_LOCATION'):
            cENV["CACHE_LOCATION"] = envVar.split("=")[1].strip('\n')
        elif envVar.startswith('CHECKS_LOCATION'):
            cENV["CHECKS_LOCATION"] = envVar.split("=")[1].strip('\n')
        elif envVar.startswith('TENNANT_ID'):
            cENV["MS_TENNANT_ID"] = envVar.split("=")[1].strip('\n')
        elif envVar.startswith('CLIENT_ID'):
            cENV["MS_CLIENT_ID"] = envVar.split("=")[1].strip('\n')
        elif envVar.startswith('CLIENT_SECRET'):
            cENV["MS_CLIENT_SECRET"] = envVar.split("=")[1].strip('\n')
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
                         required=False,
                        nargs=1, default=None, 
                        help='Overide Default Environment File')
    parser.add_argument('-r', '--reset',
                        action='store_true', required=False,
                        default=None, 
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
    env = loadENV(args.environment)

    checks = getChecks()

    checkResults = []

    for check in checks:
        record = check["record"]
        recordType = check["recordType"]

        result = resolve_query.resolveQuery(record, recordType)

        checkResults.append(result)


    if args.reset == True:
        cache.reset_cache(checkResults, env['CACHE_LOCATION'])
    
    elif args.reset == False:
        print("true")

    else:
        cacheLoaded = cache.load_cache(env['CACHE_LOCATION'])
        
        if cacheLoaded == "FileNotFound":
            print(f"An error occurred: {str(cacheLoaded)}")
            exit()

        compareResult = cache.cache_compare(checkResults, cacheLoaded)
        print(compareResult)

        report.fill_global_template(compareResult)

        domainGroupedResults = groupByDomain(compareResult)

        for result in domainGroupedResults:
            report.fill_domain_template(result)

###
# Start the checks
###
if __name__ == '__main__':
    main()