import json
from typing import Dict
from .Inbox import Inbox
from .Tweet import Tweet

class User:
	def __init__(self, userName: str) -> None:
		self.__userName: str = userName
		self.__inbox: 'Inbox' = Inbox()
		self.__followers: Dict[str, 'User'] = {}
		self.__following: Dict[str, 'User'] = {}

	def __str__(self) -> str:
		printFollowing = str(list(self.__following.keys()))
		printFollowers = str(list(self.__followers.keys()))
		userString: str = self.__userName + ':\nSeguindo - ' + printFollowing + '\nSeguidores - ' + printFollowers
		return userString

	def addFollower(self, follower: 'User') -> None:
		self.__followers.setdefault(follower.getUsername(), follower)

	def follow (self, otherUser: 'User') -> None:
		self.__following.setdefault(otherUser.getUsername(),otherUser)
		otherUser.addFollower(self)

	def dropFollower(self, otherUser:str):
		key_to_remove = None
		for key, value in self.__followers.items():
			if value.getUsername() == otherUser:
				key_to_remove = key
				break  

		if key_to_remove is not None:
			del self.__followers[key_to_remove]				

	def getInbox(self) -> 'Inbox':
		return self.__inbox

	def sendTweet (self, tw: 'Tweet') -> None:
		if (tw.getUsername() == self.__userName):
			self.__inbox.storeInMyTweets(tw)
			self.__inbox.storeInTimeline(tw)
		else:
			self.__inbox.storeInTimeline(tw)

	def like (self, idTweet: int) -> None:
		for value in self.__inbox.getTimeline().values():
			if(value.getId() == idTweet):
				value.like(self.getUsername())
				

	def unfollow(self, otherUsername: str) -> None:
		self.__inbox.removeMsgFrom(otherUsername)
		del self.__following[otherUsername]

	def unfollowAll(self) -> None:
		keysToRemove = []

		for key, value in self.__inbox.getTimeline().items():
			if (value.getUsername() != self.__userName):
				keysToRemove.append(key)
    
		for key in keysToRemove:
			# del self.__inbox.__timeline[key]
			del self.__inbox.getTimeline()[key]
		
		self.__inbox.getTimeline().clear()

	def rejectAll(self) -> None:
		self.__followers.clear()
		self.unfollowAll()
		for key, value in self.__inbox.getMyTweets().items():
			value.deleted = True
 
	def setUserName(self, newUsername: str):
		self.__userName = newUsername

	def getUsername(self) -> str:
		return self.__userName

	def getInbox(self) -> 'Inbox':
		return self.__inbox

	def getFollowers(self) -> Dict[str, 'User']:
		return self.__followers
	def getFollowing(self) -> Dict[str, 'User']:
		return self.__following

	def userToDict(self) -> Dict:
		userDict = {
			'username': self.__userName,
			'inbox': self.__inbox.inboxToDict(),
			'followers': list(self.__followers.keys()),  # Apenas nomes de usuário
			'following': list(self.__following.keys()),  # Apenas nomes de usuário
		}
		return userDict

	@staticmethod
	def userFromDict(dictUser: Dict) -> 'User':
		# Criando o objeto User a partir do nome de usuário
		user = User(dictUser['username'])
		
		# Reconstruindo a inbox a partir do dicionário
		inbox = Inbox.inboxFromDict(dictUser['inbox'])
		user.__inbox = inbox  # Atribui a inbox recriada ao usuário
		
		# Reconstruindo os seguidores
		for followerUsername in dictUser['followers']:
			follower = User(followerUsername)  # Cria um novo objeto User
			user.addFollower(follower)  # Usando o método para adicionar o seguidor

		# Reconstruindo os seguidos
		for followingUsername in dictUser['following']:
			following = User(followingUsername)  # Cria um novo objeto User
			user.follow(following)  # Usando o método follow para seguir o usuário

		return user

	def userToJson(self) -> str:
		return json.dumps(self.userToDict())

	@staticmethod
	def userFromJson(jsonStr: str) -> 'User':
		userDict = json.loads(jsonStr)
		return User.userFromDict(userDict)