Query BTCMarkets price and notify via twilio when it reaches a certain value.

Run with cron once an hour
```
0 * * * * /path
```

twilioConfig.py is required
```
account_sid = ""
auth_token = ""
twilio_number = ""
recp = ""
```
