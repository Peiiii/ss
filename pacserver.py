import http.server
import socketserver


def run_pacserver():
    PORT = 9998
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        # import signal
        # def stop(signal, frame):
        #     print('server stopping...')
        #     # httpd.shutdown()
        #     exit(0)
        #
        # signal.signal(signal.SIGINT, stop)
        httpd.serve_forever()
if __name__=='__main__':
    run_pacserver()