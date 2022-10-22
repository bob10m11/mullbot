from datetime import datetime, timezone
import json
import mysql.connector
import pytz


val = []

# posts_in_database = []


# with mysql.connector.connect(host="localhost", user="bob10m11", password="D@bears13", database="nick_mullen") as db:
    # cursor = db.cursor()
    # cursor.execute("SELECT post_id FROM posts;")
    # for pid in cursor.fetchall():
        # posts_in_database.append(pid)


with open('untweeted_mullen_posts.json', encoding="utf8") as j:
  for post in json.load(j):
    if post["mentions"] == [] and post["username"] == "nickmullen":
        if "http" in post["tweet"] or "pic.twitter" in post["tweet"]:
            tweet = post["tweet"]
            datetime_str = post["date"] + " - " + post["time"]
            post_made = datetime.strptime(datetime_str, '%Y-%m-%d - %H:%M:%S')
            eastern = pytz.timezone('US/Eastern')
            post_made = eastern.localize(post_made)
            if "pic.twitter" in tweet:
                original = post["tweet"]
                str_list = original.split("pic.twitter")
                photos = post["photos"]
                if not photos:
                    photos = [""]
                tweet = str_list[0] + photos[0]
            post_tuple = (post["id"], post_made, tweet, False)
            val.append(post_tuple)
            print("\n" + "Values Appended: " + str(post_tuple) + "\n")

print("\n\n\n" + "Values to be Inserted: " + str(val) + "\n\n\n")

sql = "INSERT INTO picture_posts (post_id, post_made, post, post_tweeted) VALUES (%s, %s, %s, %s)"

with mysql.connector.connect(host="host", user="dbuser", password="dbpass", database="db") as db:
    cursor = db.cursor()
    cursor.executemany(sql, val)
    db.commit()
    print(cursor.rowcount, "was inserted.")


