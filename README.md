# dns-checkCompare

## Adding Domain to Check

Edit `checks` file.
```
#DOMAIN;RECORDTYPE
google.com;A
```

## Environment Variables

### Defaults

`CACHE_LOCATION`
The Cache file location

`CHECKS_LOCATION`
The checks file location

### Mail Info

`RECIPIENT`
Set to the Recipient mail i.e. `reports@example.com`

`SENDER`
Set to the Sender mail i.e. `healthcheck@example.com`

### SMTP MAILER

`MAILER`
Set to SMTP

`SERVER`
Set to the Server Address

`PORT`
Set to the Port used for SMTP Communication

`AUTHENTICATION`
Currently only SSL supported

`USERNAME`
Set to the SMTP User

`PASSWORD`
Set to the SMTP User Password