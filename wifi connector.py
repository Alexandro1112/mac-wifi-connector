import os
import platform
import getpass

def createNewConnection(name, SSID, key):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+key+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    if platform.system() == "Windows":
        command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
        with open(name+".xml", 'w') as file:
            file.write(config)
    elif platform.system() == "Linux":
        command = "nmcli dev wifi connect '"+SSID+"' password '"+key+"'"
    os.system(command)
    if platform.system() == "Windows":
        os.remove(name+".xml")

def connect(name, SSID):
    if platform.system() == "Windows":
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli con up "+SSID
    os.system(command)

        
def displayAvailableNetworks():
    if platform.system() == "Windows":
        command = "netsh wlan show networks interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli dev wifi list"
    os.system(command)
    if platform.system == 'Darwin':
        
        """ Function output all wi-fi networks,
              which available for your devise."""
        scan_cmd = subprocess.Popen(['airport', '-s'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                     stdin=subprocess.PIPE)
        scan_out, scan_err = scan_cmd.communicate()
        scan_out_data = dict()
        scan_out_lines = str(scan_out).split("\\n")[1:-1]
        for each_line in scan_out_lines:
             split_line = [i for i in each_line.split(' ') if i != '']
             line_data = {"SSID": split_line[0], "RSSI": split_line[2], "channel": split_line[3],
                          "HT": (split_line[4] == "Y"), "CC": split_line[5], "security": split_line[6]}
             scan_out_data[split_line[1]] = line_data
        names_ = scan_out_data

        for names in names_.values():
             self.networks = list(names.values())[0]
             del networks.split()[-1]
             print(networks.split()) if not networks.strip() == '' else None
try:
    displayAvailableNetworks()
    option = input("New connection (y/N)? ")
    if option == "N" or option == "":
        name = input("Name: ")
        connect(name, name)
        print("If you aren't connected to this network, try connecting with correct credentials")
    elif option == "y":
        name = input("Name: ")
        key = getpass.getpass("Password: ")
        createNewConnection(name, name, key)
        connect(name, name)
        print("If you aren't connected to this network, try connecting with correct credentials")
except KeyboardInterrupt as e:
    print("\nExiting...")
