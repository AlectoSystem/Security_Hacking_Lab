import requests,sys,itertools,pathlib,argparse,socket,platform,gc
from urllib.parse import urlparse
from pprint import pprint

class Gobuster:

      def __init__(self,target_url):
          #[*] Prepare a word list and overwrite it.
          self.word_path = "wordlists"
          self.url = target_url
          self.cycle = itertools.cycle(r"/-\|")
          

      def wordlists(self):
          return [file_path for file_path in pathlib.Path(self.word_path).glob("*.list")]

      def file_line_get(self,file_path,point=0):

           for _ in open(file_path,"r",encoding="utf-8").readlines():
              point += 1
           return point

      def status_code_get(self,file_path,point_code,list_connect=[],point=0):
           
          for word_file in file_path:
              for wordlist in open(word_file,"r",encoding="utf-8").readlines():
                  point += 1              
                  data = (point / point_code) * 100
                  add_link = f"{self.url}/{wordlist}"
                  status_date = requests.get(add_link,timeout=10).status_code
                  sys.stdout.write("\r\n")
                  sys.stdout.write(f"[*] URL / {add_link}[+]<{status_date}> {point}/{point_code} - <{data}%>")
                  gc.collect()

                  if status_date < 404:
                     list_connect.append(add_link)
          return list_connect

def main(point=0):

          try:

              arg = argparse.ArgumentParser()
              arg.add_argument("-url",type=str,help="Target_URL / -url < target_url >")
              parse = arg.parse_args()
              ip_url = socket.gethostbyname(urlparse(parse.url).netloc)
              path_get,file_name = "Status_Link_List",f"{urlparse(parse.url).netloc}_status.list"
             
              print(f"""
                     [!] Target_URL / {parse.url}\n
                     [!] HostByName / {ip_url}\n
                     [*] Save_Path / {path_get}\n
                     """)

              gobuster = Gobuster(parse.url)
              for file_path in gobuster.wordlists():
                  point += gobuster.file_line_get(file_path)

              word_status = gobuster.status_code_get(gobuster.wordlists(),point)
              pathlib.Path(path_get).mkdir(exist_ok=True)
              with open(f"{path_get}/{file_name}")as link_file:
                   for link_code in word_status:
                       link_file.write(f"{link_code}\n")
                  
          except TypeError:
                 if platform.system() == "Linux":
                    sys.stdout.write("\n[#] Check,Help_Command / root@Linux_Platform: python3 gobuster.py -h  \n")
                 elif platform.system() == "Windows":
                    sys.stdout.write("\n[#] Check,Help_Command / C:/User/Windows_Platform> python gobuster.py -h \n")
                 sys.exit()
          except KeyboardInterrupt:
                 sys.stdout.write("\nStop_Process...\n")
                 sys.exit()

if __name__ == "__main__":

   main()
