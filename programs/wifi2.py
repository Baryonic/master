import subprocess
import re

def scan_wifi_netsh():
    """Uses Windows netsh command to list available WiFi networks."""
    try:
        result = subprocess.run(["netsh", "wlan", "show", "network"], capture_output=True, text=True)
        networks = re.findall(r"SSID\s+\d+\s+:\s+(.+)", result.stdout)  # Extract SSIDs
        
        if not networks:
            raise Exception("No WiFi networks found.")
        
        print("\nAvailable WiFi Networks:")
        for idx, network in enumerate(networks, start=1):
            print(f"{idx}. {network}")
        
        return networks
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def connect_wifi_netsh(ssid, password):
    """Attempts to connect to WiFi using netsh command."""
    try:
        profile_content = f"""
            <?xml version="1.0"?>
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                <name>{ssid}</name>
                <SSIDConfig>
                    <SSID>
                        <name>{ssid}</name>
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
                            <keyMaterial>{password}</keyMaterial>
                        </sharedKey>
                    </security>
                </MSM>
            </WLANProfile>
        """
        
        with open(f"{ssid}.xml", "w") as file:
            file.write(profile_content)

        # Add the WiFi profile
        subprocess.run(["netsh", "wlan", "add", "profile", f"filename={ssid}.xml"], capture_output=True)

        # Connect to the WiFi network
        result = subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], capture_output=True, text=True)
        
        if "Connection request was completed successfully" in result.stdout:
            print(f"Successfully connected to {ssid}!")
        else:
            raise Exception("Failed to connect. Check the password or network availability.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        networks = scan_wifi_netsh()
        if networks:
            ssid = input("\nEnter the SSID of the network you want to connect to: ")
            password = input("Enter the WiFi password: ")
            connect_wifi_netsh(ssid, password)
    
    except Exception as e:
        print(f"Error: {e}")
