# facebook-json-to-csv
Convert your personal Facebook JSON archive to CSV or pandas dataframe.

### How to use

1. Request a JSON archive from Facebook, download it and unpack zip file to local folder
2. Copy [`friends.py`](https://raw.githubusercontent.com/epogrebnyak/facebook-json-to-csv/master/friends.py) somewhere you can use it, for example

```
curl -o friends.py https://raw.githubusercontent.com/epogrebnyak/facebook-json-to-csv/master/friends.py
```
3. Try some code as below:

```python
from friends import Friends, Comments, Posts, AddressBook 

f = Friends("./facebook-epogrebnyak")
friends = f.get_tuples()         # list of (timestamp, name) tuples
friends_dicts = f.get_dicts()    # same data as list of dictionaries
friends_gen = f.iterate()        # useful for streaming large archives
friends_df = f.get_dataframe()   # pandas DataFrame ready for analysis 
f.save_csv("./output_folder")    # saves data to 'friends.csv'
```

See [friends.py](friends.py) for another example:

```
Friends added in Jan-Jul 2020 by month (total 39)
2020-01: ▇▇▇ 3    
2020-02: ▇▇ 2    
2020-03: ▇▇ 2    
2020-04: ▇▇▇ 3    
2020-05: ▇▇▇▇▇▇▇▇▇▇ 8    
2020-06: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 16   
2020-07: ▇▇▇▇▇▇ 5    


Contacts from my phonebook stored by Facebook:
2020-07: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 212


Number of posts Jan-Jul 2020 by month (total 33)
2020-01: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 13   
2020-02: ▇▇▇▇▇▇▇▇▇ 6    
2020-03: ▇▇▇▇▇▇ 4    
2020-04: ▇▇▇▇▇▇▇ 5    
2020-05: ▇▇▇ 2    
2020-06: ▇ 1    
2020-07: ▇▇▇ 2     
```

## Background

Motivated by desire for break free from FB without loosing the data.

Similar efforts:

- https://github.com/itzmeanjan/fviz/issues/15
- https://github.com/kaustubhhiware/facebook-archive
- https://github.com/numbersprotocol/fb-json2table/
