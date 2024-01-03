#!/bin/python3
import argparse
from pathlib import Path
import cache
import alert
import resolve_query
import json, os, report
from logit import logit
###
# Load Checks
###
def getChecks():
    """
    The function `getChecks` reads a file named "checks" and parses its contents into a list of
    dictionaries, where each dictionary represents a check with a "record" and "recordType" key-value
    pair.
    :return: The function `getChecks` returns a list of dictionaries, where each dictionary represents a
    check. Each dictionary contains two key-value pairs: "record" and "recordType".
    """
    f = open(Path('checks').resolve(), 'r')
    logit.info('Opening Checks file')
    uChecks = f.readlines()
    # Create data dictionary
    checks = []
    # loop through all checks and add to dictionary
    for check in uChecks:
        logit.info('Running check for {}'.format(check))
        if check.startswith('#'):
            continue

        checkData = {}
        checkData["record"] = check.split(";")[0]
        checkData["recordType"] = check.split(";")[1].strip('\n')
        logit.debug('{}'.format(checkData))
        logit.info('Appending check to list')
        checks.append(checkData)
    logit.info('Closing checks file')
    f.close()
    
    return checks

###
# Group Results
###
def groupByDomain(checkResults):
    """
    The function `groupByDomain` groups a list of dictionaries by their 'domain' key.
    
    :param checkResults: The parameter `checkResults` is expected to be a list of dictionaries. Each
    dictionary represents a check result and should have a key called 'domain' that represents the
    domain name
    :return: a dictionary where the keys are the unique domain values from the checkResults list, and
    the values are lists of items from checkResults that have the same domain value.
    """
    groupedResults = {}
    for item in checkResults:
        key = item.get('domain')
        if key not in groupedResults:
            groupedResults[key] = []
        groupedResults[key].append(item)
    return groupedResults

###
# Load Environment Variables
###
def loadENV(envPath):
    """
    The function `loadENV` reads environment variables from a file and returns a dictionary containing
    specific variables.
    
    :param envPath: The `envPath` parameter is a string that represents the path to the environment
    file. This file contains environment variables that need to be loaded into the program. If the
    `envPath` parameter is `None`, the function will try to open a file named `.env` in the current
    directory
    :return: a dictionary `cENV` which contains the environment variables `CACHE_LOCATION`,
    `CHECKS_LOCATION`, `MS_TENNANT_ID`, `MS_CLIENT_ID`, and `MS_CLIENT_SECRET`.
    """

    if envPath != None:
        f = open(envPath, 'r')
    else:
        f = open(Path('.env').resolve(), 'r')


    uENV = f.readlines()
    cENV={}

    for envVar in uENV:
        if envVar.startswith('CACHE_LOCATION'):
            cENV["CACHE_LOCATION"] = envVar.split("CACHE_LOCATION=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('CHECKS_LOCATION'):
            cENV["CHECKS_LOCATION"] = envVar.split("CHECKS_LOCATION=")[1].split(' #')[0].strip('\n')
        # MAIL ENVELOPE
        elif envVar.startswith('RECIPIENT'):
            cENV["RECIPIENT"] = envVar.split("RECIPIENT=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('SENDER'):
            cENV["SENDER"] = envVar.split("SENDER=")[1].split(' #')[0].strip('\n')
        # MAILER
        elif envVar.startswith('MAILER'):
            cENV["MAILER"] = envVar.split("MAILER=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('TENNANT_ID'):
            cENV["MS_TENNANT_ID"] = envVar.split("TENNANT_ID=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('CLIENT_ID'):
            cENV["MS_CLIENT_ID"] = envVar.split("CLIENT_ID=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('CLIENT_SECRET'):
            cENV["MS_CLIENT_SECRET"] = envVar.split("CLIENT_SECRET=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('AUTHENTICATION'):
            cENV["SMTP_AUTHENTICATION"] = envVar.split("AUTHENTICATION=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('SERVER'):
            cENV["SMTP_SERVER"] = envVar.split("SERVER=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('PORT'):
            cENV["SMTP_PORT"] = envVar.split("PORT=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('USERNAME'):
            cENV["SMTP_USERNAME"] = envVar.split("USERNAME=")[1].split(' #')[0].strip('\n')
        elif envVar.startswith('PASSWORD'):
            cENV["SMTP_PASSWORD"] = envVar.split("PASSWORD=")[1].split(' #')[0].strip('\n')
        else:
            continue
    f.close()
    return cENV

def dockerENV():
    """
    The function `loadENV` reads environment variables from a file and returns a dictionary containing
    specific variables.
    
    :param envPath: The `envPath` parameter is a string that represents the path to the environment
    file. This file contains environment variables that need to be loaded into the program. If the
    `envPath` parameter is `None`, the function will try to open a file named `.env` in the current
    directory
    :return: a dictionary `cENV` which contains the environment variables `CACHE_LOCATION`,
    `CHECKS_LOCATION`, `MS_TENNANT_ID`, `MS_CLIENT_ID`, and `MS_CLIENT_SECRET`.
    """

    cENV={}
    # Defaults
    cENV["CACHE_LOCATION"] = os.getenv('CACHE_LOCATION', '/opt/hbland/checkcompare/cachefile')
    cENV["CHECKS_LOCATION"] = os.getenv('CHECKS_LOCATION', '/opt/hbland/checkcompare/checks')
    # Mail Envelope
    cENV["RECIPIENT"] = os.getenv('RECIPIENT')
    cENV["SENDER"] = os.getenv('SENDER')
    # MAILER
    cENV["MAILER"] = os.getenv('MAILER')
    cENV["MS_TENNANT_ID"] = os.getenv('TENNANT_ID')
    cENV["MS_CLIENT_ID"] = os.getenv('CLIENT_ID')
    cENV["MS_CLIENT_SECRET"] = os.getenv('CLIENT_SECRET')
    cENV["SMTP_AUTHENTICATION"] = os.getenv('AUTHENTICATION')
    cENV["SMTP_SERVER"] = os.getenv('SERVER')
    cENV["SMTP_PORT"] = os.getenv('PORT')
    cENV["SMTP_USERNAME"] = os.getenv('USERNAME')
    cENV["SMTP_PASSWORD"] = os.getenv('PASSWORD')

    return cENV

###
# Load Arguments
###
def getArgs():
    """
    The `getArgs` function is a Python function that uses the `argparse` module to parse command line
    arguments and return the parsed arguments.
    :return: The function `getArgs()` returns the parsed arguments from the command line.
    """
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
    """
    The main function performs a series of checks on records, resolves queries, and compares results
    with a cached version before generating a report.
    """
    args = getArgs()
    logit.info('Checking host')
    if os.getenv('HB_RUNTIME') == 'DOCKER':
        logit.info('Script running in Docker building env')
        env = dockerENV()
    else:
        logit.info('Script running local building env')
        env = loadENV(args.environment)
        
    logit.info('Getting Checks')
    checks = getChecks()
    logit.info('Checks complete')
    checkResults = []
    logit.debug({}.format(checkResults))
    
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
        # print(compareResult)

        report.fill_global_template(env, compareResult)

        domainGroupedResults = groupByDomain(compareResult)

        report.fill_domain_template(env, domainGroupedResults)


###
# Start the checks
###
if __name__ == '__main__':
    main()