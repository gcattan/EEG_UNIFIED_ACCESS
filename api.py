from http.server import BaseHTTPRequestHandler, HTTPServer
from classification_wrapper import run_request
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
        print('Started httpserver on port ', PORT_NUMBER)

        # Wait forever for incoming htto requests
        server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
