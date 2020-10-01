import socket
from time import sleep


class WCsimEnvCore:

    def __init__(self, server_ip='127.0.0.1', server_port=8877):
        self.server_ip = server_ip
        self.server_port = server_port
        # initialize socket
        self.env_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Trying to connect to the simulator
        while not self.connect():
            print("Retrying to connect to server: " + self.server_ip + ":" + str(self.server_port));
            sleep(3)
        # Connection is success
        print("Connected to Server successfully.")
        self.reset()        # ensure that the environment is reset.
        self.stations = []  # index of stations in the environment.
        self.users = []     # index of users in the environment.

    def connect(self):
        try:
            self.env_sock.connect((self.server_ip, self.server_port))
            self.env_sock.send("Client: Hello Server".encode())
            print(self.env_sock.recv(1024).decode())
            return True
        except ConnectionRefusedError:
            print("Unable to connect to the server.")
        return False

    def reset(self):
        self.env_sock.send("r".encode())
        res = self.env_sock.recv(1024).decode()
        assert res[0:3] == "rok"

    def disconnect(self):
        self.env_sock.send("e".encode())
        res = self.env_sock.recv(1024).decode()
        assert res[0:3] == "eok"
        self.env_sock.close()

    def ask_station_number(self):
        return self.ask(1)

    def ask_user_number(self):
        return self.ask(2)

    def ask_station_location(self, station_number):
        return self.ask(3, index=station_number)

    def ask_users_of_station(self, station_number):
        return self.ask(4, index=station_number)

    def ask_avg_receivers_at_station(self, station_number):
        return self.ask(5, index=station_number)

    def ask(self, question, index=None):
        # Questions:
        # 1: How many stations are?
        # 2: How many users are?
        # 3: What is location of base station number N
        # 4: Who are users of base station number N
        # 5: Average Receivers quality of base station number N
        message = 'q'
        if index is None:
            message += str(question)
        else:
            message += str(question) + ',' + str(index)
        self.env_sock.send(question + str(index));
        # Confirms that server understand the question
        if self.env_sock.recv(1024).decode() == 'qok':
            print("Server understands the question.")
        # Get the answer
        answer = self.env_sock.recv(1024).decode()
        if answer[0] == 'a':
            answer = answer[1:-1]
        else:
            print("This should not be an answer.")
        return

    def command_add_tx2env(self, location):
        return self.command(1, location)

    def command(self, command, location):
        # Commands:
        # 1: Add a station to the env
        # 2: Add a user to the env
        # 3: Add a user to station
        # 4: Move station
        # Add transmitter and return the transmitter id
        # tx_id = self.env_sock.recv(1024).decode()
        message = 'c' + str(command) + str(location)
        self.env_sock.send(message.encode())
        if self.env_sock.recv(1024).decode() == 'cok':
            print("Server understands the command.")
        return


env = WCsimEnvCore(server_ip='127.0.0.1', server_port=8877)

env.reset()

env.disconnect()
