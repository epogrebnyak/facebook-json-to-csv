import pandas as pd

from friends import get_friends, get_address_book

# This is a path to a folder where I unzipped Facebook JSON file
folder = "./facebook-epogrebnyak"

# Friends added in Jan-Jul 2020: 39
friends = get_friends(folder)
print("Friends added in Jan-Jul 2020:", len(friends))

print("Friends added by month:")
friends_df = pd.DataFrame(friends).set_index("timestamp")
print(friends_df.groupby(pd.Grouper(freq="M")).count())
#             name
# timestamp
# 2020-01-31     3
# 2020-02-29     2
# 2020-03-31     2
# 2020-04-30     3
# 2020-05-31     8
# 2020-06-30    18
# 2020-07-31     3

# Numbers from my phonebook stored by Facebook: 212
phones = get_address_book(folder)
print("\nNumbers from my phonebook stored by Facebook:", len(phones))
