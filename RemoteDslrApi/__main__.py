from RemoteDslrApi.server import Server
import atexit


def exit_handler():
    app.stop()

if __name__ == "__main__":
    app = Server(__name__)
    app.start()
    atexit.register(exit_handler)
