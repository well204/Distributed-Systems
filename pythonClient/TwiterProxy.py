from typing import List
import json
from .UDPClient import UDPClient
from utils import Mensagem
from twiterClasses import *


class TwiterProxy:
    def __init__(self):
        self.__requestId: int = 0
        self.__client = UDPClient('localhost',60000)

    def doOperation(self, objectReference: str, methodId: str, arguments: List[str]):
        self.__requestId += 1
        message = Mensagem(0,self.__requestId,objectReference,methodId, arguments)
        try:
            # Serializa a mensagem para JSON
            serialized_message = message.to_json()
            
            # Envia a mensagem para o servidor
            self.__client.sendRequest(serialized_message)

            response = self.__client.getResponse()
            # Deserializa a resposta
            
            return json.loads(response[0].decode('utf-8'))
        except AttributeError:
            print('alguma coisa')

    def add(self, userName: str) -> bool:
        newUser = User(userName)
        # request = 'username,add,,'
        request = userName + ',add,,'
        argumentsList = request.split(',')

        finalResponse = self.doOperation(newUser.userToJson(),'add',argumentsList)
        
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        
        if(mensagem.objectReference == 'Usuário já existe'):
            print("\nUsuário já existe")
            return False
        else:
            recievedUser: 'User' = User.userFromJson(mensagem.objectReference)
            
            print("\nUsuário adicionado com sucesso: " + str(recievedUser))
            return True



    def show (self, username: str) -> None:
        # request = 'username,show,,'
        request = username + ',show,,'
        argumentsList = request.split(',')

        finalResponse = self.doOperation('objRef','show',argumentsList)
        
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        print("\n" + mensagem.objectReference)



    def follow(self, userName: str, otherUser: str) -> None:
        # request = 'username,follow,otherUser,'
        request = userName +',follow,' + otherUser +','
        argumentsList = request.split(',')

        finalResponse = self.doOperation('objRef','follow',argumentsList)
        
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        
        print("\n" + mensagem.objectReference)

    def tweetar (self, userName: str, tweetMsg: str) -> None:
        newTweet = Tweet(-1,userName,tweetMsg)
        # request = 'username,tweetar,twMsg,'
        request = userName + ',tweetar,' + tweetMsg +','
        argumentsList = request.split(',')

        finalResponse = self.doOperation(newTweet.to_json(),'tweetar',argumentsList)
        
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        
        postedTweet: 'Tweet' = Tweet.from_json(mensagem.objectReference)
        
        print("\n" + 'Tweet postado:\n' + str(postedTweet))

    def timeline(self, userName: str) -> None:
        # request = 'username,timeline,,'
        
        userWhoRequest = User(userName)
        request = userName + ',timeline,,'
        argumentsList = request.split(',')

        finalResponse = self.doOperation(userWhoRequest.userToJson(),'timeline',argumentsList)
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        
        userInbox: 'Inbox' = Inbox.inboxFromJson(mensagem.objectReference)

        print("\n" + str(userInbox))
        # print("\n" + mensagem.objectReference)

    def like(self, userName: str, tweetId: int) -> None:
        # request = 'username,like,twID,'

        request = userName + ',like,' + str(tweetId) + ','

        argumentsList = request.split(',')

        finalResponse = self.doOperation('objRef','like',argumentsList)
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        
        if (mensagem.objectReference == "Tweet inexistente"):
            print("\n Tweet inexistente")
        else:
            likedTweet: 'Tweet' = Tweet.from_json(mensagem.objectReference)
            print("\nTweet curtido: \n" + str(likedTweet))

    def unfollow (self, userName: str, otherUser: str) -> None:
        # request = 'username,unfollow,otherUser,'
        request = userName + ',unfollow,' + otherUser + ','
        argumentsList = request.split(',')

        finalResponse = self.doOperation('objRef','unfollow',argumentsList)
        
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        
        print("\n" + mensagem.objectReference)

    
    def rt (self, username: str, tweetId: int, rtMsg: str) -> None:
        # request = 'username,rt,twID,msg'
        request = username + ',rt,' + str(tweetId) + ',' + rtMsg
        argumentsList = request.split(',')

        finalResponse = self.doOperation('objRef','rt',argumentsList)
        
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
                
        if (mensagem.objectReference == "Tweet inexistente"):
            print("\n Tweet inexistente")
        else:
            reTweet: 'Tweet' = Tweet.from_json(mensagem.objectReference)
            print("\n Retweet postado:\n" + str(reTweet))

    def rm (self, userName: str) -> None:
        # request = 'username,rm,,'
        request = userName + ',rm,,'
        argumentsList = request.split(',')

        finalResponse = self.doOperation('objRef','rm',argumentsList)
        
        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        
        print("\n" + mensagem.objectReference)
        print("Encerrando...")
        self.close()
        
    
    def end(self, username: str):
        # request ='username,end,,'
        request = username + ',end,,'
        argumentsList = request.split(',')

        finalResponse = self.doOperation('objRef', 'end', argumentsList)

        mensagem = Mensagem.from_json(json.dumps(finalResponse))
        

        print('\n' + mensagem.objectReference)
        self.close()

    def close(self):
        self.__client.closeConection()