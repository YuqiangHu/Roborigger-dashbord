## System test guidlines

### Requirements:

- [Firefox](https://www.mozilla.org/en-US/firefox/new/)

1. Change to usertest directory `cd usertest`
2. Set up python virtual environment `python3 -m venv venv`
3. Activate the python virtual environment `source venv/bin/activate`
4. Download the required packages `pip install -r requirements.txt`
5. Run system test `python3 systemtest.py`
6. Exit the environment `deactivate`