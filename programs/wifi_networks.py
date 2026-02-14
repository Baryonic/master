from pywifi import PyWiFi, const, Profile
import time

def list_interfaces():
    """Lists available WiFi interfaces and lets user choose one."""
    wifi = PyWiFi()
    ifaces = wifi.interfaces()
    
    if not ifaces:
        raise Exception("No WiFi interfaces found!")
    
    print("\nAvailable Network Interfaces:")
    for idx, iface in enumerate(ifaces, start=1):
        print(f"{idx}. {iface.name()}")
    
    while True:
        try:
            choice = int(input("\nSelect the interface number: "))
            if 1 <= choice <= len(ifaces):
                return ifaces[choice - 1]
            else:
                print("Invalid selection. Choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def scan_wifi(iface):
    
    """Scans and returns available WiFi networks using the chosen interface."""
    try:
        iface.scan()
        time.sleep(3)  # Wait for scan results
        networks = iface.scan_results()
        
        if not networks:
            raise Exception("No networks found.")
        
        print("\nAvailable WiFi Networks:")
        for idx, network in enumerate(networks, start=1):
            print(f"{idx}. {network.ssid}")
        return networks
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def connect_wifi(iface, ssid, password):
    """Attempts to connect to the specified WiFi network."""
    try:
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        
        iface.remove_all_network_profiles()
        profile = iface.add_network_profile(profile)
        
        iface.connect(profile)
        time.sleep(5)  # Wait for connection
        
        if iface.status() == const.IFACE_CONNECTED:
            print(f"Successfully connected to {ssid}!")
        else:
            raise Exception("Failed to connect. Check your password or network availability.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        iface = list_interfaces()
        wifi = PyWiFi()
        iface = wifi.interfaces()[0]  # Select the first interface

        print(f"Interface: {iface.name()}")
        print(f"Status Code: {iface.status()}")  # Check status

        status_dict = {
            const.IFACE_DISCONNECTED: "Disconnected",
            const.IFACE_SCANNING: "Scanning",
            const.IFACE_INACTIVE: "Inactive",
            const.IFACE_CONNECTED: "Connected"
        }

        print(f"Translated Status: {status_dict.get(iface.status(), 'Unknown Status')}")

        if iface.status() == const.IFACE_DISCONNECTED:
            print("WiFi adapter is enabled.")
        else:
            raise Exception("No WiFi adapter found or disabled.")
        
        networks = scan_wifi(iface)
        if networks:
            ssid = input("\nEnter the SSID of the network you want to connect to: ")
            password = input("Enter the WiFi password: ")
            connect_wifi(iface, ssid, password)
    
    except Exception as e:
        print(f"Error: {e}")
