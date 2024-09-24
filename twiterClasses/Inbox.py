import json
from typing import Dict
from .Tweet import Tweet

class Inbox:
    def __init__(self) -> None:
        self.__timeline: Dict[int, 'Tweet'] = {}
        self.__myTweets: Dict[int, 'Tweet'] = {}

    def storeInTimeline(self, tw: 'Tweet') -> None:
        self.__timeline.setdefault(tw.getId(), tw)

    def getListTimeline(self) -> None:
        return list(self.__timeline.values())

    def getTimeline(self) -> Dict[int, 'Tweet']:
        return self.__timeline

    def __str__(self) -> str:
        inboxTimelineStr = "TimeLine:\n"
        for tweet in self.__timeline.values():
            if not tweet.getDeleted():
                inboxTimelineStr += f"\n {tweet}"
        return inboxTimelineStr

    def myTweetsToString(self) -> str:
        myTweetsStr = ""
        for tweet in self.__myTweets.values():
            myTweetsStr += str(tweet)
        return myTweetsStr

    def getTweet(self, id: int) -> 'Tweet':
        return self.__timeline.get(id)

    def removeMsgFrom(self, other_username: str) -> None:
        keys_to_remove = [key for key, tweet in self.__timeline.items() if tweet.getUsername() == other_username]
        for key in keys_to_remove:
            self.__timeline.pop(key, None)

    def storeInMyTweets(self, tweet: Tweet) -> None:
        self.__myTweets[tweet.getId()] = tweet

    def getMyTweetsList(self):
        return list(self.__myTweets.values())

    def getMyTweets(self):
        return self.__myTweets

    def inboxToDict(self) -> Dict[str, Dict[int, 'Tweet']]:
        inboxDict = {
            'timeline' : {tweetId : tweet.TweetToDict() for tweetId, tweet in self.__timeline.items()},
            'myTweets' : {tweetId : tweet.TweetToDict() for tweetId, tweet in self.__myTweets.items()},
        }
        return inboxDict

    @staticmethod
    def inboxFromDict(dictInbox: Dict[str, Dict[int, 'Tweet']]) -> 'Inbox':
        inbox = Inbox()
        
        for tweetId, tweet in dictInbox['timeline'].items():
            newTweet: 'Tweet' = Tweet.TweetFromDict(tweet)
            inbox.storeInTimeline(newTweet)
        for tweetId, tweet in dictInbox['myTweets'].items():
            newTweet: 'Tweet' = Tweet.TweetFromDict(tweet)
            inbox.storeInMyTweets(newTweet)
        
        return inbox
    
    def inboxToJson(self) -> str:
        return json.dumps(self.inboxToDict())
    
    @staticmethod
    def inboxFromJson(jsonStr: str) -> 'Inbox':
        inboxDict = json.loads(jsonStr)
        return Inbox.inboxFromDict(inboxDict)
