from typing import Dict
from .Tweet import Tweet
from .Inbox import Inbox
from .User import User

class Twiter:
	def __init__(self) -> None:
		self.__nextTweetId: int = 0
		self.__users: Dict[str, 'User'] = {}
		self.__tweets: Dict[int, 'Tweet'] = {}

		self.popular()

	def isUserExists(self, userName: str) -> bool:
		return userName in self.__users

	def addUser(self, userName: str) -> None:
		if userName not in self.__users:
			self.__users[userName] = User(userName)

	def addUser2(self, newUser: 'User') -> bool:
		username = newUser.getUsername()
		if username in self.__users:
			return False  
		else:
			self.__users[username] = newUser
			return True

	def sendTimline(self, user: 'User') -> 'Inbox':
		return self.getUserByUsername(user.getUsername()).getInbox().inboxToJson()
 

	def __str__(self) -> str:
		controlerString = ''
		for key, value in self.__users.items():
			controlerString += '\n' + str(value) + '\n'
		return controlerString

	def createTweet(self, senderUsername: str, msg: str) -> 'Tweet':
		self.__nextTweetId += 1
		aux: int = self.__nextTweetId
		newTweet = Tweet(aux, senderUsername, msg)
		self.__tweets.setdefault(aux, newTweet)
		return newTweet

	def createTweetRemote(self, newTweet: 'Tweet') -> 'Tweet':
		self.__nextTweetId += 1
		newTweet.setId(self.__nextTweetId)
		self.__tweets.setdefault(newTweet.getId(), newTweet)
		return newTweet

	def getUserByUsername(self, userName: str) -> 'User':
		return self.__users[userName]

	def sendTweet(self, userName: str, msg: str) -> None:
		aux: 'Tweet' = self.createTweet(userName, msg)
		self.getUserByUsername(userName).sendTweet(aux)

		for key, value in self.getUserByUsername(userName).getFollowers().items():
			value.sendTweet(aux)

	def sendTweetRemote(self, tweet: 'Tweet') -> str:
		newTweet = self.createTweetRemote(tweet)
		self.getUserByUsername(tweet.getUsername()).sendTweet(tweet)
		
		for key, value in self.getUserByUsername(tweet.getUsername()).getFollowers().items():
			value.sendTweet(tweet)
		return newTweet.to_json()

	def like(self, userName: str, tweetId: int) -> bool:
		if tweetId < 0 or tweetId > self.__nextTweetId:
			return False
		else:
			self.getUserByUsername(userName).like(tweetId)
			return True
  
	def likeRemote(self, userName: str, tweetId: int) -> str:

		if tweetId not in self.getUserByUsername(userName).getInbox().getTimeline().keys():
			return "Tweet inexistente"
		
		if tweetId < 0 or tweetId > self.__nextTweetId:
			return "Tweet inexistente"
		else:
			self.getUserByUsername(userName).like(tweetId)
			return self.getUserByUsername(userName).getInbox().getTweet(tweetId).to_json()

	def follow (self, userName: str, otherUser: str) -> str:
		if ((otherUser not in self.__users.keys()) or otherUser == userName):
			return "Usuario inexistente"
		else:
			self.getUserByUsername(userName).follow(self.getUserByUsername(otherUser))
			return str(self.getUserByUsername(userName)) + "\n\nSeguiu:\n\n" + str(self.getUserByUsername(otherUser)) 

	def unfollow(self, userName: str, otherUser: str) -> str:
		if (otherUser not in self.__users.keys() or otherUser == userName):
			return "Usuario inexistente"
		else:
			self.getUserByUsername(userName).unfollow(otherUser)
			self.getUserByUsername(otherUser).dropFollower(userName)
			return str(self.getUserByUsername(userName)) + "\n\nDeixou de seguir:\n\n" + str(self.getUserByUsername(otherUser)) 

	def unfollowAll(self, username: str) -> None:
		self.getUserByUsername(username).unfollowAll()
		for key, value in self.__users.items():
			if(username in value.getFollowers().keys()):
				del value.getFollowers()[username]


	def sendRt(self, userName: str, tweetId: int, rtMsg: str) -> str:
		if tweetId not in self.getUserByUsername(userName).getInbox().getTimeline().keys():
			return "Tweet inexistente"

		if tweetId < 0 or tweetId > self.__nextTweetId:
			return "Tweet inexistente"
		else:
			aux: 'Tweet' = self.createTweet(userName, rtMsg)
			aux.setRt(self.__tweets[tweetId])
			self.getUserByUsername(userName).sendTweet(aux)

			for value in self.getUserByUsername(userName).getFollowers().values():
				value.sendTweet(aux)			
			
			return aux.to_json()
			

	def removeUser(self, userName: str) -> None:
		self.getUserByUsername(userName).rejectAll()
		self.unfollowAll(userName)

		for key, value in self.__users.items():
			# del value.__following[userName]
			if userName in value.getFollowing():
				del value.getFollowing()[userName]


		del self.__users[userName]
  
	
	def popular(self):
		self.addUser("marcus");
		self.addUser("mason");
		self.addUser("rose")
		self.addUser("anne")
		self.getUserByUsername("marcus").follow(self.getUserByUsername("rose"));
		self.getUserByUsername("marcus").follow(self.getUserByUsername("anne"));
		self.getUserByUsername("marcus").follow(self.getUserByUsername("mason"));
		self.getUserByUsername("rose").follow(self.getUserByUsername("marcus"));
		self.getUserByUsername("rose").follow(self.getUserByUsername("anne"));
		self.getUserByUsername("rose").follow(self.getUserByUsername("mason"));
		self.getUserByUsername("anne").follow(self.getUserByUsername("rose"));
		self.getUserByUsername("anne").follow(self.getUserByUsername("marcus"));
		self.getUserByUsername("anne").follow(self.getUserByUsername("mason"));
		self.getUserByUsername("mason").follow(self.getUserByUsername("rose"));
		self.getUserByUsername("mason").follow(self.getUserByUsername("anne"));
		self.getUserByUsername("mason").follow(self.getUserByUsername("marcus"));

		self.sendTweet("marcus", "oioi");
		self.sendTweet("rose", "olaaa");
		self.sendTweet("anne", "oiiii");
		self.sendTweet("mason", "oioi amigos");
		self.sendTweet("marcus", "videogame com o mason");
		self.sendTweet("mason", "contra você é fácil");
		self.sendTweet("rose", "chocolate é muito bom");
		self.sendTweet("mason", "também quero");
		self.sendTweet("rose", "kkkk");

		self.like("marcus", 2);
		self.like("marcus", 3);
		self.like("marcus", 4);
		self.like("marcus", 5);
		self.like("mason", 5);
		self.like("mason", 2);
		self.like("rose", 4);
		self.like("rose", 1);
		self.like("mason", 1)