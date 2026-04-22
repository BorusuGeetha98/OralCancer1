import socket
import os

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def update_config():
    ip = get_ip()
    config_path = r'c:\Users\geeth\Desktop\project\ReactApp\constants\Config.js'
    
    if os.path.exists(config_path):
        with open(config_path, 'w') as f:
            content = f"// ReactApp/constants/Config.js\n"
            content += f"export const API_URL = 'http://{ip}:8000';\n"
            f.write(content)
        print(f"Successfully auto-configured Config.js to your PC IP: http://{ip}:8000")
    else:
        print("Config.js not found at path.")

if __name__ == '__main__':
    update_config()
