FROM python:3.10.13

MAINTAINER Harry Bland <info@hbland.co.uk>

WORKDIR /usr/src/app

# Pull and Install requirements
ADD source/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy cron job to container
ADD checkcompare.cronjob /opt/hbland/checkcompare.cronjob

# Copy source to container
COPY source/ /opt/hbland/checkcompare/

# Change permission cron job file and load it with crontab
RUN \
	chmod 0644 /opt/hbland/checkcompare.cronjob && \
	crontab /opt/hbland/checkcompare.cronjob

# Create a file needed by checkcompare.cronjob
RUN \
	touch /var/log/cron.log

# Run the command on container startup:
# - Run non-daemonized cron in background
# - Output the log result from checkcompare.cronjob
CMD (cron -f &) && tail -f /var/log/cron.log