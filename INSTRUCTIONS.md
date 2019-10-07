# PyConES 2019 data

This doc explains how to interact with the Sched.com talks export process to recreate the PyConES 2019 data.


## How to (re)process it

Just get your sched.com API key and execute it:

```sh
python sched_talks.py -o files -t $SCHED_API_KEY
```

```
