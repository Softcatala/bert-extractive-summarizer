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

import random
import argparse


def main():

    parser = argparse.ArgumentParser(description='Process and summarize lectures')
    parser.add_argument('-path', dest='path', default=None, help='File path of lecture')

    args = parser.parse_args()
    filename = args.path
    if filename == None:
        print("Missing parameter -path")
        return    

    with open(filename, "r") as fh_text:
        sentences = []
        lines = fh_text.readlines()
        for line in lines:
            sentences_line = line.split('.')
            for sentence in sentences_line:
                sentences.append(sentence)

        idxs = random.sample(range(0, len(sentences) - 1), 3)

        txt =''
        for idx in idxs:
            txt += sentences[idx] + ". "

        print(txt)
    
if __name__ == "__main__":
    main()
