#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
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

import os
import shutil

def read_lines():

    with open("MLSUM-Catalan/data/processed/ca_train.txt", "r") as fh:
        return fh.readlines()
                  
def main():

    print("Reads MLSUM input, spits text and summary, and saves in a")
    print("single file the summaries to run later metrics")

    SPLIT_DIR = 'split'

    refs = []

    if os.path.exists(f'{SPLIT_DIR}'):
        shutil.rmtree(f'{SPLIT_DIR}')

    os.makedirs(f'{SPLIT_DIR}')

    lines = read_lines()
    cnt = 0
    
    for line in lines:
        #url 0  + url_date 1 + text 2 +  summary 3+  title 4+  topic 5+  '\n')
     
        fields = line.split('\t')

        text = fields[2]
        summary = fields[3]

        text_fn = f"{SPLIT_DIR}/text-{cnt}.ca"
        summary_fn = f"{SPLIT_DIR}/summary-{cnt}.ca" 
        with open(text_fn, "w") as text_fh, open(summary_fn, "w") as summary_fh:
            text_fh.write(text)
            summary_fh.write(summary)

        cnt = cnt + 1
        refs.append(summary)

        if cnt == 50:
            break

    with open(f"{SPLIT_DIR}/summary.ca", "w") as fh:
        for ref in refs:
            fh.write(ref + "\n")


if __name__ == "__main__":
    main()
