import os
import paramiko
import time 
import pandas as pd
from io import StringIO


class HiveConnect:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
       
    def fetch(self, query):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, username=self.user,
             password=self.password)
            command = " hive -e 'use marketing; set hive.cli.print.header=true;" + query + "'" 
            #print cmd
            _, ssh_stdout, _  = ssh.exec_command(command)
            edge_out_str = str(ssh_stdout.read())
            edge_out_str_t = ",".join(edge_out_str.split("\\t"))
            edge_out_str_n = "\n".join(edge_out_str_t.split("\\n"))
            edge_out_str_n = edge_out_str_n[2:]
            edge_out_str_n = edge_out_str_n[:-1]
            edge_out_csv = StringIO(edge_out_str_n)
            df = pd.read_csv(edge_out_csv, sep=",")
            return df
        except:
            print("There was an exception...")
            raise
        finally:
            if ssh:
                ssh.close()
    
    def Save(self, data, path):
        data.to_csv(path, index=False)
