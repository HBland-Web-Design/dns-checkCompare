import json
from pathlib import Path
from datetime import datetime
import mailer
import os
###
# DateTime
###
def getDate():
    return datetime.now().date()

def getTimeStamp():
    return datetime.now().strftime('%H:%M')

###
# FillTemplate
###
def fill_global_template(env, results):
    # Load the HTML template
    with open(Path('Templates/globalReport.html').resolve(), 'r') as file:
        template_content = file.read()

    # Create rows based on JSON data
    rows_content = ""
    RED = 0
    for record in results:
        if record['status'] == "Fail":
            RED += 1
            row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: center;'>{record['domain']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{record['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{record['recordType']}</td><td style='background-color: red; border: 1px solid black; padding: 8px; text-align: center;'>{record['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{record['msg']}</td></tr>"
        elif record['status'] == "Pass":
            RED += 0
            row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: center;'>{record['domain']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{record['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{record['recordType']}</td><td style='background-color: green; border: 1px solid black; padding: 8px; text-align: center;'>{record['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: center; background-color: lightgrey'></td></tr>"
        rows_content += row

    if RED >= 1:
        report_title=f"<h1 style='color: red;'>ERROR in Global DNS Record Check for {getDate()}</h1>"
    elif RED == 0:
        report_title=f"<h1>Global DNS Record Check for {getDate()}</h1>"
    # Fill in the template
    filled_template = template_content.format(title=report_title, time=getTimeStamp(), rows=rows_content)
    subject = "Global DNS Record Check for {}".format(getDate())
    
    mailer.main(env, subject, filled_template)
    
    # Write the filled template to a new HTML file
    if os.getenv('HB_RUNTIME') == 'DOCKER':
        pass
    else:
        with open(Path('Reports/globalReport_{}.html'.format(getDate())).resolve(), 'w+') as file:
            file.truncate(0)
            file.write(filled_template)

    print("Filled HTML template created successfully.")
    
    return()


def fill_domain_template(env, domains):
    # domain, results = domains
    # print(domain)
    # print(results)
    # Load the HTML template
    with open(Path('Templates/domainReport.html').resolve(), 'r') as file:
        template_content = file.read()

    # Create rows based on JSON data
    # rows_content = ""
    # RED = 0
    
    for domain, results in domains.items():
        print('HIT@@')
        rows_content = ""
        RED = 0
        for result in results:
            print(result)
            if result['status'] == "Fail":
                print(result['status'])
                RED += 1
                row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: center;'>{result['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{result['recordType']}</td><td style='background-color: red; border: 1px solid black; padding: 8px; text-align: center;'>{result['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{result['msg']}</td></tr>"
            elif result['status'] == "Pass":
                print(result['status'])
                RED += 0
                row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: center;'>{result['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: center;'>{result['recordType']}</td><td style='background-color: green; border: 1px solid black; padding: 8px; text-align: center;'>{result['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: center; background-color: lightgrey'></td></tr>"
            rows_content += row

        if RED >= 1:
            report_title=f"<h1 style='color: red;'>ERROR in {domain} DNS Record Check for {getDate()}</h1>"
        elif RED == 0:
            report_title=f"<h1>{domain} DNS Record Check for {getDate()}</h1>"
        # Fill in the template
        filled_template = template_content.format(domain=domain,title=report_title, time=getTimeStamp(), rows=rows_content)

        subject = "{} DNS Record Check for {}".format(domain,getDate())
    
        mailer.main(env, subject, filled_template)
        
        # Write the filled template to a new HTML file
        if os.getenv('HB_RUNTIME') == 'DOCKER':
            pass
        else:
            with open(Path('Reports/{}_Report_{}.html'.format(domain, getDate())).resolve(), 'w+') as file:
                file.truncate(0)
                file.write(filled_template)

        print("Filled HTML template created successfully.")
        
    return()