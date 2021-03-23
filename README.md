# e3372-py

E3372 SMS handler written in Python. Uses the hilink web interface API. Allows
you to do something when SMS arrives.

## Requirements

* lxml (`apt install python3-lxml` or something like it)
* see `requirements.txt`

## Usage

You need at least Python 3.6 or so.

See `main.py` and adjust the `sms_handler` function to your needs.

The script should be launched periodically by cron. For example, put this to the 
crontab to launch it every 15 minutes:
```cron
*/15 * * * * python3 /path/to/e3372-py/main.py --trusted-phone +79001234567 > /dev/null
```

## License

BSD-2c