import subprocess

def secure_ping(ip_address):
    # DEFENSE: Input Validation
    # We only allow numbers and dots. No special characters like ; | &
    if not ip_address.replace('.', '').isdigit():
        return "Error: Invalid IP format."

    # DEFENSE: Using subprocess without shell=True
    # This prevents command injection entirely
    try:
        # On Linux/Mac
        result = subprocess.run(['ping', '-c', '1', ip_address], 
                                capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)
