from typing import Dict
import json

class Tweet:
	def __init__(self, id: int, username: str, message: str):
		self.__id: int = id
		self.__username: str = username
		self.__message: str = message
		self.__likes: list = []
		self.__rt: 'Tweet' = None
		self.__deleted: bool = False
    
	def __str__(self) -> str:
		stringTweet: str = ''
		likesStr = f"Likes: {', '.join(self.__likes)}"
		if(self.__deleted):
			stringTweet = ''
		else:
			stringTweet += str(self.__id) + ":" + self.__username +" - (" + self.__message + "), " + likesStr

			if(self.__rt != None):
				if(self.__rt.getDeleted()):
					stringTweet += "\n      "
					stringTweet += str(self.__id) + ": UserRemoved - (Esse tweet não está mais dispónível), " + likesStr
				stringTweet += "\n      ";
				stringTweet += str(self.__rt)
		return stringTweet

	def setRt(self,tweet: 'Tweet'):
		self.__rt = tweet

	def like(self, username: str):
		if username not in self.__likes:
			self.__likes.append(username)

	def setId(self, newId) -> None:
		self.__id = newId

	def getLikes(self):
		return self.__likes

	def getId(self) -> int:
		return self.__id

	def getUsername(self) -> str:
		return self.__username

	def setUsername(self, new_username: str):
		self.__username = new_username

	def get_message(self) -> str:
		return self.__message

	def getDeleted(self) -> bool:
		return self.__deleted

	def setDeleted(self, state: bool):
		self.__deleted = state

	def TweetToDict(self) -> Dict:
		tweetDict = {
			'id' : self.__id,
			'username' : self.__username,
			'message' : self.__message,
			'likes' : list(self.__likes),
			'rt' : self.__rt.TweetToDict() if self.__rt else None,
			'deleted' : self.__deleted
		}
		return tweetDict

	@staticmethod
	def TweetFromDict(dictTweet: Dict[str,str]) -> 'Tweet':  
		# Criando uma nova instância de Tweet usando os dados do dicionário
		tweet = Tweet(
			id = dictTweet['id'],
			username = dictTweet['username'],
			message = dictTweet['message']
		)

		# Adicionando likes usando o método like()
		for like_user in dictTweet['likes']:
			tweet.like(like_user)

		# Definindo o estado de "deletado" usando o método setDeleted()
		tweet.setDeleted(dictTweet['deleted'])

		# Se houver um retweet, reconstrua o Tweet de retweet e associe
		if dictTweet.get('rt'):
			rt_tweet = Tweet.TweetFromDict(dictTweet['rt'])  # Recursivamente cria o retweet
			tweet.setRt(rt_tweet)

		return tweet

	def to_json(self) -> str:
		return json.dumps(self.TweetToDict())

	@staticmethod
	def from_json(json_str: str) -> 'Tweet':
		tweetDict = json.loads(json_str)
		return Tweet.TweetFromDict(tweetDict)