#!/usr/bin/python3
# coding: utf-8
import os
import subprocess
from urllib.parse import urlsplit

from core.config import *
from core.result import ResultToExcel
from core.utils import mkdir


class Vuln:
    def __init__(self,domainlist):
        self.domain = ""
        self.domainlist = domainlist
        self.outpath = ""
        self.ipfile = ""
        self.domainfile = ""
        self.url = ""

    def httpx_title(self):
        print('\033[1;34m [+]Start httpx-title \033[0m \033[1;31m {} \033[0m'.format(self.domain))
        if os.path.exists(self.domainfile):
            httpx_command = httpx +" -nc -retries 3 -timeout 3 -status-code -title -l " + self.domainfile + " -o " + self.outpath + "httpx_" + self.domain + ".txt"
            print("\033[0;32m " + httpx_command + " \033[0;32m ")
            result = subprocess.Popen(httpx_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            result.wait()
            os.system("rm -rf "+httpx_tmp)
            return
    def httpx_url(self):
        print('\033[1;34m [+]Start httpx-url \033[0m \033[1;31m {} \033[0m'.format(self.domain))
        if os.path.exists(self.domainfile):
            httpx_command = httpx + " -silent -nc -mc 200,301,302 -l " + self.domainfile + " -o " + self.outpath + "httpx_url_" + self.domain + ".txt"
            print("\033[0;32m " + httpx_command + " \033[0;32m ")
            result = subprocess.Popen(httpx_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            result.wait()
            os.system("rm -rf " + httpx_tmp)
            return
    def urlfinder(self):
        print('\033[1;34m [+]Start urlfinder \033[0m \033[1;31m {} \033[0m'.format(self.domain))
        mkdir(self.outpath + "urlfinder")
        if os.path.exists(self.outpath+"httpx_url_" + self.domain + ".txt"):
            urlfinder_command = urlfinder + " -s all -m 2 -f "+self.outpath+"httpx_url_" + self.domain + ".txt -o " + self.outpath +"urlfinder/"
            print("\033[0;32m " + urlfinder_command + " \033[0;32m ")
            result = subprocess.Popen(urlfinder_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            result.wait()
            return

    def ffuf(self):
        print('\033[1;34m [+]Start ffuf \033[0m \033[1;31m {} \033[0m'.format(self.domain))
        mkdir(self.outpath + "ffuf")
        if os.path.exists(self.outpath+"httpx_url_" + self.domain + ".txt"):
            for urls in open(self.outpath+"httpx_url_" + self.domain + ".txt"):
                url = urls.strip()
                ffuf_command = ffuf + " -mc 200,302 -c -s -w " +ffuf_dict+" -u {0}/FUZZ -recursion -recursion-depth 2 -o ".format(url) + self.outpath + "ffuf/"+urlsplit(url).hostname+".txt"
                print("\033[0;32m " + ffuf_command + " \033[0;32m ")
                result = subprocess.Popen(ffuf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                result.wait()
            return
    def katana(self):
        print('\033[1;34m [+]Start katana \033[0m \033[1;31m {} \033[0m'.format(self.domain))
        mkdir(self.outpath + "katana")
        if os.path.exists(self.outpath+"httpx_url_" + self.domain + ".txt"):
            for urls in open(self.outpath+"httpx_url_" + self.domain + ".txt"):
                url = urls.strip()
                katana_command = katana + " -u {} -o ".format(url) + self.outpath + "katana/"+urlsplit(url).hostname+".txt"
                print("\033[0;32m " + katana_command + " \033[0;32m ")
                result = subprocess.Popen(katana_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                result.wait()
            return


    def list_subdomain(self):
        for domain in self.domainlist:
            print('\033[1;34m [+]Start Vulnscan \033[0m \033[1;31m {} \033[0m'.format(domain))
            self.domain = domain
            self.outpath = "/tmp/"+self.domain+"/"
            self.ipfile = self.outpath+"allinone_ip_"+self.domain+".txt"
            self.domainfile = self.outpath+"allinone_domain_"+self.domain+".txt"
            if os.path.exists(self.domainfile) or os.path.exists(self.ipfile):
                self.httpx_title()
                self.httpx_url()
                self.urlfinder()
                self.ffuf()
                self.katana()

            self.save()

    def save(self):
        print("\033[0;32m " + "正在保存title结果到xlsx文件中" + " \033[0;32m ")
        ResultToExcel(self.outpath + self.domain + ".xlsx", "title").saveHttpxTitle(self.outpath + "httpx_" + self.domain + ".txt")