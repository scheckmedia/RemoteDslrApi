from RemoteDslrApi import Camera
from RemoteDslrApi.server import Server

if __name__ == "__main__":
    app = Server(__name__)
    app.start()