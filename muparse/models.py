# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models


MUNIN_VERSION_CHOICES = (
    ('v1', 'version 1'),
    ('v2', 'version 2'),
)


class MuninNodes(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    cgi_path = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255, blank=True)
    munin_version = models.CharField(
        max_length=2,
        choices=MUNIN_VERSION_CHOICES
    )

    def __unicode__(self):
        return self.name

    def as_dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'cgi_path': self.cgi_path,
            'image_path': self.image_path,
            'version': self.munin_version
        }


class NodeGroup(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=512)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class GraphCategory(models.Model):
    name = models.SlugField(max_length=255)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Graph(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=128, blank=True, null=True)
    category = models.ForeignKey(GraphCategory)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Node(models.Model):
    name = models.SlugField(max_length=255)
    url = models.CharField(max_length=512)
    group = models.ForeignKey(NodeGroup)
    graphs = models.ManyToManyField(Graph, blank=True, null=True, through='NodeGraphs')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_graph_categories(self):
        cat_list = []
        for graph in self.graphs.all():
            cat_list.append(graph.category.pk)
        return GraphCategory.objects.filter(pk__in=list(set(cat_list)))

    class Meta:
        ordering = ['name']


class NodeGraphs(models.Model):
    node = models.ForeignKey(Node)
    graph = models.ForeignKey(Graph)
    baseurl = models.CharField(max_length=512)
    pageurl = models.CharField(max_length=512)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s:%s:%s' %(self.node, self.graph, self.baseurl)


class SavedSearch(models.Model):
    description = models.CharField(max_length=255)
    display_type = models.CharField(max_length=64)
    graphs = models.ManyToManyField(NodeGraphs, blank=True, null=True)

    def __unicode__(self):
        return self.description
