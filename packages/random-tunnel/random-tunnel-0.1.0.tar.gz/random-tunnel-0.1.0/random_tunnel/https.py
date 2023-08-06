# -*- coding: utf-8 -*-

import asyncio
import time

import tornado
import turbo_tunnel

from .utils import CreateTunnelTask, RandomTunnelMixin


class RandomHTTPSTunnelServer(turbo_tunnel.https.HTTPSTunnelServer,
                              RandomTunnelMixin):
    '''Random HTTPS Tunnel Server
    '''
    def post_init(self):
        RandomTunnelMixin.__init__(self)
        this = self
        this._current_tunnel_urls = []

        class HTTPServerHandler(tornado.web.RequestHandler):
            '''HTTP Server Handler
            '''
            SUPPORTED_METHODS = ['CONNECT']

            async def create_tunnel(self, tunnel_url, address):
                tunnel_chain = this.create_dynamic_tunnel_chain(tunnel_url)
                try:
                    await tunnel_chain.create_tunnel(address)
                except turbo_tunnel.utils.TunnelError:
                    tunnel_chain.close()
                    return None
                return tunnel_chain

            async def connect(self):
                address = self.request.path.split(':')
                address[1] = int(address[1])
                address = tuple(address)
                downstream = turbo_tunnel.tunnel.TCPTunnel(
                    self.request.connection.detach(), server_side=True)
                auth_data = this._listen_url.auth
                if auth_data:
                    auth_data = auth_data.split(':')
                    for header in self.request.headers:
                        if header == 'Proxy-Authorization':
                            value = self.request.headers[header]
                            auth_type, auth_value = value.split()
                            if auth_type == 'Basic' and auth_value == auth.http_basic_auth(
                                    *auth_data):
                                break
                    else:
                        utils.logger.info(
                            '[%s] Connection to %s:%d refused due to wrong auth'
                            %
                            (self.__class__.__name__, address[0], address[1]))
                        await downstream.write(
                            b'HTTP/1.1 403 Forbidden\r\n\r\n')
                        self._finished = True
                        return
                tunnel_chain = None
                random_tunnel_count = 10
                timeout = 10
                with turbo_tunnel.server.TunnelConnection(
                        self.request.connection.context.address,
                        address) as tun_conn:
                    while not downstream.closed():
                        tunnel_urls = await this.select_tunnels(
                            random_tunnel_count, this._current_tunnel_urls
                        )  # exclude current connected tunnels

                        tasks = []

                        for tunnel_url in tunnel_urls:
                            task = CreateTunnelTask(this._tunnel_urls,
                                                    tunnel_url, address)
                            tasks.append(task)
                            assert(tunnel_url not in this._current_tunnel_urls)
                            this._current_tunnel_urls.append(tunnel_url)

                        current_tunnel_url = None
                        time0 = time.time()
                        while time.time() - time0 < timeout:
                            for i, task in enumerate(tasks):
                                if task.done() and task.result():
                                    current_tunnel_url = task.tunnel_url
                                    tunnel_chain = task.result()
                                    tasks.pop(i)
                                    this.update_tunnel_result(
                                        current_tunnel_url, True)
                                    turbo_tunnel.utils.logger.info(
                                        '[%s] Connect %s:%d through %s success'
                                        % (self.__class__.__name__, address[0],
                                           address[1], current_tunnel_url))
                                    tunnel_url = turbo_tunnel.utils.Url(
                                        current_tunnel_url)
                                    tun_conn.update_tunnel_address(
                                        (tunnel_url.host, tunnel_url.port))
                                    break
                                elif task.done():
                                    # Connect failed
                                    this.update_tunnel_result(
                                        task.tunnel_url, False)
                                    tasks.pop(i)
                                    this._current_tunnel_urls.remove(task.tunnel_url)
                                    break

                            if tunnel_chain:
                                break
                            for i, task in enumerate(tasks):
                                if not task.done():
                                    break
                            else:
                                # All tasks done
                                turbo_tunnel.utils.logger.warn(
                                    '[%s] Connect %d random tunnels failed' %
                                    (self.__class__.__name__,
                                     random_tunnel_count))
                                break
                            await asyncio.sleep(0.005)
                        else:
                            turbo_tunnel.utils.logger.warn(
                                '[%s] Connect %d random tunnels timeout' %
                                (self.__class__.__name__, random_tunnel_count))

                        for task in tasks:
                            task.cancel()
                            if not tunnel_chain:
                                this.update_tunnel_result(
                                    task.tunnel_url, False)
                            this._current_tunnel_urls.remove(task.tunnel_url)

                        if tunnel_chain:
                            break
                    if not tunnel_chain:
                        if not downstream.closed():
                            await downstream.write(
                                b'HTTP/1.1 504 Gateway timeout\r\n\r\n')
                        self._finished = True
                        return

                    with tunnel_chain:
                        if not downstream.closed():
                            await downstream.write(
                                b'HTTP/1.1 200 HTTPSTunnel Established\r\n\r\n'
                            )
                            tasks = [
                                this.forward_data_to_upstream(
                                    tun_conn, downstream, tunnel_chain.tail),
                                this.forward_data_to_downstream(
                                    tun_conn, downstream, tunnel_chain.tail)
                            ]
                            await turbo_tunnel.utils.AsyncTaskManager(
                            ).wait_for_tasks(tasks)
                        else:
                            turbo_tunnel.utils.logger.warn(
                                '[%s] Downstream closed unexpectedly' %
                                self.__class__.__name__)
                            tun_conn.on_downstream_closed()
                        downstream.close()
                        self._finished = True
                        this._current_tunnel_urls.remove(current_tunnel_url)

        handlers = [
            (['CONNECT'], r'', HTTPServerHandler),
        ]
        app = tornado.web.Application()
        router = turbo_tunnel.https.HTTPRouter(app, handlers)
        self._http_server = tornado.httpserver.HTTPServer(router)


turbo_tunnel.registry.server_registry.register('http+random',
                                               RandomHTTPSTunnelServer)
turbo_tunnel.registry.server_registry.register('https+random',
                                               RandomHTTPSTunnelServer)
