# facebook-json-to-csv
Convert your personal Facebook JSON archive to CSV files or pandas dataframes.

### How to use

1. Request a JSON archive from Facebook, download it and unpack zip file to local folder.
2. Copy [`friends.py`](https://raw.githubusercontent.com/epogrebnyak/facebook-json-to-csv/master/friends.py) somewhere you can use it, for example

```
curl -o friends.py https://raw.githubusercontent.com/epogrebnyak/facebook-json-to-csv/master/friends.py
```
3. Prey the Facebook JSON schema has not changed since I wrote this code
   (please fil an issue if it did).
4. Try some code below.

### Examples

Bulk conversion:

```
from friends import save_csv_all
save_csv_all(source_dir="./facebook-epogrebnyak", 
             output_dir="./output_folder")
```

creates the following files:

```
Saved files:
  output_folder\friends.csv
  output_folder\comments.csv
  output_folder\posts.csv
  output_folder\address_book.csv
  output_folder\reactions.csv
  output_folder\sessions.csv
```
Read your data with functions:

```python
from friends import get_friends, get_address_book, get_posts

directory = "C:/temp/facebook-me" # your path to folder with JSON here
friends = get_friends(directory)
phones = get_address_book(directory)
posts = get_posts(directory)
```

More flexible reading - as dicts, dataframes, etc:

```python
from friends import Friends, Comments, Posts, AddressBook, Reactions, Session 

f = Friends("./facebook-epogrebnyak")
friends = f.get_tuples()         # list of (timestamp, name) tuples
friends_dicts = f.get_dicts()    # same data as list of dictionaries
friends_gen = f.iterate()        # generator, useful for streaming large archives
friends_df = f.get_dataframe()   # pandas DataFrame ready for analysis 
f.save_csv("./output_folder")    # saves data to 'friends.csv'
```

See how [friends.py](friends.py) drawes some bars in the terminal:

```
Contacts from my phonebook stored by Facebook:
Total: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 212

Friends added by month (total 39)
2020-01: ▇▇▇ 3    
2020-02: ▇▇ 2    
2020-03: ▇▇ 2    
2020-04: ▇▇▇ 3    
2020-05: ▇▇▇▇▇▇▇▇ 8    
2020-06: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 18   
2020-07: ▇▇▇ 3    


Number of posts and comments by month (total 72)
2020-01: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 32   
2020-02: ▇▇▇▇▇▇▇▇▇ 15   
2020-03: ▇▇ 4    
2020-04: ▇▇▇▇▇▇▇▇ 13   
2020-05: ▇ 2    
2020-06: ▏ 1    
2020-07: ▇▇▇ 5    


Reactions by month (total 289)
2020-01: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 102  
2020-02: ▇▇▇▇▇▇▇▇▇▇▇▇▇ 67   
2020-03: ▇▇▇▇▇ 27   
2020-04: ▇▇▇▇ 22   
2020-05: ▇▇▇▇ 22   
2020-06: ▇▇ 13   
2020-07: ▇▇▇▇▇▇▇ 36   


Sessions by month (total 640)
2020-01: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 201  
2020-02: ▇▇▇▇▇▇▇▇▇▇ 108  
2020-03: ▇▇▇▇▇▇▇▇▇▇ 107  
2020-04: ▇▇▇▇▇▇▇ 75   
2020-05: ▇▇▇▇▇ 56   
2020-06: ▇▇▇▇ 42   
2020-07: ▇▇▇▇ 50   
2020-08: ▏ 1    

Session locations (includes VPN): Amsterdam, Balashikha, Bronnitsy, Elektrosal, Helsinki, Kashira, Kazan, Khimki, Kostroma, Moscow, Nizhny Novgorod, Nuremberg, Oryekhovo, Otvazhnoye, Penza, Samara, Sergiyevskoye, Serpukhov, Shchelkovo, Sofrino, Soligalich, Solnechnogorski, Tallinn, Tolyatti, Ufa, Zelënyy Gorod
Saved files:
  output_folder\friends.csv
  output_folder\comments.csv
  output_folder\posts.csv
  output_folder\address_book.csv
  output_folder\reactions.csv
  output_folder\sessions.csv

runfile('D:/github/facebook-json-to-csv/friends.py', wdir='D:/github/facebook-json-to-csv')

Contacts from my phonebook stored by Facebook:
Total: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 212

Friends added by month (total 39)
2020-01: ▇▇▇ 3    
2020-02: ▇▇ 2    
2020-03: ▇▇ 2    
2020-04: ▇▇▇ 3    
2020-05: ▇▇▇▇▇▇▇▇ 8    
2020-06: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 18   
2020-07: ▇▇▇ 3    


Number of posts and comments by month (total 72)
2020-01: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 32   
2020-02: ▇▇▇▇▇▇▇▇▇ 15   
2020-03: ▇▇ 4    
2020-04: ▇▇▇▇▇▇▇▇ 13   
2020-05: ▇ 2    
2020-06: ▏ 1    
2020-07: ▇▇▇ 5    


Reactions by month (total 289)
2020-01: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 102  
2020-02: ▇▇▇▇▇▇▇▇▇▇▇▇▇ 67   
2020-03: ▇▇▇▇▇ 27   
2020-04: ▇▇▇▇ 22   
2020-05: ▇▇▇▇ 22   
2020-06: ▇▇ 13   
2020-07: ▇▇▇▇▇▇▇ 36   


Sessions by month (total 640)
2020-01: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 201  
2020-02: ▇▇▇▇▇▇▇▇▇▇ 108  
2020-03: ▇▇▇▇▇▇▇▇▇▇ 107  
2020-04: ▇▇▇▇▇▇▇ 75   
2020-05: ▇▇▇▇▇ 56   
2020-06: ▇▇▇▇ 42   
2020-07: ▇▇▇▇ 50   
2020-08: ▏ 1    

Session locations (includes VPN): Amsterdam, Balashikha, Bronnitsy, Elektrosal, Helsinki, Kashira, Kazan, Khimki, Kostroma, Moscow, Nizhny Novgorod, Nuremberg, Oryekhovo, Otvazhnoye, Penza, Samara, Sergiyevskoye, Serpukhov, Shchelkovo, Sofrino, Soligalich, Solnechnogorski, Tallinn, Tolyatti, Ufa, Zelënyy Gorod

Saved files:
  output_folder\friends.csv
  output_folder\comments.csv
  output_folder\posts.csv
  output_folder\address_book.csv
  output_folder\reactions.csv
  output_folder\sessions.csv
  ```

## Background

Motivated by desire for break free from FB without loosing the data.

Similar efforts:

- https://github.com/Lackoftactics/facebook_data_analyzer
- https://github.com/itzmeanjan/fviz/issues/15
- https://github.com/kaustubhhiware/facebook-archive
- https://github.com/numbersprotocol/fb-json2table/
