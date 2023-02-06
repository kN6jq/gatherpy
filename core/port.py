#!/usr/bin/python3
# coding: utf-8
import os
import subprocess

from core.config import txportmap
from core.result import ResultToExcel


class Port:
    def __init__(self,domainlist):
        self.domain = ""
        self.domainlist = domainlist
        self.outpath = ""
        self.ipfile = ""


    def portscan(self):
        if os.path.exists(self.ipfile):
            txportmap_command = txportmap + " -l " + self.ipfile + " -nocolor -t1000 -o " + self.outpath + "txportmap_" + self.domain + ".txt"
            print("\033[0;32m " + txportmap_command + " \033[0;32m ")
            result = subprocess.Popen(txportmap_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            result.wait()
            return

    def list_subdomain(self):
        for domain in self.domainlist:
            print('\033[1;34m [+]Start Portscan \033[0m \033[1;31m {} \033[0m'.format(domain))
            self.domain = domain
            self.outpath = "/tmp/"+self.domain+"/"
            self.ipfile = self.outpath+"allinone_ip_"+self.domain+".txt"
            self.portscan()
            self.save()
            break


    def save(self):
        print("\033[0;32m " + "正在保存端口结果到xlsx文件中" + " \033[0;32m ")
        ResultToExcel(self.outpath+self.domain+".xlsx","port").savePort(self.outpath + "txportmap_" + self.domain + ".txt")