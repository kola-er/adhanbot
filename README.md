# adhanbot

Slack bot for Islamic Call to Prayer

## Requirements

* Python 3
* Git
* Slack Incoming Webhook registration on your workspace at https://slack.com/
* Sendgrid API_KEY at https://sendgrid.com/ if you want to be nofitified of any issues. NOT REQUIRED!

## Setup

* Clone this repo.
* Run these commands in the projects root directory.
```bash
$ pip install -r requirements.txt
$ cp .env.example .env
$ cp config.json.example config.json
```
* Edit both .env and config.json accordingly. NOTE that `channelA` and `channelB` are used as example in both files and need to be changed to the Slack channels you would like to send notifications to.
* Start the app with this command. NOTE that you need to have python3 installed.
```bash
$ python start.py
```

## Contributing

Please check out [CONTRIBUTING](CONTRIBUTING.md) file for detailed contribution guidelines.

## Credits

adhanbot is maintained by `Kolawole ERINOSO`.

## License

adhanbot is released under the MIT Licence. See the bundled [LICENSE](LICENSE.md) file for details.
