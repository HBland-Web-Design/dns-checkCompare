import json
from pathlib import Path
from datetime import datetime
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
def fill_global_template(results):
    # Load the HTML template
    with open(Path('Templates/globalReport.html').resolve(), 'r') as file:
        template_content = file.read()

    # Create rows based on JSON data
    rows_content = ""
    RED = 0
    for record in results:
        if record['status'] == "Fail":
            RED += 1
            row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['domain']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['recordType']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['msg']}</td></tr>"
        elif record['status'] == "Pass":
            RED += 0
            row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['domain']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['recordType']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{record['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: left; background-color: lightgrey'></td></tr>"
        rows_content += row

    if RED >= 1:
        report_title=f"<h1 style='color: red;'>ERROR in Global DNS Record Check for {getDate()}</h1>"
    elif RED == 0:
        report_title=f"Global DNS Record Check for {getDate()}"
    # Fill in the template
    filled_template = template_content.format(title=report_title, time=getTimeStamp(), rows=rows_content)

    # Write the filled template to a new HTML file
    with open('globalReport_{}.html'.format(getDate()), 'w') as file:
        file.write(filled_template)

    print("Filled HTML template created successfully.")


def fill_domain_template(domains):
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
        for result in results:
            rows_content = ""
            RED = 0
            print(result)
            if result['status'] == "Fail":
                RED += 1
                row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: left;'>{result['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{result['recordType']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{result['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{result['msg']}</td></tr>"
            elif result['status'] == "Pass":
                RED += 0
                row = f"\n<tr><td style='border: 1px solid black; padding: 8px; text-align: left;'>{result['record']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{result['recordType']}</td><td style='border: 1px solid black; padding: 8px; text-align: left;'>{result['status']}</td><td style='border: 1px solid black; padding: 8px; text-align: left; background-color: lightgrey'></td></tr>"
            rows_content += row

        if RED >= 1:
            report_title=f"<h1 style='color: red;'>ERROR in {domain} DNS Record Check for {getDate()}</h1>"
        elif RED == 0:
            report_title=f"{domain} DNS Record Check for {getDate()}"
        # Fill in the template
        filled_template = template_content.format(domain=domain,title=report_title, time=getTimeStamp(), rows=rows_content)

        # Write the filled template to a new HTML file
        with open('{}_Report_{}.html'.format(domain, getDate()), 'w') as file:
            file.write(filled_template)

        print("Filled HTML template created successfully.")