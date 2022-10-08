import peewee as pw

db = pw.SqliteDatabase('src/stockbot42.db') # initialize database in the bot/ directory

# base model to be inherited by all other models
# makes the already defined db the default for all new models
class BaseModel(pw.Model):
    class Meta:
        database = db

# corresponding to Mention table
class Mention(BaseModel):
    tweet_id = pw.CharField(primary_key=True) # store tweet ID in a string
    user_command = pw.CharField(null=True) # store user command given in tweet, allow null values for unrecognized commands
    user_screen_name = pw.CharField() # store author's @handle

# if running this file, initialize the database and create the Mention table
if __name__ == '__main__':
    db.connect()
    db.create_tables([Mention]) # create Mention table in the database
    db.close()