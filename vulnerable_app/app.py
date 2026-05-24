from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# HTML Template for the simple web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Admin Ping Tool</title></head>
<body>
    <h2>Network Administration Tool</h2>
    <p>Enter an IP address to check connectivity:</p>
    <form method="post">
        <input type="text" name="ip_address" placeholder="127.0.0.1">
        <button type="submit">Ping</button>
    </form>
    <pre>{{ output }}</pre>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        ip = request.form.get('ip_address')
        
        # VULNERABILITY: Direct User Input to System Shell
        # This is the bug we are demonstrating.
        command = f"ping -c 1 {ip}" # Linux/Mac
        # command = f"ping -n 1 {ip}" # Windows (uncomment if on Windows)
        
        # Executing the command
        output = os.popen(command).read()
        
    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
