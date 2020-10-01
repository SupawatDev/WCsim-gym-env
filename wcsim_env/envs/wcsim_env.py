import gym
import socket
from gym import error, spaces, utils
from gym.utils import seeding


class WCsimEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, server_ip='127.0.0.1', server_port=8877):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = 30
        # initialize socket
        self.env_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _step(self, action):
        ...

    def _reset(self):
        ...

    def _render(self, mode='human', close=False):
        ...

    def connect(self):
        self.env_sock.connect((self.server_ip, self.server_port))
        print("Connected to " + self.server_ip + ":" + str(self.server_port))
        self.env_sock.send("Client: Hello Server".encode())
        print(self.env_sock.recv(1024).decode())
        return None

    def disconnect(self):
        self.env_sock.close()

    def command_transmitter(self, command, transmitter_location, transmitter_rotation):
        # Add transmitter and return the transmitter id
        command = 'tx_add:' + str(transmitter_location) + str(transmitter_rotation)
        tx_id = self.env_sock.recv(1024).decode()
        self.env_sock.send(command.encode())
        return None
