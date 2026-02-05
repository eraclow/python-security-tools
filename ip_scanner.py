import ipaddress
import sys
from concurrent.futures import ThreadPoolExecutor
import subprocess
import socket



def worker_scanner(ip):  #Sends ICMP ping to check whether the host is alive.
    result = subprocess.run(["ping", "-n", "2", "-w", "200",str(ip)],stdout=subprocess.DEVNULL) #This is a Windows command so It will not work on other OS.
    if result.returncode == 0: 
        return ip
    else:
        return None

def worker_resolver(ip):   #We need another worker to resolve the alive hosts' hostnames. 
    try:
        hostname = socket.gethostbyaddr(str(ip))[0]
    except:
        hostname = "unknown"
    return (ip, hostname)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print(f"python {sys.argv[0]} <CIDR>")
        print("Example:")
        print(f"{sys.argv[0]} 192.168.1.0/24")
        sys.exit(1)
    
    CIDR = str(sys.argv[1])

    try:
        network = ipaddress.ip_network(CIDR)
    except ValueError:
        print(f"[!] Invalid CIDR: {CIDR}")
        sys.exit(1)
    
    hosts = list(network.hosts())

    with ThreadPoolExecutor(max_workers=30) as pool:   #30 workers are assigned here.You can change the value as you want. 
        results= pool.map(worker_scanner,hosts)  #The actual process where the IPv4 addresses in hosts are tested to see if They are up.
        alive = [ip for ip in results if ip]
    
    with ThreadPoolExecutor(max_workers=20) as pool2:
        resolving = pool2.map(worker_resolver, alive)  #Going through the list of only alive hosts to resolve their hostnames.
        resolved= list(resolving)
        hostmap = {ip: host for ip, host in resolved}
        print(f'{"IP":<15}  HOSTNAME')  #Making the output nice.
        print(f'{"-"*15}  {"-"*20}')
        
    for ip in alive:
        host = hostmap.get(ip, "unknown") 
        print(f"{str(ip):<15}  {host}")