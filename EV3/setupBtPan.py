#!/usr/bin/env python3

import os, sys

def main():
    try:
        distro = os.system('lsb_release -a | grep Distributor\ ID | awk \'{print $3}\'')
        if distro == 'Fedora':
            os.system('sudo dnf -y install bluez bluez-tools rfkill')
        elif distro == 'Ubuntu' or distro == 'LinuxMint' or distro == 'Debian':
            os.system('sudo apt-get -y install bluez bluez-tools rfkill')
    except OSError:
        try:
            print ('The System Encountered An Error')
            sys.exit()
        except SystemExit:
            print ('Exiting')

    os.system('sudo rfkill unblock bluetooth')
    os.system('sudo bluetoothctl power on')
    os.system('sudo bluetoothctl discoverable on')

    panNetdev_path = '/etc/systemd/network/pan0.netdev'
    panNetwork_path = '/etc/systemd/network/pan0.network'
    agentService_path = '/etc/systemd/system/bt-agent.service'
    networkService_path = '/etc/systemd/system/bt-network.service'

    if not os.path.exists(panNetdev_path):
        with open(panNetdev_path, 'w') as f:
            f.write('[NetDev]\nName=pan0\nKind=bridge')

    if not os.path.exists(panNetwork_path):
        with open(panNetwork_path, 'w') as f:
            f.write('[Match]\nName=pan0\n\n[Network]\nAddress=10.42.0.1\nDHCPServer=yes')

    if not os.path.exists(agentService_path):
        with open(agentService_path, 'w') as f:
            f.write('[Unit]\nDescription=Bluetooth Auth Agent\n\n[Service]\nExecStart=/usr/bin/bt-agent -c NoInputNoOutput\nType=simple\n\n[Install]\nWantedBy=multi-user.target')

    if not os.path.exists(networkService_path):
        with open(networkService_path, 'w') as f:
            f.write('[Unit]\nDescription=Bluetooth NEP PAN\nAfter=pan0.network\n\n[Service]\nExecStart=/usr/bin/bt-network -s nap pan0\nType=simple\n\n[Install]\nWantedBy=multi-user.target')

    os.system('sudo systemctl start systemd-networkd')
    os.system('sudo systemctl start bt-agent')
    os.system('sudo systemctl start bt-network')

if __name__ == '__main__':
    main()
