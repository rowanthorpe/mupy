# -*- coding: utf-8 -*-
# Copyright 2014 Leonidas Poulopoulos
# Copyright 2014 Costas Drogos
# Copyright 2014 Stavros Kroustouris
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bs4 import BeautifulSoup
import urllib
from datetime import timedelta
from django.utils import timezone

from django.core.management.base import NoArgsCommand
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User

from muparse.models import *
from utils import get_v2_nodes, get_v1_nodes


class Command(NoArgsCommand):

    def parseUrlSoup_v1(self, baseUrl, urlPage):
        serverListPage = urllib.urlopen("%s/%s" % (baseUrl, urlPage))
        htmlText = serverListPage.read()
        serverListPage.close()
        return BeautifulSoup(htmlText)

    def parseUrlSoup_v2(self, baseUrl, urlPage):
        if urlPage:
            serverListPage = urllib.urlopen('%s/%s' % (baseUrl, urlPage))
        else:
            serverListPage = urllib.urlopen('%s' % (baseUrl))
        htmlText = serverListPage.read()
        serverListPage.close()
        return BeautifulSoup(htmlText)

    def delete_garbage(self):
        self.stdout.write('Deleting junk from %s day(s) ago.\n' % settings.DATA_EXPIRES)
        date_N_days_ago = timezone.now() - timedelta(days=int(settings.DATA_EXPIRES))
        NodeGroup.objects.filter(updated__lt=date_N_days_ago).delete()
        GraphCategory.objects.filter(updated__lt=date_N_days_ago).delete()
        Node.objects.filter(updated__lt=date_N_days_ago).delete()
        Graph.objects.filter(updated__lt=date_N_days_ago).delete()
        NodeGraphs.objects.filter(updated__lt=date_N_days_ago).delete()
        # delete cache
        for u in User.objects.all():
            cache.delete('user_%s_tree' % (u.pk))
            cache.delete('user_%s_tree_cat' % (u.pk))
        self.stdout.write('Done...\n')

    def parse_v1(self):
        mnodes = get_v1_nodes()
        for mnode in mnodes:
            mnode_dict = mnode[1]
            baseUrl = mnode_dict['url']
            cgiPath = mnode_dict['cgi_path']
            soup = self.parseUrlSoup(_v1baseUrl, "index.html")
            homePage = soup.find_all('span', attrs={'class': 'domain'})
            for nodeGroup in homePage:
                ng_url = "%s/%s" % (baseUrl, nodeGroup.a.get('href'))
                ng, created = NodeGroup.objects.get_or_create(
                    name="%s@%s" % (
                        nodeGroup.a.text,
                        mnode_dict['name']
                    ),
                    url=ng_url
                )
                self.stdout.write('Added nodeGroup: %s\n' % ng.name.encode('utf8'))
    #            print i.a.text, i.a.get('href')
                for node in nodeGroup.findParent('li').findChildren(
                    'span',
                    attrs={'class': 'host'}
                ):
                    #print node.a.text, node.a.get('href')
                    n_url = "%s/%s" % (baseUrl, node.a.get('href'))
                    n, created = Node.objects.get_or_create(
                        name=node.a.text,
                        url=n_url,
                        group=ng
                    )
                    self.stdout.write('-Added node: %s\n' % n.name.encode('utf8'))
                    nodeSoup = self.parseUrlSoup_v1(baseUrl, node.a.get('href'))
                    metricsTable = nodeSoup.find_all(
                        'td',
                        {'class': 'graphbox'}
                    )
                    for metricGroup in metricsTable:
                        metricCategory = metricGroup.get('id')
                        graphCategories = metricGroup.find_all(
                            'div',
                            {'class': 'lighttext'}
                        )
                        gc, created = GraphCategory.objects.get_or_create(
                            name=metricCategory
                        )
                        self.stdout.write(
                            '-Added Category: %s\n' % gc.name.encode('utf8')
                        )
                        for graphCategory in graphCategories:
                            pageUrl = "%s/%s/%s/%s" % (
                                baseUrl,
                                nodeGroup.a.text,
                                n.name,
                                graphCategory.a.get('href')
                            )
                            self.stdout.write(
                                '-Page URL: %s\n' % pageUrl.encode('utf8')
                            )
                            t = graphCategory.findParent('tr').find_next_sibling('tr')
                            g, created = Graph.objects.get_or_create(
                                name=graphCategory.a.text,
                                slug=t.img.get('src').split('/')[-1:][0].split('-')[0],
                                category=gc
                            )
                            self.stdout.write(
                                '--Added Graph: %s\n' % g.name.encode('utf8')
                            )
                            imageUrl = "%s/%s%s/%s/%s" % (
                                baseUrl,
                                cgiPath,
                                nodeGroup.a.text,
                                n.name,
                                g.slug
                            )
                            nodegraph, created = NodeGraphs.objects.get_or_create(
                                node=n,
                                graph=g,
                                baseurl=imageUrl,
                                pageurl=pageUrl
                            )
                            self.stdout.write('--Added NodeGraph: %s\n' % nodegraph)

    def parse_v2(self):
        MNODES = get_v2_nodes()

        for mnode in MNODES:
            mnode_dict = mnode[1]
            baseUrl = mnode_dict['url']
            soup = self.parseUrlSoup_v2(baseUrl, "index.html")
            homePage = soup.find_all('span', attrs={'class': 'domain'})
            for nodeGroup in homePage:
                ng_url = '%s/%s' % (baseUrl, nodeGroup.a.get('href'))
                ng, created = NodeGroup.objects.get_or_create(name='%s@%s' % (nodeGroup.a.text, mnode_dict['name']), url=ng_url)
                self.stdout.write('NodeCategory: %s\n' % ng.name)
                nodegroupSoup = self.parseUrlSoup_v2(ng_url, "")
                nodes = nodegroupSoup.find('div', attrs={'id': 'content'})\
                                     .find('ul', recursive=False).find_all('li', recursive=False)
                for node in nodes:
                    node_name = node.find('span', attrs={'class': 'domain'}, recursive=False)
                    n_url = '%s/%s/%s' % (baseUrl, nodeGroup.a.text, node_name.a.get('href'))
                    n, created = Node.objects.get_or_create(name=node.a.text, url=n_url, group=ng)
                    self.stdout.write('-Node: %s\n' % (n.name))
                    services_categories = node.find_all('ul', recursive=False)
                    # get inside node
                    for service_category in services_categories:
                        category_group = service_category.find_all('li')
                        # a node has graph categories (class=host) that have services (class=service)
                        last_cat = None
                        for category in category_group:
                            cat = category.find('span', attrs={'class': 'host'})
                            if cat:
                                gc, created = GraphCategory.objects.get_or_create(name=cat.text)
                                self.stdout.write('--GraphCategory: %s\n' % gc.name)
                                last_cat = gc
                            else:
                                slug = category.a.get('href').replace(node_name.text, '').replace('.html', '')[1:].replace('/index', '')
                                g, created = Graph.objects.get_or_create(name=category.a.text.partition('for')[0], slug=slug.partition('/')[0], category=last_cat)
                                self.stdout.write('---Graph: %s\n' % (g.name))
                                services = category.findChildren('span', attrs={'class': 'service'})
                                for service in services:
                                    if 'for' not in service.a.text:
                                        graph_base_url = baseUrl + '/munin-cgi/munin-cgi-graph/' + nodeGroup.a.text + '/' + service.a.get('href').replace('.html', '').replace('/index', '')
                                        pageurl = baseUrl + '/' + nodeGroup.a.text + '/' + service.a.get('href')
                                        nodegraph, created = NodeGraphs.objects.get_or_create(node=n, graph=g, baseurl=graph_base_url, pageurl=pageurl)
                                        #  this is the link for the four final graphs (day, week, month, year)
                                        self.stdout.write('---Service: %s, %s\n' % (service.a.text, pageurl))

    def handle_noargs(self, **options):
        self.delete_garbage()
        self.parse_v1()
        self.parse_v2()
