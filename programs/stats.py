import psutil #type:ignore
import requests #type:ignore
from datetime import datetime
import socket
import shutil
from cpuinfo import get_cpu_info #type:ignore
import clr #type:ignore

def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        #print(battery.percent)
        if battery.percent<34:
            print(f"\033[31mBattery level: {battery.percent}%, Plugged in: {'Yes' if battery.power_plugged else 'No'}")
        elif battery.percent>33 and battery.percent<67:
            print(f"\033[93mBattery level: {battery.percent}%, Plugged in: {'Yes' if battery.power_plugged else 'No'}")
        elif battery.percent>67:
            print(f"\033[92mBattery level: {battery.percent}%, Plugged in: {'Yes' if battery.power_plugged else 'No'}")
        elif battery is None:
            raise ValueError("Battery information not available.")
        return f""
        
    except Exception as e:
        return f"\033[31mError retrieving battery status: {e}"

def get_current_time():
    try:
        current_time = datetime.now()
        return f"\033[0mCurrent time: \033[95m{current_time.strftime('%Y-%m-%d %H:%M:%S')}\033[0m"
    except Exception as e:
        return f"\033[31mError retrieving current time: {e}"

def get_location():
    print("getting location this can take 20 seconds if using vpn...")
    try:
        response = requests.get('https://ipinfo.io', timeout=20)
        if response.status_code != 200:
            raise ConnectionError("Unable to fetch location.")
        location_data = response.json()
        return f"Location:\033[96m {location_data.get('city', 'Unknown')}, {location_data.get('region', 'Unknown')}, {location_data.get('country', 'Unknown') }\033[0m"
    except requests.exceptions.RequestException as e:
        return f"Error retrieving location: {e}"
    except Exception as e:
        return f"Unexpected error retrieving location: {e}"

def get_ip_addresses():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        # Fetch router's (public) IP address
        response = requests.get('https://api64.ipify.org?format=json', timeout=10)
        public_ip = response.json().get("ip", "Unavailable")

        return f"Local IP Address: \033[95m{local_ip},\033[37m Public IP Address: \033[95m{public_ip}\033[37m"
    except Exception as e:
        return f"Error retrieving IP addresses: {e}"

def get_available_space():
    try:
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)  # Convert bytes to gigabytes
        return f"Available Storage: \033[33m{free_gb}\033[37m GB"
    except Exception as e:
        return f"Error retrieving storage space: {e}"

def get_cpu_info_details():
    try:
        info = get_cpu_info()
        cpu_brand = info.get('brand_raw', 'Unknown')
        cpu_architecture = info.get('arch', 'Unknown')
        cpu_hz_advertised = info.get('hz_advertised', 'Unknown')
        cpu_features = info.get('flags', [])
        
        return (
            f"CPU Brand: {cpu_brand}\n"
            f"CPU Architecture: {cpu_architecture}\n"
            f"Advertised Frequency: {cpu_hz_advertised}\n"
            f"Features: {', '.join(cpu_features)}"
        )
    except Exception as e:
        return f"Error retrieving CPU information: {e}"
    
def read_cpu_temperature():
    try:
        sensors = psutil.sensors_temperatures()
        if not sensors:
            return "Temperature sensors not available on this system."
        
        cpu_temps = sensors.get("coretemp", [])
        temperature_data = [f"Core {idx}: {temp.current}°C" for idx, temp in enumerate(cpu_temps)]
        
        return "\n".join(temperature_data) if temperature_data else "No temperature data available."
    except Exception as e:
        return f"Error retrieving CPU temperature: {e}"

def display_pc_stats():
    print("\n\033[34m=== PC Stats ======================================================\n")
    print(f"{get_battery_status()}")
    print(f"{get_current_time()}\n")
    print(f"\n{get_location()}")
    print(f"\n{get_ip_addresses()}")
    print(f"\n{get_available_space()}")
    #print(f"\nget cpu info")
    #print(f"{get_cpu_info()}")
    print("\n\033[34m===================================================================\n")
    input("\033[0mPress\033[92m Enter \033[37mto continue")

# If the file is run directly, execute the PC stats display
if __name__ == "__main__":
    display_pc_stats()
