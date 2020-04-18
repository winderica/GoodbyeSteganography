#!/usr/bin/env python
import argparse
from encrypt import encrypt
from decrypt import decrypt

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', required=True)
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-b', '--block_size', default=8, type=int)
parser.add_argument('-k', '--key', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e', '--encrypt', action='store_true')
group.add_argument('-d', '--decrypt', action='store_true')
args = parser.parse_args()

if args.encrypt:
    encrypt(args.input, args.output, args.block_size, args.key)
if args.decrypt:
    decrypt(args.input, args.output, args.block_size, args.key)
