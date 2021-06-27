# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import fnmatch
import os
import re
from functools import cmp_to_key

def num_comp(a, b):
    num_a = int(re.findall(r'\d+', a)[0])
    num_b = int(re.findall(r'\d+', b)[0])
    if num_a > num_b:
        return 1
    elif num_a == num_b:
        return 0
    else:
        return -1


class FindFiles(object):


    def find(self, directory, pattern):
        filelist = []

        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    filelist.append(filename)

        cmp_items_py = cmp_to_key(num_comp)
        filelist.sort(key=cmp_items_py)
        return filelist
