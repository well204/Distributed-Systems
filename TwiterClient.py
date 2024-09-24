import os
from pythonClient import TwiterProxy

def clearTerminal () -> None:
	os.system('cls' if os.name == 'nt' else 'clear')

def enterToContinue() -> None:
	input('\nPressione enter para continuar')

def menu(username: str) -> None:
	print("================= Twiter =================");
	print("================= "+ username +" =================\n")
	print("show:     mostrar todos os usuários");
	print("follow:   seguir um usuário");
	print("tweetar:  fazer um tweet");
	print("timeline: mostrar timeline");
	print("like:     curtir um tweet");
	print("unfollow: deixar de seguir um usuário");
	print("rt:       retweetar algo");
	print("rm:       remover conta");
	print("end:      encerrar programa");

def main():
	proxy: 'TwiterProxy' = TwiterProxy()
	option: str = None
	mainUserName = ''
	newUserExists: bool = False
	# opcoes = ['y','n','s','sim','nao', 'não', 'no']
	# opcoesYes = ['y','s','sim']

	# while(isNewUser not in opcoes):
	# 	isNewUser = input('novo usuário?(y/n): ').lower

	# if(isNewUser in opcoesYes ):		
	# 	mainUserName = input("Seu nome de usuário: ")
	# 	proxy.login(mainUserName)
	# else:
	while(newUserExists != True):
		mainUserName = input("Seu nome de usuário: ")
		print('novo user: ' + mainUserName)
		newUserExists = proxy.add(mainUserName)
		enterToContinue()
		clearTerminal()

	while(True):
		menu(mainUserName)
		option = input('Escolha uma opção: ').lower()
		clearTerminal()

		if option == 'show':
			proxy.show(mainUserName)
			enterToContinue()
			clearTerminal()
			continue
		elif option == 'follow':
			otherUser = input('Digite o nome de quem quer serguir: ')
			proxy.follow(mainUserName, otherUser)
			enterToContinue()
			clearTerminal()
			continue
		elif option == 'tweetar':
			tweetMsg = input("Digite a mensagem do tweet: \n")
			proxy.tweetar(mainUserName, tweetMsg)
			enterToContinue()
			clearTerminal()
			continue
		elif option == 'timeline':
			proxy.timeline(mainUserName)
			enterToContinue()
			clearTerminal()
			continue
		elif option == 'like':
			tweetId = int(input('id do tweet que deseja curtir: '))
			proxy.like(mainUserName, tweetId)
			enterToContinue()
			clearTerminal()
			continue
		elif option == 'unfollow':
			otherUser = input('Usuário que quer parar de seguir: ')
			proxy.unfollow(mainUserName, otherUser)
			enterToContinue()
			clearTerminal()
			continue
		elif option == 'rt':
			tweetId = int(input("id do twwet: "))
			rtMsg = input("mensagem do retweet: ")
			proxy.rt(mainUserName, tweetId, rtMsg)
			enterToContinue()
			clearTerminal()
			continue
		elif option == 'rm':
			proxy.rm(mainUserName)
			enterToContinue()
			clearTerminal()
			return
		elif option == 'end':
			proxy.end(mainUserName)
			print("\nSaindo...")
			return
		else:
			print("Entrada inválida")
			enterToContinue()
			clearTerminal()
			continue

if __name__ == '__main__':
	main()