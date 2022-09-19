import peewee as pw

db = pw.SqliteDatabase('stockbot42.db')

class BaseModel(pw.Model):
    class Meta:
        database = db

class Mention(BaseModel):
    tweet_id = pw.CharField(primary_key=True) # store tweet ID in a string
    user_command = pw.CharField(null=True) # store user command given in tweet, allow null values for unrecognized commands
    user_screen_name = pw.CharField() # store author's @handle

if __name__ == '__main__':
    db.connect()
    db.create_tables([Mention]) # create Mention table in the database
    db.close()