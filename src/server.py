#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Сервер для обработки сообщений от клиентов
#
#  Ctrl + Alt + L - форматирование кода
#
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone, Protocol
from twisted.protocols.basic import LineOnlyReceiver


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None

    def connectionMade(self):
        # Потенциальный баг для внимательных =)
        self.sendLine("Hi! Please login!".encode())

    def connectionLost(self, reason=connectionDone):
        if self.login is not None:
            print(f"{self.login} disconnected")
        if self.login is not None:
            self.factory.clients.remove(self)

    def lineReceived(self, line: bytes):
        try:
            content = line.decode()
        except Exception as e:
            print(e) # Просто чтоб сервер не падал в случае неудачной декодировки символов
            return

        if self.login is not None:
            content = f"Message from {self.login}: {content}"
            self.__saveHistory(content)
            for user in self.factory.clients:
                if user is not self:
                    user.sendLine(content.encode())
                    print(f"Send to {user.login}")

        else:
            # login:admin -> admin
            if content not in [user.login for user in self.factory.clients]:
                self.login = content
                self.sendLine("Welcome!".encode())
                self.factory.clients.append(self) # перенес сюда, чтобы пользователь не добавлялся в случае неудачной авторизации
                self.sendHistory()
                print(f"{self.login} joined")
            else:
                self.sendLine(f"Login {content} is already exists!\nDisconnected!".encode())
                self.transport.loseConnection() # закрытие соединения после неудачного ввода имени пользователя

    def __saveHistory(self,msg):
        self.factory.hysory = self.factory.hysory[1::1]
        self.factory.hysory.append(msg.encode())

    def sendHistory(self):
        for msg in self.factory.hysory:
            if msg is not None:
                self.sendLine(msg)


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list
    hysory: list = [None]*10

    def startFactory(self):
        self.clients = []
        print("Server started")

    def stopFactory(self):
        print("Server closed")


reactor.listenTCP(1234, Server())
reactor.run()
