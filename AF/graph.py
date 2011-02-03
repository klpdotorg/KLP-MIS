#!/usr/bin/env python

# Copyright (C) 2008 Adam Lofts
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# This program generates a graphviz file to plot a graph of your database layout.
# 
# Usage:
#
# Set PYTHONPATH and DJANGO_SETTINGS_MODULE for your django app
# ./graph.py <django_app_name> | dot -Tpng -o graph.png

import sys
from django.db.models import get_app, get_models


def graph(app, outfile):

    models = get_models(get_app(app))

    outfile.write("digraph G {\n")

    for model in models:

        # Format the shape
        name = model._meta.object_name
        label = "%s\\n" % name + "\\n".join([field.name for field in model._meta._fields()])
        outfile.write("%s [shape=box,label=\"%s\"];" % (name, label))

        # Draw the relations
        for related in model._meta.get_all_related_objects():
            outfile.write("\t%s -> %s;\n" % (name, related.model._meta.object_name))

        for related in model._meta.get_all_related_many_to_many_objects():
            outfile.write("\t%s -> %s [dir=both];\n" % (name, related.model._meta.object_name))

    outfile.write("}\n")

if __name__=="__main__":
   
    if len(sys.argv) != 2:
        print "graph.py <appname>"
        print "\tWrites a graph of your models suitable for processing with graphviz"
        sys.exit(1)

    graph(sys.argv[1], sys.stdout)

