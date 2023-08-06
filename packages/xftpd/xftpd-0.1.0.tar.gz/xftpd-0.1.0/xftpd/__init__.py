import os,\
        sys,\
        time,\
        socket,\
        random,\
        paramiko,\
        netifaces,\
        threading,\
        traceback,\
        socketserver,\
        multiprocessing
from sftpserver.stub_sftp import StubSFTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from paramiko import ServerInterface,\
                        AUTH_FAILED,\
                        AUTH_SUCCESSFUL,\
                        OPEN_SUCCEEDED



########################
# Random Password Generator
# Returns 14 character string
#
def _random_string(num=14):
    Random_Str = ''
    char = 'abcdefghijklmnopqrstuvwxyz'
    CHAR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    NUM = '1234567890'
    while len(Random_Str) < num:
        Random_Str += random.choice(char)
        Random_Str += random.choice(NUM)
        Random_Str += random.choice(CHAR)
    return Random_Str


########################
# Random RSA Key Generator
# Returns dictionary with
# private and public filenames
#
def _random_rsa():
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    priv = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    PRIV = ''.join(i for i in [chr(random.randint(97,122)) for i in range(6)])
    f = open(PRIV, "wb")
    f.write(priv)
    f.close()
    pub = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    PUB = ''.join(i for i in [chr(random.randint(97,122)) for i in range(6)])
    f = open(PUB, "wb")
    f.write(pub)
    f.close()
    return {'priv':PRIV,'pub':PUB}


########################
# Get Local IP
# Returns IP Address as String
#
#
def _get_local_ip():
    try:
        TEST = socket.socket()
        TEST.connect(('8.8.8.8', 53))
        Addr = TEST.getsockname()[0]
        TEST.close()
        return Addr
    except:
        print(traceback.format_exc())

########################
# Get Local INT
# Returns interface name as String
#
#
def _get_local_int():
    INTS = {}
    for Int in netifaces.interfaces():
      try:
        netifaces.ifaddresses(Int)[netifaces.AF_INET]
        INTS.update({f'{Int}': netifaces.ifaddresses(Int)[netifaces.AF_INET][0]['addr']})
      except:
        None
    Addr = _get_local_ip()
    for Int,addr in INTS.items():
        if addr == Addr:
            return Int




########################
# FTP Server Class
# Dir = str()
#   Ex: '/tmp'
#   Default: CWD
# Port = int()
#   Ex: 2121
#   Default: 2121
#
class ftp_server(object):
    # Create Random Username and Password
    def __init__(self,Dir=os.getcwd(),Port=2121):
        self.Dir = Dir
        self.Port = Port
        # Get Local Server Address
        self.Addr = _get_local_ip()

    def _run_server(self):
        # Create Dummy Authorizer, with the random user/pass
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user(self.User, self.Pass, self.Dir, perm='elradfmw')
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        # Instantiate the FTP Server
        self.SRV = ThreadedFTPServer(('0.0.0.0',self.Port), self.handler)
        self.SRV.serve_forever()

    def start(self):
        # Random user/pass
        self.User = _random_string()
        self.Pass = _random_string()
        # Start separate process calling Run Server function
        self.srv = multiprocessing.Process(target=self._run_server)
        self.srv.start()

    def stop(self):
        # Close all connections immediately
        self.srv.kill()


########################
# SFTP Server Class
# Dir = str()
#   Ex: '/tmp'
#   Default: CWD
# Port = int()
#   Ex: 22
#   Default: 22
# level = str()
#   Paramiko Debug Level
#   Ex: 'DEBUG'
#   Default: 'INFO'
#
class sftp_server(object):
    def __init__(self,Dir=os.getcwd(),Port=22,level='INFO'):
        self.Dir = Dir
        self.Port = Port
        self.level = level
        # Get Local Server Address
        self.Addr = _get_local_ip()

    class _stub_server(ServerInterface):
        # SubClass of Paramiko ServerInterface
        # Allowing authentication only for random user/pass
        def __init__(self,User,Pass):
            self.User = User
            self.Pass = Pass

        def check_auth_password(self, username, password):
            # Only randomly generated user/pass is allowed
            if (username == self.User) and (password == self.Pass):
                return AUTH_SUCCESSFUL
            else:
                return AUTH_FAILED

        def check_channel_request(self, kind, chanid):
            return OPEN_SUCCEEDED

        def get_allowed_auths(self, username):
            # List availble auth mechanisms
            return 'password'

    class _conn_handler_thd(threading.Thread):
        # Custom Connection Handler Thread for running server
        def __init__(self, conn, SRV, User, Pass, Dir, keyfile):
            threading.Thread.__init__(self)
            self.User = User
            self.Pass = Pass
            self.Dir = Dir
            self.SRV = SRV
            self._conn = conn
            self._keyfile = keyfile

        def run(self):
            self._host_key = paramiko.RSAKey.from_private_key_file(self._keyfile)
            self.transport = paramiko.Transport(self._conn)
            self.transport.add_server_key(self._host_key)

            self.STUB = StubSFTPServer
            self.STUB.ROOT = self.Dir

            self.transport.set_subsystem_handler(
                'sftp', paramiko.SFTPServer, StubSFTPServer)

            self.transport.start_server(server=self.SRV)
            self.channel = self.transport.accept()
            while self.transport.is_active():
                time.sleep(1)

    def _run_server(self):
        # Run Server function that calls Custom Connection Handler Thread
        paramiko_level = getattr(paramiko.common, self.level)
        paramiko.common.logging.basicConfig(level=paramiko_level)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.server_socket.bind(('0.0.0.0', self.Port))
        self.server_socket.listen(10)
        self.SRV = self._stub_server(self.User,self.Pass)
        while True:
            self._conn, self.addr = self.server_socket.accept()
            self.srv = self._conn_handler_thd(self._conn, self.SRV, self.User, self.Pass, self.Dir, self._keyfile)
            self.srv.deamon = True
            self.srv.start()

    def start(self):
        # Random user/pass
        self.User = _random_string()
        self.Pass = _random_string()
        # Random RSA key pair
        self._keys = _random_rsa()
        self._keyfile = self._keys['priv']

        # Start separate process calling Run Server function
        self.srvA = multiprocessing.Process(target=self._run_server)
        self.srvA.start()

    def stop(self):
        # Close server socket immediately
        # This will print a Threading Exception to STDOUT, but will not throw a true exception
        self.srvA.kill()
        os.remove(self._keys['priv'])
        os.remove(self._keys['pub'])






