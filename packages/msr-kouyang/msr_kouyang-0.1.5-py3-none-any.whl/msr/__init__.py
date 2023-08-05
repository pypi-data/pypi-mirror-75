#!/usr/bin/env python3
# import sys
# import argparse
# from urllib.parse import urlparse
# from urllib.request import urlopen
# from time import time
#
# import os
#
# def version():
#     print(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION"))
#     with open("../VERSION", "r") as fv:
#         version = fv.read().rstrip('\n')
#         print(version)
#
# def register():
#     if url_is_valid(args.url):
#         # TODO: add to registry
#         print("Added " + args.url + " to registry.")
#     else:
#         print(args.url + " is not a valid url.")
#         sys.exit(1)
#
# def measure():
#     print('measure')
#
# def race():
#     # TODO: read data from registry
#     times = [ None for x in registry ]
#     for i, url in enumerate(registry):
#         times[i] = get_time(url)
#
#     # TODO: pretty print
#     print(registry)
#     print(times)
#
#
# # -- helper functions
#
# def get_time(url: str) -> float:
#     req = urlopen(url)
#     start = time()
#     req.read()
#     end = time()
#     return end - start
#
# def url_is_valid(url: str) -> bool:
#     try:
#         res = urlparse(url)
#         return all([res.scheme, res.netloc, res.path])
#     except:
#         return False
#
# # -- parse CLI arguments
#
# function_map = {
#     'version' : version,
#     'register' : register,
#     'measure' : measure,
#     'race' : race
# }
#
# parser = argparse.ArgumentParser(description="Measure web pages.")
# subparsers = parser.add_subparsers(dest='command')
#
# parser_register = subparsers.add_parser('register')
# parser_register.add_argument('url')
# subparsers.add_parser('measure')
# subparsers.add_parser('race')
# subparsers.add_parser('version')
#
# args = parser.parse_args()
# if len(sys.argv) < 2:
#     parser.print_help()
#     sys.exit(1)
#
# function_map[args.command]()
