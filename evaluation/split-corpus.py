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
import datetime

def read_lines():

    with open("ca_train.txt", "r") as fh:
        return fh.readlines()
                  
def main():

    print("Reads MLSUM input and spits text and summary, calculates hypotesis")
    print("and saves in a single file to run later metrics")


    hypos = []
    refs = []

    lines = read_lines()
    cnt = 0
    start_time = datetime.datetime.now()

    for line in lines:
        #url 0  + url_date 1 + text 2 +  summary 3+  title 4+  topic 5+  '\n')
     
        fields = line.split('\t')

        text = fields[2]
        summary = fields[3]

        text_fn = f"data/text-{cnt}.ca"
        with open(text_fn, "w") as text_fh, open(f"data/summary-{cnt}.ca", "w") as summary_fh:
            text_fh.write(text)
            summary_fh.write(summary)

        cmd = f'python3 ../summarize.py -path {text_fn} > hypo/summary-{cnt}.ca'
        os.system(cmd)

        with open(f"hypo/summary-{cnt}.ca", "r") as fh:
            hyp = fh.read()

        refs.append(summary)
        hypos.append(hyp)

        cnt = cnt + 1

        if cnt % 10 == 0:
            print(f"Processing: {cnt}")

        if cnt == 50:
            break

    with open("summary.ca", "w") as fh:
        for ref in refs:
            fh.write(ref + "\n")

    with open("hypos.ca", "w") as fh:
        for hyp in hypos:
            fh.write(hyp)

    diff = (datetime.datetime.now() - start_time) /cnt
    print(f"Average time per summary: {diff}")


if __name__ == "__main__":
    main()
