from http.server import BaseHTTPRequestHandler, HTTPServer
from server.classification_wrapper import run_request
from filelock import FileLock

PORT_NUMBER = 8585

# This class will handles any incoming request from
# the browser


class apiCall(BaseHTTPRequestHandler):

    def _get_action_(self):
        last_history = self.path.split('/')[-1]
        pload = last_history.split("?")
        if(len(pload) > 1):
            return (pload[0], pload[1])
        return (None, None)

    # Handler for the GET requests

    def do_GET(self):

        # Send the html message
        action, params = self._get_action_()
        params = str(params).replace("%20", " ")
        if(action == "request"):
            answer = str(run_request(params))
            self.send_response(200)
        elif(action == 'ping'):
            answer = "ok"
            self.send_response(200)
        else:
            self.send_response(400)
            answer = "Action '" + str(action) + "' is not valid"

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(answer, "utf-8"))
        return


try:

    lock = FileLock("server.lock")
    with lock:
        # Create a web server and define the handler to manage the
        # incoming request
        server = HTTPServer(('', PORT_NUMBER), apiCall)
        server.timeout = 10
        server.handle_timeout = lambda: (_ for _ in ()).throw(TimeoutError())
        print('Started httpserver on port ', PORT_NUMBER)

        # Wait forever for incoming http requests
        while True:
            server.handle_request()

except KeyboardInterrupt:
    print('^C received')
except TimeoutError:
    print("Timeout occured")
except:
    print("other error occured")
finally:
    print('Shutting down server and releasing lock file')
    server.socket.close()
    lock.release()
