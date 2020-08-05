from friends import Friends, Comments, Posts, AddressBook 

f = Friends("./facebook-epogrebnyak")
friends = f.get_tuples()         # list of tuples
friends_dicts = f.get_dicts()    # list of dictionaries
friends_gen = f.iterate()        # useful for streaming large archives
friends_df = f.get_dataframe()   # ready for analysis 
f.save_csv("./output_folder")    # not implemented yet