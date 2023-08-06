# -*- coding: utf-8 -*-
'''
'''

import asyncio
import json
import os
import random

import tornado
import turbo_tunnel


class RandomTunnelMixin(object):
    def __init__(self):
        self._random_tunnel_urls = {}
        asyncio.ensure_future(self.fetch_tunnel_list_task())

    async def fetch_tunnel_list_task(self):
        provider = self._listen_url.params.get('provider')
        while True:
            tunnel_list = await self.retrieve_tunnel_list(provider, 100)
            for url in tunnel_list:
                if url not in self._random_tunnel_urls:
                    self._random_tunnel_urls[url] = 0
            await asyncio.sleep(300)

    def update_tunnel_result(self, tunnel_url, result):
        assert (tunnel_url in self._random_tunnel_urls)
        if result:
            self._random_tunnel_urls[tunnel_url] += 1
        else:
            self._random_tunnel_urls[tunnel_url] -= 1

    async def retrieve_tunnel_list(self, url, count):
        if url.startswith('http://') or url.startswith('https://'):
            if '?' in url:
                url += '&limit=%d' % count
            else:
                url += '?limit=%d' % count
            request = tornado.httpclient.HTTPRequest(
                url, 'GET', headers={'Content-Type': 'application/json'})
            turbo_tunnel.utils.logger.debug(
                '[%s] Retrieve tunnels from url %s' %
                (self.__class__.__name__, url))
            client = tornado.httpclient.AsyncHTTPClient()
            response = await client.fetch(request)
            result = json.loads(response.body)
            return ['%s://%s:%d' % (it['type'], it['ip'], it['port']) for it in result['results']]
        elif url.startswith('file://'):
            tunnel_list = []
            file_path = url[7:]
            if not os.path.exists(file_path):
                turbo_tunnel.utils.logger.warn('[%s] File %s not exist' % (self.__class__.__name__, file_path))
                return tunnel_list
            with open(file_path) as fp:
                for line in fp.read().splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    tunnel_list.append(line)
            return tunnel_list
        else:
            raise NotImplementedError(url)

    async def select_tunnels(self, count=1, exclude=None):
        exclude = exclude or []
        while len(self._random_tunnel_urls.keys()) < count:
            await asyncio.sleep(0.005)
        tunnels = list(self._random_tunnel_urls.keys())
        for it in exclude:
            tunnels.remove(it)
        tunnels.sort(key=lambda it: self._random_tunnel_urls[it], reverse=True)
        tunnels = tunnels[:count * 2]
        return random.sample(tunnels, k=count)

    def create_dynamic_tunnel_chain(self, tunnel_url):
        tunnel_urls = self._tunnel_urls[:]
        if len(tunnel_urls) == 1 and tunnel_urls[0] == 'tcp://':
            tunnel_urls = []
        tunnel_urls.append(turbo_tunnel.utils.Url(tunnel_url))
        return turbo_tunnel.chain.TunnelChain(tunnel_urls,
                                              self.retry_count + 1)


class CreateTunnelTask(object):
    def __init__(self, tunnel_urls, tunnel_url, address):
        self._tunnel_urls = tunnel_urls[:]
        if len(self._tunnel_urls) == 1 and self._tunnel_urls[0] == 'tcp://':
            self._tunnel_urls = []
        self._tunnel_urls.append(turbo_tunnel.utils.Url(tunnel_url))
        self._tunnel_url = tunnel_url
        self._address = address
        self._done = False
        self._result = None
        self._task = asyncio.ensure_future(self.run())

    @property
    def tunnel_url(self):
        return self._tunnel_url

    def result(self):
        return self._result

    def done(self):
        return self._done

    def cancel(self):
        if not self._done:
            self._task.cancel()
            self._task = None

    async def run(self):
        tunnel_chain = turbo_tunnel.chain.TunnelChain(self._tunnel_urls)
        try:
            await tunnel_chain.create_tunnel(self._address)
        except turbo_tunnel.utils.TunnelError:
            tunnel_chain.close()
            return None
        except asyncio.CancelledError:
            turbo_tunnel.utils.logger.debug(
                '[%s] Task create tunnel to %s cancelled' %
                (self.__class__.__name__, self._tunnel_urls[-1]))
        except:
            turbo_tunnel.utils.logger.exception(
                '[%s] Task create tunnel to %s crashed' %
                (self.__class__.__name__, self._tunnel_urls[-1]))
        else:
            self._result = tunnel_chain
        self._done = True
        self._task = None
