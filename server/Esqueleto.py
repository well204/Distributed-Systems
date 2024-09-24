from typing import List
from twiterClasses import *

class Esqueleto:
    def __init__(self):
        self.__sistema: 'Twiter' = Twiter()        
        
    def add(self, msg):
        if (self.__sistema.addUser2(msg)):
            return self.__sistema.getUserByUsername(msg.getUsername()).userToJson()
        else:
            return "Usuário já existe"

    def login(self, msg):
        pass

    def show(self, msg):
        return str(self.__sistema) 

    def follow(self, msg):
        return self.__sistema.follow(msg[0],msg[2])

    def tweetar(self, msg):
        return self.__sistema.sendTweetRemote(msg)         

    def timeline(self, msg):
        return self.__sistema.sendTimline(msg) 

    def like(self, msg):
        return self.__sistema.likeRemote(msg[0], int(msg[2]))             

    def unfollow(self, msg):
        return self.__sistema.unfollow(msg[0],msg[2])
    
    def rt(self, msg):
        return self.__sistema.sendRt(msg[0],int(msg[2]),msg[3])
             
    def rm(self, msg):
        username = self.__sistema.getUserByUsername(msg[0]).getUsername()
        self.__sistema.removeUser(msg[0])
        return "Usuário: " + username + " removido com sucesso"
    
    def end(self, msg):        
        return "Logout de @" + msg[0] + " feito com sucesso"