import pandas as pd  

from friends import get_friends, get_address_book

folder = "./facebook-epogrebnyak"
friends = get_friends(folder)
print("Friends added in Jan-Jul 2020:", len(friends))
# Friends added in Jan-Jul 2020: 39

print("Friends added by month:")
friends_df = pd.DataFrame(friends).set_index("timestamp")
print(friends_df.groupby(pd.Grouper(freq="M")).count())
# Friends added by month:
#             name
# timestamp
# 2020-01-31     3
# 2020-02-29     2
# 2020-03-31     2
# 2020-04-30     3
# 2020-05-31     8
# 2020-06-30    18
# 2020-07-31     3

phones = get_address_book(folder)
print("\nNumbers from my phonebook stored by Facebook:", len(phones))
# Numbers from my phonebook stored by Facebook: 212