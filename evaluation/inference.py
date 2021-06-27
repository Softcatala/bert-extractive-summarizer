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

from findfiles import FindFiles
import re
import datetime
import os
import shutil

def main():

    HYPO_DIR = 'hypo'

    print(f"Inference of texts and write summaries into '{HYPO_DIR}' directory")

    if os.path.exists(f'{HYPO_DIR}'):
        shutil.rmtree(f'{HYPO_DIR}')

    os.makedirs(f'{HYPO_DIR}')
    hypos = []

    findFiles = FindFiles()

    start_time = datetime.datetime.now()
    cnt = 0
    for filename in findFiles.find("split/", 'text*.ca'):
        num = re.findall(r'\d+', filename)[0]

        text_fn = f"hypo/summary-{num}.ca"  
        hypo_fn = f"{HYPO_DIR}/summary-{num}.ca"
        
        cmd = f'python3 ../summarize.py -path {text_fn} > {hypo_fn}'
        print(cmd)
        os.system(cmd)

        cnt = cnt + 1

        if cnt % 10 == 0:
            print(f"Processing: {cnt}")

        with open(hypo_fn, "r") as fh:
            hyp = fh.read()
            hypos.append(hyp)
                
    with open(f"{HYPO_DIR}/hypos.ca", "w") as fh:
        for hyp in hypos:
            fh.write(hyp)

    diff = (datetime.datetime.now() - start_time) /cnt
    print(f"Average time per summary: {diff}")


if __name__ == "__main__":
    main()
