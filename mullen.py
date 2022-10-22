import mysql.connector
import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("key", 
    "key")
auth.set_access_token("token", 
    "token")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)


with mysql.connector.connect(host="dbip", user="dbuser", password="dbpass", database="dbname") as db:
    cursor = db.cursor()
    post_id = 0
    cursor.execute("SELECT id, post FROM posts WHERE post_tweeted = false ORDER BY RAND() LIMIT 1;")
    post = cursor.fetchall()
    post_number = 0
    for p in post:
        print("Updating status...")
        api.update_status(str(p[1]))
        print("Status updated: '" + str(p[1]))
        post_id = p[0]
        post_number += 1
    if post_number == 0:
        cursor.execute("UPDATE posts SET post_tweeted = false")
    else:
        cursor.execute("UPDATE posts SET post_tweeted = true WHERE id = %d" % post_id)
    print("Post %d updated" % post_id)
    db.commit()

quit()
