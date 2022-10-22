from datetime import datetime, timezone
import json
import mysql.connector
import pytz


val = []

with open('untweeted_mullen_posts.json', encoding="utf8") as j:
  for post in json.load(j):
    if post["mentions"] == [] and post["username"] == "nickmullen" and "http" not in post["tweet"]:
        datetime_str = post["date"] + " - " + post["time"]
        post_made = datetime.strptime(datetime_str, '%Y-%m-%d - %H:%M:%S')
        eastern = pytz.timezone('US/Eastern')
        post_made = eastern.localize(post_made)
        post_tuple = (post["id"], post_made, post["tweet"], False)
        val.append(post_tuple)
        print("\n" + "Values Appended: " + str(post_tuple) + "\n")

print("\n\n\n" + "Values to be Inserted: " + str(val) + "\n\n\n")

sql = "INSERT INTO posts (post_id, post_made, post, post_tweeted) VALUES (%s, %s, %s, %s)"

with mysql.connector.connect(host="dbhost", user="dbuser", password="dbpass", database="db") as db:
    cursor = db.cursor()
    cursor.executemany(sql, val)
    db.commit()
    print(cursor.rowcount, "was inserted.")
