from .Esqueleto import Esqueleto
from twiterClasses import*
from utils import Mensagem

class Despachante:

    def __init__(self):
            self.__esqueleto = Esqueleto() 

    def invoke(self, msg) -> str:
        messageDeserele = Mensagem.from_json(msg.decode('utf-8'))
        
        messageSerele = messageDeserele
        messageSerele.messageType = 1
        if messageDeserele.methodId == 'add':
            messageSerele.objectReference = self.__esqueleto.add(User.userFromJson(messageDeserele.objectReference))
        elif messageDeserele.methodId == 'login':
            messageSerele.objectReference = self.__esqueleto.login(messageDeserele.arguments)            
        elif messageDeserele.methodId == 'show':
            messageSerele.objectReference = self.__esqueleto.show(messageDeserele.arguments)
        elif messageDeserele.methodId == 'follow':
            messageSerele.objectReference = self.__esqueleto.follow(messageDeserele.arguments)
        elif messageDeserele.methodId == 'tweetar':
            messageSerele.objectReference = self.__esqueleto.tweetar(Tweet.from_json(messageDeserele.objectReference))
        elif messageDeserele.methodId == 'timeline':
            messageSerele.objectReference = self.__esqueleto.timeline(User.userFromJson(messageDeserele.objectReference))
        elif messageDeserele.methodId == 'like':
            messageSerele.objectReference = self.__esqueleto.like(messageDeserele.arguments)
        elif messageDeserele.methodId == 'unfollow':
            messageSerele.objectReference = self.__esqueleto.unfollow(messageDeserele.arguments)
        elif messageDeserele.methodId == 'rt':
            messageSerele.objectReference = self.__esqueleto.rt(messageDeserele.arguments)
        elif messageDeserele.methodId == 'rm':
            messageSerele.objectReference = self.__esqueleto.rm(messageDeserele.arguments)
        elif messageDeserele.methodId == 'end':
            messageSerele.objectReference = self.__esqueleto.end(messageDeserele.arguments)
            
        return messageSerele.to_json()