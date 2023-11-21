import socket
import common_ports

# Check if the address is an IP by checking if the last part is not alphabetic
def is_ip(address):
    return not address.split(".")[-1].isalpha()

def get_open_ports(target, port_range, verbose=False):
  open_ports = []
  hostname = ""

  # Validate the target (IP address or hostname)
  if is_ip(target):
    try:
      socket.inet_aton(target)
    except socket.error:
      return "Error: Invalid IP address"
  else:
    try:
      IpOfTarget = socket.gethostbyname(target)
    except socket.error:
      return "Error: Invalid hostname"
      
  # Try to connect to each port, if port is open, we add it to the list of open ports.
  for port in range(port_range[0], port_range[1] + 1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.settimeout(1)
      try:
        if sock.connect_ex((target, port)) == 0:
          open_ports.append(port)
      except socket.error:
        pass

  # If verbose is True, provide a detailed response
  if verbose:
    verboseResponse = []
    if is_ip(target): 
      # getfqdn resolves hostname from IP or returns IP if no hostname.
      hostnameOfIp = socket.getfqdn(target)
      if is_ip(hostnameOfIp):
        verboseResponse.append(f"Open ports for {target}\nPORT     SERVICE")
      else: 
        verboseResponse.append(f"Open ports for {hostnameOfIp} ({target})\nPORT     SERVICE")
    elif hostname: 
      verboseResponse.append(f"Open ports for {target} ({IpOfTarget})\nPORT     SERVICE")
    
    # Format and add open ports to the verbose response
    for select in open_ports:
      formated = str(select).ljust(8, " ")
      verboseResponse.append(f"{formated} {common_ports.ports_and_services[select]}")
      
    # Join the verbose response for a formatted output and return the result
    verboseRez = "\n".join(verboseResponse)
    return verboseRez
  else:
    return open_ports
