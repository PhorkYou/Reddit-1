import praw
import time
import bot
import sqlite3

#Configurable variables

USERAGENT = "/u/redditbot1 reddit bot" #description (must include username)
USERNAME = bot.username
PASSWORD = bot.password
SUBREDDIT = "test" 
MAXPOSTS = 10 #can range from 1 to 100

SETPHRASES = ["python", "bots"]
SETRESPONSE = "I am a python bot."

WAIT = 20 #The period of each scan

#Database things
print "Opening databse"
sql = sqlite3.connect("sql.db")
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
sql.commit()


print "Logging in to reddit."

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)


def replyBot():

    print "Fetching subreddit " + SUBREDDIT
    subreddit = r.get_subreddit(SUBREDDIT)

    print "Fetching comments"
    comments = subreddit.get_comments(limit*MAXPOSTS)

    for comment in comments:
        cid = comment.id

        cur.execute('SELECT * FROM oldposts WHERE ID=?', [cid])
        if not cur.fetchone():
            try:
                cauthor = comment.author.name
                if cauthoer.lower() == USERNAME.lower():
                    cbody = comment.body.lower()

                    if any(key.lower() in cbody for key in SETPHRASES):
                        print "Replying to " cauthor
                        comment.reply(SETRESPONSE)
                else: 
                    print "Will not reply to self."

            except AttributeError:
                pass

            cur.execute('INSERT INTO oldposts VALUES(?)', [cid])
            sql.commit()


while True:
    replyBot()
    print "Waiting " + str(WAIT) + "seconds"
    time.sleep(WAIT)


            
    
