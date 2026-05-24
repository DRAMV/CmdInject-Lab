# 🛡️ CmdInject-Lab

A safe, local **Vulnerability Lab** designed to demonstrate **OS Command Injection**. This project provides a holistic view of a vulnerability lifecycle: **Deployment (Dev), Exploitation (Red Team), and Remediation (Blue Team).**

---

## ⚠️ Disclaimer
**This application is vulnerable by design.**  
Do **not** deploy this application to a public web server or expose it to the internet. It is intended solely for educational purposes, Capture The Flag (CTF) practice, and local security testing.

---

## 🎯 Project Objectives

This lab is designed to teach three distinct cybersecurity disciplines:

1. **Development:** Understanding how insecure coding practices (like direct string concatenation) lead to vulnerabilities.
2. **Offensive Security:** Learning how to identify and exploit Command Injection flaws using automated scripts.
3. **Defensive Security:** Implementing input validation and secure API calls to neutralize the threat.

---

## 📂 Project Structure

```text
CmdInject-Lab/
│
├── vulnerable_app/              # The intentionally vulnerable Flask application
│   ├── app.py                   # Main application logic
│   └── requirements.txt         # Python dependencies
│
├── exploit_scripts/             # Automated Red Team tools
│   └── auto_exploit.py          # Script to weaponize the vulnerability
│
├── defense_artifacts/           # Blue Team remediation code
│   └── secure_code_example.py   # Patched and secure logic
│
└── README.md                    # You are here
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed
- `pip` (Python package installer)

### 1. Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/CmdInject-Lab.git
cd CmdInject-Lab
```

Install the required dependencies for the web application:

```bash
cd vulnerable_app
pip install -r requirements.txt
```

### 2. Running the Vulnerable App

Start the Flask server:

```bash
python app.py
```

The application will be running locally at: `http://127.0.0.1:5000`

---

## 💣 Phase 1: The Exploit (Red Team)

With the server running, we can simulate an attack. The application takes an IP address to "ping," but fails to sanitize the input.

### Manual Exploitation

1. Open the web interface at `http://127.0.0.1:5000`.
2. In the input box, enter: `127.0.0.1; whoami`
3. Submit the form.
4. **Result:** The server executes `ping 127.0.0.1` followed by `whoami`. You will see the server's username in the output (e.g., `root` or your user profile).

### Automated Exploitation

A script is provided to automate this process.

1. Open a new terminal window.
2. Install the requests library if needed: `pip install requests`
3. Run the exploit script from the project root:

```bash
cd exploit_scripts
python auto_exploit.py id
```

**Expected Output:**  
The script will inject the payload and return the output of the `id` command (or `whoami` on Windows), proving Remote Code Execution (RCE).

---

## 🛡️ Phase 2: The Defense (Blue Team)

The vulnerability exists in `vulnerable_app/app.py` at this line:

```python
# VULNERABLE CODE
command = f"ping -c 1 {ip}"
output = os.popen(command).read()
```

### Remediation Strategy

To fix this, we must:
1. **Validate Input:** Ensure the input is a valid IP address and contains no special characters.
2. **Use Secure Libraries:** Avoid `os.popen` or `shell=True`.

### The Fix

See `defense_artifacts/secure_code_example.py` for the corrected implementation:

```python
import subprocess
import re

def secure_ping(ip_address):
    # 1. Input Validation: Strict regex for IPv4
    # Only allows numbers and dots. Rejects ';', '&', '|', etc.
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address):
        return "Error: Invalid IP address format."

    # 2. Secure Execution: Use subprocess without shell=True
    # Arguments are passed as a list, preventing command chaining
    try:
        result = subprocess.run(
            ['ping', '-c', '1', ip_address],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Execution Error: {e}"
```

---

## 🔧 Technologies Used

| Category | Tools |
|---|---|
| Backend | Python, Flask |
| Networking | HTTP, Sockets |
| Security Concepts | OS Command Injection, Input Sanitization, Subprocess Security |

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
