#!/usr/bin/python3
# coding: utf-8
import argparse
from core.port import Port
from core.subdomain import Subdomain
from core.vuln import Vuln

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--target', default='google.com', help='domain name')
    parser.add_argument('--targets', default='domain.txt',help='domain name file')
    parser.add_argument('-s',action="store_true",help='Subdomain for domain')
    parser.add_argument('-p',action="store_true",help='Port for domain')
    parser.add_argument('-v',action="store_true",help='Vuln for domain')
    # parser.add_argument('-i',action="store_true",help='insert data to db')

    args = parser.parse_args()
    domains_list = []



    if args.target:
        domains_list.append(args.target)
    elif args.targets:
        with open(args.targets, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                domains_list.append(line)
    else:
        print('Please enter the domain name or domain name file')
    domains_list = list(set(domains_list))
    if args.s:
        print('Start Subdomain for domain')
        Subdomain(domains_list).list_subdomain()
    if args.p:
        print('Start Port for domain')
        Port(domains_list).list_subdomain()
    if args.v:
        print('Start Vuln for domain')
        Vuln(domains_list).list_subdomain()
    # if args.i:
    #     print('Start insert data to db')
    #     DB(domains_list).list_subdomain()