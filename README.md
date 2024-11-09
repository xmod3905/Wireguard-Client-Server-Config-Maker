# Wireguard Client & Server Config Maker
[![Commits](https://img.shields.io/github/commit-activity/m/xmod3905/Wireguard-Client-Server-Config-Maker?label=commits&style=for-the-badge&logo=github)](https://github.com/xmod3905/Wireguard-Client-Server-Config-Maker/commits "Commit History")
![GitHub Repo stars](https://img.shields.io/github/stars/xmod3905/Wireguard-Client-Server-Config-Maker?style=for-the-badge&logo=github)
![GitHub License](https://img.shields.io/github/license/xmod3905/Wireguard-Client-Server-Config-Maker?style=for-the-badge&logo=github)
![GitHub contributors](https://img.shields.io/github/contributors/xmod3905/Wireguard-Client-Server-Config-Maker?style=for-the-badge&logo=github)
![GitHub Created At](https://img.shields.io/github/created-at/xmod3905/Wireguard-Client-Server-Config-Maker?style=for-the-badge&logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/xmod3905/Wireguard-Client-Server-Config-Maker?style=for-the-badge&logo=github)




A Python-based tool to generate WireGuard configuration files for both client and server.

## Dependencies
- Python
- WireGuard

## Usage
To generate WireGuard configuration files, run the `key_generator.py` script with the following options:
```bash
python3 key_generator.py [-h] [-p SERVER_PORT] [-d DNS] [-s SERVER_ADDRESS] [-c CLIENT_NAMES]
```

### Options:
- `-h, --help`: Show this help message and exit.
- `-p SERVER_PORT, --server_port SERVER_PORT`: Define the server port (default: 51820).
- `-d DNS, --dns DNS`: Define DNS servers in string format (for multiple DNS servers, use a comma `,` as separator).
- `-s SERVER_ADDRESS, --server_address SERVER_ADDRESS`: Define the server address.
- `-c CLIENT_NAMES, --client_names CLIENT_NAMES`: Define client names in string format (for multiple clients, use a comma `,` as separator).

## Example Usage:
```bash
python key_generator.py -p 51820 -d "8.8.8.8,8.8.4.4" -s "192.168.1.1" -c "client1,client2"
```
or
```bash
python3 key_generator.py -p 51820 -d "8.8.8.8,8.8.4.4" -s "192.168.1.1" -c "client1,client2"
```

>This will generate the WireGuard configuration files for the specified clients and server.
