# web_server.py
import socket
from tests import run_all_tests

LOGFILE = "trimtab.log"

def log(msg):
    print(msg)
    try:
        with open(LOGFILE, "a") as f:
            f.write(msg + "\n")
    except:
        pass

def start_web_server(config, port_tab, starboard_tab, signalk=None):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server running on port 80")

    while True:
        cl, addr = s.accept()
        req = cl.recv(1024)
        req_str = req.decode()
        if "GET /status" in req_str:
            status = f"port:{port_tab.position:.2f},starboard:{starboard_tab.position:.2f}"
            cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n" + status.encode())
        elif "GET /run_tests" in req_str:
            run_all_tests(config, port_tab, starboard_tab, signalk, log)
            cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nTests executed. Check logs.\n")
        else:
            response = index_html(config, port_tab, starboard_tab)
            cl.send(response)
        cl.close()

def index_html(config, port_tab, starboard_tab):
    html = f"""HTTP/1.0 200 OK

<!DOCTYPE html>
<html>
<head>
    <title>Trim Tab Controller</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            margin: 0;
            padding: 10px;
        }}
        form, .status, .controls {{
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 10px auto;
        }}
        label {{
            display: block;
            margin-top: 10px;
            font-weight: bold;
        }}
        input {{
            padding: 8px;
            width: 100%;
            margin-top: 5px;
            box-sizing: border-box;
        }}
        .btn {{
            margin-top: 10px;
            padding: 10px;
            background: #007BFF;
            color: white;
            border: none;
            width: 100%;
            border-radius: 4px;
            cursor: pointer;
        }}
        .btn:hover {{
            background: #0056b3;
        }}
        .flex {{
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .btn-small {{
            flex: 1;
            padding: 8px;
        }}
    </style>
    <script>
        function updateStatus() {{
            fetch("/status").then(r => r.text()).then(t => {{
                let parts = t.split(",");
                document.getElementById("port_status").innerText = parts[0].split(":")[1];
                document.getElementById("starboard_status").innerText = parts[1].split(":")[1];
            }});
        }}
        setInterval(updateStatus, 2000);
    </script>
</head>
<body>
    <h2>Trim Tab Controller</h2>
    <form action="/config" method="POST">
        <h3>Wi-Fi Settings</h3>
        <label>SSID:</label>
        <input name="ssid" value="{config['ssid']}">
        <label>Password:</label>
        <input name="password" type="password">

        <h3>Trim Tab Settings</h3>
        <label>Travel Time (sec):</label>
        <input name="travel_time" value="{config['travel_time']}">
        <label>PWM Duty (0–65535):</label>
        <input name="pwm_duty" value="{config['pwm_duty']}">

        <h3>Signal K Settings</h3>
        <label>Host:</label>
        <input name="signalk_host" value="{config['signalk_host']}">
        <label>Port:</label>
        <input name="signalk_port" value="{config['signalk_port']}">
        <label>Token:</label>
        <input name="signalk_token" value="{config['signalk_token']}">

        <button class="btn" type="submit">Save Configuration</button>
    </form>

    <div class="controls">
        <h3>Manual Control</h3>
        <div class="flex">
            <button class="btn-small" onclick="fetch('/port/up')">Port Up</button>
            <button class="btn-small" onclick="fetch('/port/down')">Port Down</button>
            <button class="btn-small" onclick="fetch('/port/reset')">Port Reset</button>
        </div>
        <div class="flex">
            <button class="btn-small" onclick="fetch('/starboard/up')">Starboard Up</button>
            <button class="btn-small" onclick="fetch('/starboard/down')">Starboard Down</button>
            <button class="btn-small" onclick="fetch('/starboard/reset')">Starboard Reset</button>
        </div>
        <div class="flex">
            <button class="btn-small" onclick="fetch('/run_tests')">Run Self-Test</button>
        </div>
    </div>

    <div class="status">
        <h3>Status</h3>
        <p><strong>Port Position:</strong> <span id="port_status">{port_tab.position:.2f}</span></p>
        <p><strong>Starboard Position:</strong> <span id="starboard_status">{starboard_tab.position:.2f}</span></p>
        <p><strong>Access via:</strong> <a href="http://trimtab.local">http://trimtab.local</a></p>
    </div>
</body>
</html>
"""
    return html.encode()
