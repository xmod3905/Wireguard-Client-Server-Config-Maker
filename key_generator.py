import argparse, subprocess, os
from datetime import datetime as dt

def privateGenKey():
    key = subprocess.run(["wg genkey"], shell=True, capture_output=True, text=True)
    return key.stdout.strip()

def publicGenKey(privateKey):
    key = subprocess.run(f"echo {privateKey} | wg pubkey", shell=True, capture_output=True, text=True)
    return key.stdout.strip()

def fileMaker(name, value, mode="x"):
    s = open(name, mode)
    s.write(value)
    s.close()
    
def nameGenerator():
    now = dt.now()
    current = now.strftime("%Y_%b_%d-%H_%M_%S")
    return current

def builder(agrs):
    folderPath = nameGenerator()
    serverPath =os.path.join(folderPath, 'server') 
    os.makedirs(serverPath, exist_ok=True)
    clientName = [part.strip() for part in agrs.client.split(',')]
    
    serverPort = agrs.server_port
    privateKeyServer = privateGenKey()
    pubicKeyServer = publicGenKey(privateKeyServer)
    dns = agrs.dns
    serverAddress = agrs.server_address
    serverConfigTemplate = f'''
    [Interface]
    PrivateKey={privateKeyServer}
    Address = 10.0.0.1/23
    PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o ens4 -j MASQUERADE
    PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o ens4 -j MASQUERADE
    ListenPort = {serverPort}
    '''

    clientConfigTemplate = f'''
    [Interface]
    Address = ADDRESS_VALUE
    PrivateKey = PRIVATEKEY_VALUE
    ListenPort = {serverPort}
    DNS = {dns}

    [Peer]
    PublicKey = {pubicKeyServer}
    Endpoint = {serverAddress}:{serverPort}
    AllowedIPs = 0.0.0.0/0
    '''

    # Make Server Config
    fileMaker(os.path.join(serverPath,"server.conf"), serverConfigTemplate, "x")

    # Make Server Privete Key File
    fileMaker(os.path.join(serverPath,"serverPrivete.key"), privateKeyServer, "x")

    # Make Server Public Key File
    fileMaker(os.path.join(serverPath,"serverPublic.key"), pubicKeyServer,  "x")
    
    for i,name in enumerate(clientName):
        clientPrivete = privateGenKey()
        clientPublic = publicGenKey(clientPrivete)
        clientIp = f"10.0.0.{i+2}"
        confValue = clientConfigTemplate.replace('ADDRESS_VALUE', clientIp).replace('PRIVATEKEY_VALUE', clientPrivete)
        toServerConfig = f'''
    # {name} Peer
    [Peer]
    PublicKey={clientPublic}
    AllowedIPs = {clientIp}/32'''
        clientFolderPath = os.path.join(folderPath, f"peer_{name}")
        os.makedirs(clientFolderPath, exist_ok=True)
        # Make Peer Conf
        fileMaker(os.path.join(clientFolderPath, f"{name}_peer.conf"), confValue, "x")
        
        # Make Client Privete Key File
        fileMaker(os.path.join(clientFolderPath, f"{name}_Privete.key"), clientPrivete, "x")
        
        # Make Client Public Key File
        fileMaker(os.path.join(clientFolderPath, f"{name}_Public.key"), clientPublic, "x")
        
        # Adding Peer Config to server config
        fileMaker(os.path.join(serverPath,"server.conf"), toServerConfig, "a")
    print(f'Key successfully created! it is stored in {folderPath}')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p','--server_port', 
        type=int,
        default= 51820,
        help="define server port (default: 51820)"
    )
    parser.add_argument(
        '-d','--dns', 
        type=str, 
        default='1.1.1.1',
        help="define dns in string format (for multiple dns server use coma ',' for separator)",
    )
    parser.add_argument(
        '-s','--server_address', 
        type=str, 
        default='0.0.0.0',
        help="define server address",
    )
    parser.add_argument(
        '-c','--client_names', 
        type=str, 
        default='peer1,peer2',
        help="define dns in string format (for multiple client server use coma ',' for separator)",
    )
    args = parser.parse_args()
    builder(args)