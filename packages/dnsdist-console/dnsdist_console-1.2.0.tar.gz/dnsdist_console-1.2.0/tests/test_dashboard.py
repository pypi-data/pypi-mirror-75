from dnsdist_console import Console
from dnsdist_console import Dashboard

console_ip = "10.0.0.27"
console_port = 5199
console_key = "OTgmgAR6zbrfrYlKgsAAJn+by4faMqI1bVCvzacXMW0="

c = Console(host=console_ip, port=console_port, key=console_key)

Dashboard(console=c)