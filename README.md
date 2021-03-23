# e3372-py

E3372 SMS handler written in Python. Uses the hilink web interface API. Allows
you to do something when SMS arrives.

## Requirements

* lxml (`apt install python3-lxml` or something like it)
* see `requirements.txt`

## Usage

You need at least Python 3.6 or so.

See `main.py` and adjust the `sms_handler` function to your needs.

The script should be launched periodically by cron. This line in crontab would
launch the script every 10 minutes:
```cron
*/10 * * * * python3 /path/to/e3372-py/main.py --trusted-phone 79001234567
```

## License

BSD-2c