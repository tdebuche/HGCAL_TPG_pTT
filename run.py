import argparse
from S1_Input.Programmes.create_numbering import create_module_numbering
from pTTs.Programmes.pTTs_to_file import record_all_boards

#create S1 numbering
print(create_module_numbering())

#record pTTs

parser = argparse.ArgumentParser()
parser.add_argument("--Format",default = 'readable', help="textfile : readable, vhfile: vh")
parser.add_argument("--STCs",default = 'yes', help="With (yes) or without STCs (no)")
parser.add_argument("--Edges",default = 'no', help="With (yes) or without edges(no)")
args = parser.parse_args()


record_all_boards(args)
