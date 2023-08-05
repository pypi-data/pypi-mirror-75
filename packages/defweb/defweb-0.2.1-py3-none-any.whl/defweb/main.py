import argparse
import logging
import os
import ssl
import sys
from http.server import HTTPServer
from subprocess import CompletedProcess, PIPE, run

from defweb.proxy import DefWebProxy
from defweb.version import get_version_from_file
from defweb.webserver import DefWebServer

__version__ = get_version_from_file()

logger = logging.getLogger(__name__)

env = os.environ

cert_root = os.path.join(env['HOME'], '.defweb')

cert_path = os.path.join(cert_root, 'server.pem')
key_path = os.path.join(cert_root, 'server_key.pem')


def create_cert():

    # check if .defweb folder exists
    if not os.path.exists(cert_root):
        os.makedirs(cert_root)

    try:
        result = run(['/usr/bin/openssl', 'req', '-new', '-x509', '-keyout', key_path,
                      '-out', cert_path, '-days', '365', '-nodes',
                      '-subj', '/C=NL/ST=DefWeb/L=DefWeb/O=DefWeb/OU=DefWeb/CN=DefWeb.nl', '-passout',
                      'pass:DefWeb'], shell=False, stdout=PIPE, stderr=PIPE, cwd=cert_root)
    except FileNotFoundError as err:
        result = '{}'.format(err)

    if isinstance(result, CompletedProcess):
        if result.returncode == 0:
            result = 0
        elif result.returncode == 1:
            error = result.stderr.decode('utf-8').split('\n')[-3]
            result = 'Error generating ssl certificate; {}'.format(error)

    return result


def main():

    proto = DefWebServer.protocols.HTTP

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', dest='bind', help='ip to bind to; defaults to 127.0.0.1')
    parser.add_argument('-d', dest='directory', metavar='[ DIR ]', default=None,
                        help='path to use as document root')
    parser.add_argument('-i', dest='impersonate', metavar='[ SERVER NAME ]', default=None,
                        help='server name to send in headers')
    parser.add_argument('-p', dest='port', type=int, help='port to use; defaults to 8000')
    parser.add_argument('--proxy', action='store_true', help='start proxy for SOCKS4, SOCKS5 & HTTP')
    parser.add_argument('--key', dest='key', metavar='[ KEY ]', help='key file to use for webserver')
    parser.add_argument('--cert', dest='cert', metavar='[ CERT ]', help='certificate file to use for webserver')
    parser.add_argument('-r', '--recreate_cert', action='store_true', help='re-create the ssl certificate')
    parser.add_argument('-s', '--secure', action='store_true', help='use https instead of http')
    parser.add_argument('-u', dest='credentials', metavar='[ USER:PASSWORD ]',
                        help='user credentials to use when authenticating to the proxy server')
    parser.add_argument('-v', '--version', action='store_true', help='show version and then exit')

    parser.add_argument('--log-level', default='INFO', help='DEBUG, INFO (default), WARNING, ERROR, CRITICAL')

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level),
                        format="[%(asctime)s] %(levelname)-8s -> %(message)-50s -> (%(filename)s:%(lineno)s)")

    logger.info('[+] Defweb version: {}'.format(__version__))

    if args.version:
        print(__version__)
        exit(0)

    if args.port:
        if args.port <= 1024:
            if os.geteuid() != 0:
                logger.info('[+] Need to be root to bind to privileged port; increasing port number with 8000')
                port = args.port + 8000
            else:
                port = args.port
        else:
            port = args.port
    else:
        if os.geteuid() == 0 and args.secure:
            port = 443
        else:
            port = 8000

    if args.bind:
        host = args.bind
    else:
        host = '127.0.0.1'

    if not args.proxy:
        # setup webserver
        WebHandler = DefWebServer

        if args.directory:
            if os.path.exists(args.directory):
                os.chdir(args.directory)
                WebHandler.root_dir = os.getcwd()
            else:
                raise FileNotFoundError('Path: {} cannot be found!!!'.format(args.directory))
        else:
            WebHandler.root_dir = os.getcwd()

        if args.impersonate:
            WebHandler.server_version = args.impersonate

        try:
            httpd = HTTPServer((host, port), WebHandler)
        except OSError:
            logger.error('\n[-] Error trying to bind to port {}, is there another service '
                         'running on that port?\n'.format(port), exc_info=True)
            return

        if args.secure:

            if args.cert:
                if os.path.exists(args.cert):
                    global cert_path
                    cert_path = args.cert
                else:
                    raise FileNotFoundError('Certificate file not found!')

            if args.key:
                if os.path.exists(args.key):
                    global key_path
                    key_path = args.key
                else:
                    raise FileNotFoundError('Certificate file not found!')

            result = 0

            if not args.cert:
                if not os.path.exists(cert_path) or args.recreate_cert:
                    result = create_cert()

            if result == 0:
                proto = DefWebServer.protocols.HTTPS
                httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=key_path, certfile=cert_path, server_side=True)
            else:
                logger.error('[-] Certificate creation produced an error: {}'.format(result))
                logger.error('[-] Cannot create certificate... skipping https...')

        try:
            logger.info('[+] Running DefWebServer: {}'.format(WebHandler.server_version))
            logger.info('[+] Starting webserver on: {}{}:{}'.format(proto, host, port))
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info('[+] User cancelled execution, closing down server...')
            httpd.server_close()
            logger.info('Server closed, exiting!')
            sys.exit(0)
    else:
        # setup proxy

        logger.info('[+] Running DefWebProxy: {}'.format(DefWebProxy.server_version))

        if args.credentials:
            username, password = args.credentials.split(':')
            proxy_server = DefWebProxy(socketaddress=(host, port), username=username, password=password,
                                       enforce_auth=True).init_proxy()
        else:
            proxy_server = DefWebProxy(socketaddress=(host, port)).init_proxy()

        if proxy_server is not None:
            try:
                ip, host = proxy_server.server_address
                logger.info('[+] Starting WebDefProxy on {}:{}'.format(ip, host))
                proxy_server.serve_forever()
            # handle CTRL+C
            except KeyboardInterrupt:
                logger.info("[+] Exiting...")
            except Exception as err:
                logger.error("[!] Exception occured", exc_info=True)
            finally:
                proxy_server.shutdown()
                proxy_server.server_close()
                sys.exit(0)


if __name__ == '__main__':
    main()
