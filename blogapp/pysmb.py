from smb.SMBConnection import SMBConnection


server_ip = "192.168.0.103" # Take your server IP - I have put a fake IP :)
server_name = 'myserver' # The servername for the IP above
share_name = "python" # This is the principal folder of your network that you want's to connect
network_username = 'smb' # This is your network username
network_password = '123' # This is your network password
# machine_name = 'myuser@mac-mc70006405' # Your machine name
conn = SMBConnection(network_username, network_password, server_name, use_ntlm_v2 = True)
assert conn.connect(server_ip, 139)
files = conn.listPath(share_name, "/TECNOLOGIA_INFORMACAO/Dashboard Diretoria/")
for item in files:
   print(item.filename)
