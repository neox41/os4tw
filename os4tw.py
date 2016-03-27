#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
os4tw v.0.1 - OSINT and Digital Investigation tool for Twitter

#########################################################################
#                                                                     	#
# Developed by Mattia Reggiani, info@mattiareggiani.com               	#
#                                                                     	#
# This program is free software: you can redistribute it and/or modify	#
# it under the terms of the GNU General Public License as published by	#
# the Free Software Foundation, either version 3 of the License, or	#
# (at your option) any later version.					#
#									#
# This program is distributed in the hope that it will be useful,      	#
# but WITHOUT ANY WARRANTY; without even the implied warranty of       	#
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        	#
# GNU General Public License for more details.                         	#
#                                                                      	#
# You should have received a copy of the GNU General Public License    	#
# along with this program. If not, see <http://www.gnu.org/licenses/>  	#
#                                                                      	#
# Released under the GNU Affero General Public License                 	#
# (https://www.gnu.org/licenses/agpl-3.0.html)                         	#
#########################################################################

WARNING: the potential of this program is limited by the API limitations provided by Twitter
	For further information, please visit https://dev.twitter.com/rest/public/rate-limits
	
Usage examples:
	Check users friendship
	./os4tw.py -f mattia_reggiani os4tw 
	
	Search news by keyword
	./os4tw.py -s osint
	
	Get places frequented by User
	./os4tw.py -p mattia_reggiani
"""


import tweepy, sys, time, json, collections, argparse, httplib

__version__='v0.1'
__description__='''\
  ___________________________________________________________
  
  os4tw - OSINT and Digital Investigation tool for Twitter
  Author: Mattia Reggiani (info@mattiareggiani.com)
  Github: https://github.com/mattiareggiani/os4tw
  ___________________________________________________________
'''

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
from keys import tweekeys

SCREEN_NAME = tweekeys['screen_name']
CONSUMER_KEY = tweekeys['consumer_key']
CONSUMER_SECRET = tweekeys['consumer_secret']
ACCESS_TOKEN = tweekeys['access_token']
ACCESS_TOKEN_SECRET = tweekeys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#api = tweepy.API(auth, wait_on_rate_limit=True)
api = tweepy.API(auth)

def getFollower(profile):
    i = 0
    l = []
    printColour("\n[*] ", BLUE)
    print "Follower list:\n"
    for user in tweepy.Cursor(api.followers, screen_name=profile, count=200).items():
		try:
			l.append(user.screen_name)
			i = i + 1
		except:
			print "[-] Timeout, sleeping for 15 minutes..."
			time.sleep(15*60)
    for user in l:
		printColour("[+] @" + user, GREEN)
		print(" (https://www.twitter.com/" + user + ")\n")
    printColour("\n[*] ", CYAN)
    print "Total follower: " + str(len(l)-1) + "\n"

def getFollowing(profile):
    i = 0
    l = []
    printColour("\n[*] ", BLUE)
    print "Following list:\n"
    for user in tweepy.Cursor(api.friends, screen_name=profile, count=200).items():
		try:
			l.append(user.screen_name)
			i = i + 1
		except:
			print "[-] Timeout, sleeping for 15 minutes..."
			time.sleep(15*60)
    for user in l:
		printColour("[+] @" + user, GREEN)
		print(" (https://www.twitter.com/" + user + ")\n")
    printColour("\n[*] ", CYAN)
    print "Total following: " + str(len(l)-1) + "\n"

def getConnection(profile1, profile2):
    followerProfile1 = []
    for user in tweepy.Cursor(api.followers, screen_name=profile1).items():
        followerProfile1.append(user.screen_name)
    followerProfile2 = []
    for user in tweepy.Cursor(api.followers, screen_name=profile2).items():
        followerProfile2.append(user.screen_name)
    sharedFollower = []
    for i in len(followerProfile1):
        for e in len(followerProfile2):
            if (followerProfile1[i] == followerProfile2[e]):
                sharedFollower.append(followerProfile1[i])
                print "[*] " + followerProfile1[i]
    print "\n[+] Total shared follower " + str(len(sharedFollower)) + "\n"

    followingProfile1 = []
    for user in tweepy.Cursor(api.followers, screen_name=profile1).items():
        followingProfile1.append(user.screen_name)
    followingProfile2 = []
    for user in tweepy.Cursor(api.followers, screen_name=profile2).items():
        followingProfile2.append(user.screen_name)
    sharedFollowing = []
    for i in len(followingProfile1):
        for e in len(followingProfile2):
            if (followingProfile1[i] == followingProfile2[e]):
                sharedFollowing.append(followingProfile1[i])
                print "[*] " + followingProfile1[i]
    print "\n[+] Total shared following " + str(len(sharedFollowing)) + "\n"

    getSharedFollower(profile1Follower,profile2Follower)

def showFriendship(profileList):
    friends = []
    printColour("\n[*] ", BLUE)
    print "Users connected:\n"
    i = 0
    x = 0
    for profile1 in profileList:
        for profile2 in profileList[x:]:
            if profile1 != profile2:
                friendship = api.show_friendship(source_screen_name=profile1, target_screen_name=profile2)
                if (friendship[0].followed_by and friendship[0].following):
                        printColour ("[+] "+ profile1 + " <---> " + profile2 + "\n", GREEN)
                        i += 1
                else:
                    continue
        x += 1
    printColour("\n[*] ", CYAN)
    print "Total connection: " + str(i) + "\n"

def cyberSquatting(s): # Function inspired to https://github.com/elceef/dnstwist
    result = []
    # Addidion
    for i in range(97, 123):
        result.append(s + chr(i))

    for i in range(0, 10):
        result.append(s + str(i))

    result.append(s + chr(95))

    for i in range(1, len(s)):
        result.append(s[:i] + '_' + s[i:])
    # Insertion
    for i in range(1, len(s)):
        for key in range(97, 123):
            result.append(s[:i] + chr(key) + s[i:])
    for i in range(1, len(s)):
        for key in range(0, 10):
            result.append(s[:i] + str(key) + s[i:])
    for i in range(1, len(s)):
        result.append(s[:i] + '_' + s[i:])
    # Omission
    for i in range(0, len(s)):
        result.append(s[:i] + s[i+1:])
    # Repetition
    for i in range(0, len(s)):
        result.append(s[:i] + s[i] + s[i] + s[i+1:])
    # Homoglyph
    glyphs = {
        'd': ['b', 'cl', 'dl', 'di'], 'm': ['n', 'nn', 'rn', 'rr'], 'l': ['1', 'i'],
        'o': ['0'], 'k': ['lk', 'ik', 'lc'], 'h': ['lh', 'ih'], 'w': ['vv'],
        'n': ['m', 'r'], 'b': ['d', 'lb', 'ib'], 'i': ['1', 'l'], 'g': ['q'], 'q': ['g'],
        }
    for ws in range(0, len(s)):
        for i in range(0, (len(s)-ws)+1):
            win = s[i:i+ws]
            j = 0
            while j < ws:
                c = win[j]
                if c in glyphs:
                    win_copy = win
                    for g in glyphs[c]:
                        win = win.replace(c, g)
                        result.append(s[:i] + win + s[i+ws:])
                        win = win_copy
                j += 1
    # Trasposition
    for i in range(0, len(s)-1):
        if s[i+1] != s[i]:
            result.append(s[:i] + s[i+1] + s[i] + s[i+2:])
    # Replacement
    for i in range(0, len(s)):
        for key in range(97, 123):
            result.append(s[:i] + chr(key) + s[i+1:])
    for i in range(0, len(s)):
        for key in range(0, 10):
            result.append(s[:i] + str(key) + s[i+1:])
    for i in range(0, len(s)):
        result.append(s[:i] + '_' + s[i+1:])
    c = 0
    q = 0
    i = 0
    for i in range(0, len(result)):
        if len(result[i]) < 16:
            q+=1
    printColour("\n[*] ", BLUE)
    print "Profile typesquatted\n"	
    conn = httplib.HTTPSConnection("twitter.com")
    for i in range(0, len(result)):
		if len(result[i]) > 15:
			continue
		else:
			if checkUserExist(conn, result[i]):
				printColour("[+] @" + result[i], GREEN)
				print (" (https://www.twitter.com/" + result[i] + ")\n")
				i += 1
			c+=1
			'''if (c==5):
				time.sleep(2)
				c=0'''
    printColour("\n[*] ", CYAN)
    print "Total profile typesquatted: " + str(i) + "\n"

def checkUserExist(conn, user):
	hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1' }
	conn.request("GET", "/" + user, headers=hdr)
	r = conn.getresponse()
	#print r.status, r.reason
	data = r.read()
	if r.status == 200:
		return True
	elif (r.status == 404) or (r.status == 302):
		return False
	else:
		print "Error " + user
		return False

def getTweets(screen_name):
    allTweets = []
    i = 0
    newTweets = api.user_timeline(screen_name = screen_name,count=200)
    allTweets.extend(newTweets)
    printColour("\n[*] ", BLUE)
    print "Getting Tweets..."
    oldest = allTweets[-1].id - 1
    while len(newTweets) > 0:
		newTweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		allTweets.extend(newTweets)
		oldest = allTweets[-1].id - 1
		print "[*] %s Tweets downloaded" % (len(allTweets))
    for tweet in allTweets:
		i += 1
		printColour("[+] " + str(tweet.id_str) + " - " + str(tweet.created_at) + " - " + str(tweet.text.encode("utf-8")), GREEN)
		print "\n"
    printColour("\n[*] ", CYAN)
    print "Total Tweets downloaded: " + str(i) + "\n"
    print "\n"

def getPlaces(screen_name):
    allTweets = []
    tmp = []
    i = 0
    newTweets = api.user_timeline(screen_name = screen_name,count=200)
    allTweets.extend(newTweets)
    oldest = allTweets[-1].id - 1
    printColour("\n[*] ", BLUE)
    print "Getting Tweets..."
    while len(newTweets) > 0:
		newTweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		allTweets.extend(newTweets)
		oldest = allTweets[-1].id - 1
		print "[*] %s Tweets downloaded" % (len(allTweets))
    for tweet in allTweets:
        if tweet.place is not None:
            if tweet.place.name not in tmp:
                tmp.append(tweet.place.name)
                i += 1
                print "\n"
                printColour("[+] Place found: " + tweet.place.full_name + " - " + tweet.place.country + " (" + tweet.place.country_code + ")", GREEN)
    printColour("\n[*] ", CYAN)
    print "Total places found: " + str(i) + "\n"
    print "\n"

def search(s):
    c = tweepy.Cursor(api.search, q=s, count=100)
    userMentionsList = []
    tweetList = []
    hashtagList = []
    locationList = []
    authorList = []
    print "\n"
    for tweet in c.items():
        text = tweet.text
        userMentions = tweet.entities.get('user_mentions')
        hashtag = tweet.entities.get('hashtags')
        location = tweet.entities.get('location')
        author = tweet.user.screen_name
        printColour("[+] ", GREEN)
        print "@" + author + ": " + text + "\n"
        tweetList.append(text)
        authorList.append(author)
        if userMentions:
            for m in userMentions:
                #print "[+] Mentions: " + m.get('screen_name')
                userMentionsList.append(m.get('screen_name'))
        if hashtag:
            for h in hashtag:
                hashtagList.append(h.get('text'))
        if location:
            locationList.append(location)
    counterM = collections.Counter()
    counterT = collections.Counter()
    counterH = collections.Counter()
    counterL = collections.Counter()
    counterA = collections.Counter()
    printColour("[*] ", CYAN)
    print "Summary:\n"
    for i in authorList:
        counterA[i] +=1
    printColour("[+] ", GREEN)
    print "Users:"
    for u in counterA.most_common(15):
		print str(u[0]) + " (" + str(u[1]) + " tweets)"
    for i in hashtagList:
        counterH[i] +=1
    printColour("\n[+] ", GREEN)
    print "Hashtag:"
    for h in counterH.most_common(15):
		print str(h[0]) + " (" + str(h[1]) + " tweets)"
    for i in userMentionsList:
        counterM[i] +=1
    printColour("\n[+] ", GREEN)
    print "Mentiones:"
    for m in counterM.most_common(15):
		print str(h[0]) + " (" + str(h[1]) + " tweets)"

def rogue(s):
	printColour("\n[*] ", BLUE)
	c = 0
	print "Potential rogue profile:\n"
	pageList = []
	tmp = []
	i=0
	for page in tweepy.Cursor(api.search_users, q=s, include_entities=False, count=20).pages():
		if (c>30): # Counter to limit the request
			break
		c +=1 
		for result in page:
			if result.screen_name not in tmp:
				i += 1
				tmp.append(result.screen_name)
				printColour("[+] " + result.name + " (@" + result.screen_name + ")", GREEN)
				print "\n"
	printColour("\n[*] ", CYAN)
	print "Total potential rogue profile: " + str(i) + "\n"

def has_colours(stream):
    if not (hasattr(stream, "isatty") and stream.isatty()):
        return False
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # TODO: log console
        return False

has_colours = has_colours(sys.stdout)
def printColour(text, colour=WHITE):
    """

    :rtype: object
    """
    if has_colours:
        seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)

def main():
	parser = argparse.ArgumentParser(
		version=__version__,
		formatter_class=argparse.RawTextHelpFormatter,
		prog='os4tw.py',
		description=__description__)
	
	parser.add_argument('-ts', help='Get Social Profile typesquotted', dest="username_ts", metavar="USERNAME", required=False)
	parser.add_argument('-r', help='Get Social Profile rogue', dest="username_r", metavar="USERNAME", required=False)
	parser.add_argument('-fe', help='Get User Followers', dest="username_fe", metavar="USERNAME", required=False)
	parser.add_argument('-fi', help='Get User Following', dest="username_fi", metavar="USERNAME", required=False)
	parser.add_argument('-p', help='Get places frequented by User', dest="username_p", metavar="USERNAME", required=False)
	parser.add_argument('-tw', help='Get Users tweets Timeline', dest="username_tw", metavar="USERNAME", required=False)
	
	parser.add_argument('-s', help='Search function by Keyword', dest="query", metavar="KEYWORD", required=False)
	
	parser.add_argument('-f', help='Get Users Friendship', nargs='+', dest="username_f", metavar="USERNAME", required=False)
	
	args = parser.parse_args()

	ts = args.username_ts
	r = args.username_r
	fe = args.username_fe
	fi = args.username_fi
	s = args.query
	p = args.username_p
	f = args.username_f
	tw = args.username_tw
	
	if ts:
		print __description__
		cyberSquatting(ts)
	elif r:
		print __description__
		rogue(r)
	elif fe:
		print __description__
		getFollower(fe) 
	elif fi:
		print __description__
		getFollowing(fi) 
	elif p:
		print __description__
		getPlaces(p) 
	elif f:
		print __description__
		showFriendship(f) 
	elif tw:
		print __description__
		getTweets(tw)
	elif s:
		print __description__
		search(s) 
	else:
		print "Usage ./os4tw.py [option]"
		print "Error arguments: missing mandatory option. Use ./os4tw.py -h to help\n"
		exit()
    
if __name__ == "__main__":
	main()


