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
from rouge import Rouge
import json

def main():

   ## print("Calculates metrics")

#    for cnt in range(0, 20):
    with open(f"summary.ca", "r") as fh_ref, open(f"hypos.ca", "r") as fh_hyp:
        refs = fh_ref.readlines()
        hyps = fh_hyp.readlines()

        rouge = Rouge()
        #scores = rouge.get_scores(hyps, refs)
        #print(scores)
        # or

        #hyps, refs = map(list, zip(*[[d['hyp'], d['ref']] for d in data]))            
        scores = rouge.get_scores(hyps, refs, avg=True)
        formatted_scores = json.dumps(scores, indent=4)
    
#        print(type(scores))
        print(f"Avg: {formatted_scores}")
       
    print(f"ref lines {len(refs)} - hypo lines {len(hyps)}")


if __name__ == "__main__":
    main()
