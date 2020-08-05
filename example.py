from friends import Friends, Comments, Posts, AddressBook

f = Friends("./facebook-epogrebnyak")
friends = f.get_tuples()  # list of (timestamp, name) tuples
friends_dicts = f.get_dicts()  # same data as list of dictionaries
friends_gen = f.iterate()  # useful for streaming large archives
friends_df = f.get_dataframe()  # pandas DataFrame ready for analysis
f.save_csv("./output_folder")  # saves data to 'friends.csv'
