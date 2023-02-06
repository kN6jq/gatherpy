#!/usr/bin/python3
# coding: utf-8
import os
import subprocess

from core.config import *
from core.result import ResultToExcel
from core.utils import mkdir


class Subdomain:
    def __init__(self, domainlist):
        self.domain = ""
        self.domainlist = domainlist
        self.outpath = ""

    def list_subdomain(self):
        for domain in self.domainlist:
            self.domain = domain
            self.outpath = "/tmp/" + domain + "/"
            mkdir(self.outpath)
            print("Start scan "+domain)
            self.scan()


    def scan(self):
        print('\033[1;34m 开始扫描子域名\033[0m \033[1;31m\033[0m')
        self.ksubdomain(self.domain)
        self.subfinder(self.domain)
        self.oneforall(self.domain)
        self.subDomainsBrute(self.domain)
        self.xray(self.domain)
        print('\033[1;34m 扫描子域名完成\033[0m \033[1;31m\033[0m')
        self.result()
        self.save()

    def result(self):
        print('\033[1;34m [+]Start result\033[0m \033[1;31m\033[0m')
        # 先创建域名和ip的文件
        os.system("touch "+self.outpath + "domain_" + self.domain + ".txt")
        os.system("touch "+self.outpath + "ip_" + self.domain + ".txt")
        ksubdomain_domain_command = "awk -F '[=]' '{print $1}' " + self.outpath + "ksubdomain_" + self.domain + ".txt | sort -u >> " + self.outpath + "domain_" + self.domain + ".txt"
        ksubdomain_ip_command = 'grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ' + self.outpath + "ksubdomain_" + self.domain + ".txt | sort -u >> " + self.outpath + "ip_" + self.domain + ".txt"
        subfinder_domain_command = "cat " + self.outpath + "subfinder_" + self.domain + ".txt | sort -u >> " + self.outpath + "domain_" + self.domain + ".txt"
        onforall_domain_command = "awk -F ',' '{print $6}' " + self.outpath + "oneforall_" + self.domain + ".txt | grep -v 'subdomain' | sort -u >> " + self.outpath + "domain_" + self.domain + ".txt"
        subDomainsBrute_domain_command = "awk -F '[ ]' '{print $1}' " + self.outpath + "subDomainsBrute_" + self.domain + ".txt | sort -u >> " + self.outpath + "domain_" + self.domain + ".txt"
        subDomainsBrute_ip_command = 'grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ' + self.outpath + "subDomainsBrute_" + self.domain + ".txt | sort -u >> " + self.outpath + "ip_" + self.domain + ".txt"
        xray_domain_command = "awk -F '[,]' '{print $1}' " + self.outpath + "xray_" + self.domain + ".txt | sort -u >> " + self.outpath + "domain_" + self.domain + ".txt"
        xray_ip_command = "awk -F '[,]' '{print $2}' " + self.outpath + "xray_" + self.domain + ".txt | sort -u >> " + self.outpath + "ip_" + self.domain + ".txt"

        # 对域名和ip进行去重
        # cat ip_txttool.com.txt | sort | uniq | grep -v '^$' >
        allinone_domain_command = "cat " + self.outpath + "domain_" + self.domain + ".txt | sort | uniq | grep -v ' ' >" + self.outpath + "allinone_domain_" + self.domain + ".txt"
        allinone_ip_command = "cat " + self.outpath + "ip_" + self.domain + ".txt | sort | uniq |grep -v '^$' > " + self.outpath + "allinone_ip_" + self.domain + ".txt"

        command = [ksubdomain_domain_command, ksubdomain_ip_command, subfinder_domain_command, onforall_domain_command, subDomainsBrute_domain_command, subDomainsBrute_ip_command, xray_domain_command, xray_ip_command, allinone_domain_command, allinone_ip_command]

        for cmd in command:
            try :
                print("\033[0;32m " + cmd + " \033[0;32m ")
                # result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                # result.wait()
                os.system(cmd)
            except Exception as e:
                print(e)
                continue
            # 去除内网的ip
        print('\033[1;34m 去除内网ip\033[0m \033[1;31m\033[0m')
        os.system(
            'grep -E -v "^10\.|192.168\.|172\.(2[6-9]|3[0-2])\." ' + self.outpath + "allinone_ip_" + self.domain + ".txt | anew " + self.outpath + "allinone_ip_" + self.domain + ".txt")
        print('\033[1;34m 结果整理完成\033[0m \033[1;31m\033[0m')
        return
    def ksubdomain(self, domain):
        """ksubdomain:爆破域名收集域名\n
           https://github.com/projectdiscovery/ksubdomain
        """
        print('\033[1;34m [+]Start Ksubdomain==>\033[0m \033[1;31m {} \033[0m'.format(domain))
        scanCommand = ksubdomain_path+" e -d {} --skip-wild -o {}".format(domain, self.outpath +"ksubdomain_"+ domain+".txt")
        print("\033[0;32m "+scanCommand+" \033[0;32m ")
        result= subprocess.Popen(scanCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result.wait()
        return

    def subfinder(self, domain):
        """subfinder:爆破域名收集域名\n
           https://github.com/projectdiscovery/subfinder
        """
        print('\033[1;34m [+]Start Subfinder==>\033[0m \033[1;31m {} \033[0m'.format(domain))
        scanCommand = subfinder_path+" -d {} -silent -all -o {}".format(domain,self.outpath + "subfinder_"+domain + ".txt")
        print("\033[0;32m "+scanCommand+" \033[0;32m ")
        result= subprocess.Popen(scanCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result.wait()
        return

    def oneforall(self, domain):
        """oneforall:爆破域名收集域名\n
           https://github.com/shmilylty/OneForAll
        """
        print('\033[1;34m [+]Start OneForAll==>\033[0m \033[1;31m {} \033[0m'.format(domain))
        scanCommand = "python3 "+ oneforall_path+" --target={} run --path {}".format(domain, self.outpath +"oneforall_"+domain + ".txt")
        print("\033[0;32m "+scanCommand+" \033[0;32m ")
        result= subprocess.Popen(scanCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result.wait()
        return

    def subDomainsBrute(self, domain):
        """subDomainsBrute:爆破域名收集域名\n
           https://github.com/lijiejie/subDomainsBrute
        """
        print('\033[1;34m [+]Start subDomainsBrute==>\033[0m \033[1;31m {} \033[0m'.format(domain))
        scanCommand = "python3 "+ subDomainsBrute_path+" {} --full -o {}".format(domain,self.outpath +"subDomainsBrute_"+ domain + ".txt")
        print("\033[0;32m "+scanCommand+" \033[0;32m ")
        result= subprocess.Popen(scanCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result.wait()
        return

    def xray(self, domain):
        """xray:爆破域名收集域名\n

        """
        print('\033[1;34m [+]Start Xray==>\033[0m \033[1;31m {} \033[0m'.format(domain))
        scanCommand = xray_path+" --config /pentest/xray/config.yaml subdomain --target {} --text-output {}".format(domain,self.outpath +"xray_" +domain + ".txt")
        print("\033[0;32m "+scanCommand+" \033[0;32m ")
        result= subprocess.Popen(scanCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result.wait()
        return

    def save(self):
        print("\033[0;32m " + "正在保存域名和ip结果到xlsx文件中" + " \033[0;32m ")
        ResultToExcel(self.outpath+self.domain+".xlsx","domain").saveDomain(self.outpath + "allinone_domain_" + self.domain + ".txt")
        ResultToExcel(self.outpath+self.domain+".xlsx","ip").saveIp(self.outpath + "allinone_ip_" + self.domain + ".txt")




