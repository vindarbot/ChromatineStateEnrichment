#!/usr/bin/env python

import os
import sys
from yattag import Doc
from name import name
from coordinates import coordinates
from state_to_gene import state_to_gene
from state_to_name import state_to_name
from results import results
from decimal import *
import argparse


os.system("python3 python/index.py")

for state in state_to_gene.keys():

	os.system("python3 python/states.py --state "+str(state)+"")

	os.system("python3 python/show_state_to_genes.py --state "+str(state)+"")

os.system("python3 python/genes.py")