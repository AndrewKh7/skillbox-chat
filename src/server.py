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


            self.factory.history.append(content)

            for user in self.factory.clients:
                user.sendLine(content.encode())
        else:
            # login:admin -> admin
            if content.startswith("login:"):
                login = content.replace("login:", "")

                for user in self.factory.clients:
                    if user.login == login:
                        self.sendLine("Login already exists! Try another one".encode())
                        return

                self.login = login
                self.factory.clients.append(self)
                self.factory.send_history(self)
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

    history: list
    def startFactory(self):
        self.clients = []
        self.history = []
        print("Server started")

    def stopFactory(self):
        print("Server closed")

    def send_history(self, client: ServerProtocol):
        client.sendLine("Welcome!".encode())

        last_messages = self.history[-10:]

        for msg in last_messages:
            client.sendLine(msg.encode())


reactor.listenTCP(1234, Server())
reactor.run()
