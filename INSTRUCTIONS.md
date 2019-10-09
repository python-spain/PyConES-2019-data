# PyConES 2019 data

This doc explains how to interact with the Sched.com talks export process to recreate the PyConES 2019 data.


## How to (re)process it

Just get your sched.com API key and execute it:

```sh
python sched_talks.py -o files -t $SCHED_API_KEY
```

## How to add a Lightning Talk

Edit the file **lightning_talks.md**, add your talk and then execute the command:

```sh
python sched_talks.py -o files -t $SCHED_API_KEY
```

## Help

```
$ python sched_talks.py --help
Usage: sched_talks.py [options]

Options:
  -h, --help            show this help message and exit
  -o DIR, --output-dir=DIR
                        attachments output directory
  -t TOKEN, --token=TOKEN
                        sched.com API key/token

```