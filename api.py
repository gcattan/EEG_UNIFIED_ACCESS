from http.server import BaseHTTPRequestHandler, HTTPServer
from main import run_request

PORT_NUMBER = 8585

# This class will handles any incoming request from
# the browser


class apiCall(BaseHTTPRequestHandler):

    def _get_action_(self):
        parameters = self.path.split('action=')
        if(len(parameters) > 1):
            action_attr = parameters[1].split("?")
            if(len(action_attr) > 1):
                return (action_attr[0], action_attr[1])
            return (action_attr[0], None)
        return (None, None)

    # Handler for the GET requests

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        action, params = self._get_action_()
        params = str(params).replace("%20", " ")
        if(action == "request"):
            answer = str(run_request(params))
        else:
            answer = "action not known"
        self.wfile.write(bytes(answer, "utf-8"))
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), apiCall)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()


# request = "@cache get-scores-in bi2012, bi2013 using subject=[1], tmax=[0.7] for bi2012, tmax=[0.9] for bi2013"
# run_request(request)
