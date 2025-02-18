@dataclass
class ProxyData:
    address: string
    port: int
    login: string
    password: string
    protocol = "https"

    def __init__(self, address, port, login = None, password = None, protocol = "https"):
        self.address = address
        self.port = port
        self.login = login
        self.password = password
        self.protocol = protocol

    def proxyUrl(self):
        credentials = ""
        if (self.login and self.password):
            credentials+= self.login+":"+self.password+"@"
        elif (self.login):
            credentials+= self.login+"@"

        return f"{self.protocol}://{credentials}{self.address}:{self.port}"
