# Json-Datetime-util

Convert data from str to datetime or datetime to str.
Can also get all dict or list values to convert all to requested type.

## How to Install

`pip install date-reclass`

## How to Use

Json-datetime-util will allow the user to simply convert entire lists or dicts of data.

All datetimes inside of the list or dict will be converted from str to datetime or vice-versa.

When you have a str and need a datetime:

```
from date_reclass import cast

date = '17/05/2020'
result = cast(date, '%d/%m/%Y').todatetime()
>>> '2020-05-17 00:00:00'

```

If you have a list or dict the same code can be used:
```
# dict example
from date_reclass import cast

date = {'date1':'17/05/2020','date2':'17/05/2021'}
result = cast(date, '%d/%m/%Y').todatetime()
>>> {'date1': datetime.datetime(2020, 5, 17, 0, 0), 'date2':{'date2': datetime.datetime(2021, 5, 17, 0, 0)}

# list example
from date_reclass import cast

date = ['17/05/2020','17/05/2021']
result = cast(date, '%d/%m/%Y').todatetime()
>>> [datetime.datetime(2020, 5, 17, 0, 0), datetime.datetime(2021, 5, 17, 0, 0)]

```

When you have a datetime and need a string:

```
from date_reclass import cast
import datetime

date = datetime.datetime(2020, 5, 17)
result = cast(date).tostr()
>>> '2020-05-17 00:00:00'

```

For list or dict:

```
# dict
from date_reclass import cast
import datetime

date = {'date1':'17/05/2020','date2':'17/05/2021'}
result = cast(date, '%d/%m/%Y').todatetime()
>>> {'date1': datetime.datetime(2020, 5, 17, 0, 0), 'date2': datetime(2021, 5, 17, 0, 0)}

# list
from date_reclass import cast
import datetime

date = ['17/05/2020', '17/05/2021']
result = cast(date, '%d/%m/%Y').todatetime()
>>> [datetime.datetime(2020, 5, 17, 0, 0), datetime(2021, 5, 17, 0, 0)]

```




## Run Tests

Run tests by running

`python3 -m unittest app/tests/*/**.py`

You can also check coverage and generate a coverage report

```
    coverage run -m unittest tests/*.py && coverage report 
```
