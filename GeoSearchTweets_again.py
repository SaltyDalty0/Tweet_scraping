# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html
# GeoSearch crawler written by Chris Cantey, MS GIS/Cartography, University of Wisconsin, https://geo-odyssey.com
# MwSQLdb schema written with great assistance from Steve Hemmy, UW-Madison DoIT


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
#import MySQLdb
import csv
import random

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers
consumer_key="D8DiofhoTFgG0wXbnxaaU5uDg"
consumer_secret="INt7LcBH2Nrjs94pY8nGghQ5PPkPna4g9HNHaqfXSjak4lplal"

access_token="1255409204187344896-CMpDfVhWWq0LQd0YxUbFbHJs6gA3sG"
access_token_secret="BoZ0TUiVNJy1oLjox6buvQHAucxw0BYkUcK2ZHYzggQ5L"

# Create your MySQL schema and connect to database, ex: mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpwd');
#db=MySQLdb.connect(host='localhost', user='root', passwd='newpwd', db='twitter')
#db.set_character_set('utf8')

Coords = dict()
XY = []
#curr=db.cursor()

#per request, write output to csv, rather than mysql. Be aware of limited rows to csv. The streaming API will return millions of rows per day.
csvfile = open('geopy_results.csv','wb')
csvwriter = csv.writer(csvfile)
tweets_list=[]
#csvwriter.writerow(['UserID', 'Date', 'Lat', 'Long', 'Text'])

class StdOutListener(StreamListener):
                """ A listener handles tweets that are the received from the stream.
                This is a basic listener that inserts tweets into MySQLdb.
                """
                
                def __init__(self, api=None):
                    super(StdOutListener, self).__init__()
                    self.num_tweets = 0
                
                def on_status(self, status):
                                print("Tweet Text: ",status.text)
                                text = status.text
                                print("Time Stamp: ",status.created_at, status.coordinates)
                                self.num_tweets += 1
                                if self.num_tweets < 20:
                                    return True
                                else:
                                    return False
                                try:
                                    Coords.update(status.coordinates)
                                    XY = (Coords.get('coordinates'))  #Place the coordinates values into a list 'XY'
                                    print("X: ", XY[0])
                                    print("Y: ", XY[1])
                                except:
                                    #Often times users opt into 'place' which is neighborhood size polygon
                                    #Calculate center of polygon
                                    Box = status.place.bounding_box.coordinates[0]
                                    XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
                                    print("X: ", XY[0])
                                    print("Y: ", XY[1])
                                    pass
                               
                                #tweets_list+=
                                #print([unicode(status.id_str).encode("utf-8"),unicode(status.created_at).encode("utf-8"),XY[1],XY[0],unicode(status.text).encode("utf-8")])
                                #csvwriter.writerow(
                                print([status.text.encode("utf-8"), status.id_str, status.created_at, XY[1], XY[0]])
                                #[unicode(status.id_str).encode("utf-8"),unicode(status.created_at).encode("utf-8"),XY[1],XY[0],unicode(status.text).encode("utf-8")])
                                # Comment out next 4 lines to avoid MySQLdb to simply read stream at console
                                #curr.execute("""INSERT INTO TwitterFeed2 (UserID, Date, Lat, Lng, Text) VALUES
                                    #(%s, %s, %s, %s, %s);""",
                                    #(status.id_str,status.created_at,XY[1],XY[0],text))
                                #db.commit()
                                
                                #Alternatively write to CSV. CSV's. limited
                            
                                if self.num_tweets < 20:
                                    return True
                                else:
                                    return False
                      

def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, timeout=30.0)
    #Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
    while True:
        try:
            # Call tweepy's userstream method
            # Use either locations or track, not both
            stream.filter(locations=[-125,25,-65,48])##These coordinates are approximate bounding box around USA
            print("\n\n\nbruh\n\n\n")
            #stream.filter(track=['obama'])## This will feed the stream all mentions of 'keyword'
            break
        except Exception as e:
             # Abnormal exit: Reconnect
             nsecs=random.randint(60,63)
             time.sleep(nsecs)
    for tweet in tweets_list:
        csvwriter.writerow([tweet])

if __name__ == '__main__':
    main()
