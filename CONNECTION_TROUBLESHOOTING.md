# Connection Troubleshooting Guide

## "Cannot Connect" Error

If you're getting a "cannot_connect" error when setting up the integration, try these steps:

### 1. Verify LubeLogger is Accessible

Test if your LubeLogger instance is reachable from your Home Assistant server:

```bash
# From Home Assistant (SSH or terminal)
curl -I http://your-lubelogger-url:port
# or
curl -I https://your-lubelogger-url
```

### 2. Check URL Format

The URL should be in one of these formats:
- `http://192.168.1.100:5000`
- `https://lubelogger.example.com`
- `http://localhost:5000` (if on same machine)

**Important**: 
- Include the protocol (`http://` or `https://`)
- Include the port number if not using standard ports (80 for HTTP, 443 for HTTPS)

### 3. Check Network Connectivity

If LubeLogger is on a different machine:

1. **Same network**: Ensure both devices are on the same network
2. **Firewall**: Check if firewall is blocking the connection
3. **Docker/Container**: If LubeLogger is in Docker, ensure ports are properly exposed

### 4. Test API Endpoint Manually

Try accessing the API endpoint directly:

```bash
# Replace with your actual URL, username, and password
curl -u username:password http://your-lubelogger-url/api/Vehicle/GetAllVehicles
```

If this works, the integration should work too.

### 5. Check Home Assistant Logs

Enable debug logging to see detailed connection errors:

1. Add to `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.lubelogger: debug
   ```

2. Restart Home Assistant

3. Try adding the integration again

4. Check logs:
   ```bash
   ha core logs | grep -i lube
   ```

Look for specific error messages that will help identify the issue.

### 6. Common Issues

#### SSL/Self-Signed Certificates
If using HTTPS with a self-signed certificate, the integration should handle this, but you can verify:
- The integration sets `ssl=False` to allow self-signed certificates
- If still having issues, try HTTP instead of HTTPS for testing

#### Wrong API Endpoint
The integration tries multiple endpoint paths:
- `/api/Vehicle/GetAllVehicles`
- `/api/Vehicle`
- `/api/vehicles`
- `/Vehicle/GetAllVehicles`

If your LubeLogger uses a different endpoint, you may need to adjust the code.

#### Authentication Issues
- Verify username and password are correct
- Check if LubeLogger requires different authentication (API key, token, etc.)
- Some LubeLogger instances might use different auth methods

### 7. Test from Home Assistant

You can test the connection from Home Assistant's Python environment:

```python
# In Home Assistant Developer Tools → Template
# Or via SSH/terminal in Home Assistant
import aiohttp
import asyncio

async def test():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://your-url/api/Vehicle/GetAllVehicles",
            auth=aiohttp.BasicAuth("username", "password"),
            timeout=aiohttp.ClientTimeout(total=10),
            ssl=False
        ) as response:
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

asyncio.run(test())
```

### 8. Check LubeLogger Configuration

Verify your LubeLogger instance:
- Is running and accessible
- Has API enabled (if there's a setting for that)
- Allows connections from your Home Assistant IP
- Is not behind a reverse proxy that might be blocking requests

### 9. Alternative: Check Actual API Structure

If you have access to LubeLogger's source code or documentation, verify:
- The actual API endpoint paths
- Required authentication method
- Any required headers

You might need to adjust the endpoints in `custom_components/lubelogger/const.py` if they differ.

## Getting More Help

If none of these work:

1. **Check the logs** with debug logging enabled
2. **Share the error details** from the logs
3. **Verify the LubeLogger API** is working by testing with curl or a browser
4. **Check LubeLogger documentation** for API details

The most common issues are:
- Incorrect URL format (missing http:// or port)
- Network/firewall blocking connection
- Wrong API endpoint path
- Authentication method mismatch

