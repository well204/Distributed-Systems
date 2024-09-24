from typing import List
import json
class Mensagem:
    def __init__(self, messageType: int, requestId: int, objectReference: str, methodId: str, arguments: List[str]):
        self.messageType = messageType
        self.requestId = requestId
        self.objectReference = objectReference
        self.methodId = methodId
        self.arguments = arguments
        
    def packMessage(self):
        packedMessage = {
            'messageType' : self.messageType,
            'requestId' : self.requestId,
            'objectReference' : self.objectReference,
            'methodId' : self.methodId,
            'arguments' : self.arguments
        }
        return packedMessage
        
    def unpackMessage(self, msgDict):
        msg = Mensagem(
            messageType = msgDict['messageType'],
            requestId = msgDict['requestId'],
            objectReference = msgDict['objectReference'],
            methodId = msgDict['methodId'],
            arguments = msgDict['arguments'],
        )
        return msg
    
    def to_json(self) -> str:
        packedMessage = self.packMessage()
        return json.dumps(packedMessage)

    @staticmethod
    def from_json(json_str: str) -> 'Mensagem':
        msgDict = json.loads(json_str)
        return Mensagem(
            messageType=msgDict['messageType'],
            requestId=msgDict['requestId'],
            objectReference=msgDict['objectReference'],
            methodId=msgDict['methodId'],
            arguments=msgDict['arguments']
        )
        
    