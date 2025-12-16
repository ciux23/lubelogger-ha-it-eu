# Troubleshooting Guide

## Integration Not Appearing in Search

If the integration downloads successfully in HACS but doesn't appear when searching in Home Assistant, follow these steps:

### Step 1: Check Home Assistant Logs

1. Go to **Settings** → **System** → **Logs**
2. Look for errors related to "lubelogger" or "custom_components"
3. Common errors to look for:
   - Import errors
   - Missing dependencies
   - Syntax errors

### Step 2: Verify File Structure

Check that all files are in the correct location:

```
/config/custom_components/lubelogger/
  ├── __init__.py
  ├── client.py
  ├── config_flow.py
  ├── const.py
  ├── coordinator.py
  ├── manifest.json
  ├── sensor.py
  └── strings.json
```

### Step 3: Check File Permissions

Ensure files are readable:

```bash
# SSH into your Home Assistant instance
chmod -R 644 /config/custom_components/lubelogger/*
chmod 755 /config/custom_components/lubelogger
```

### Step 4: Verify Dependencies

Check if `aiohttp` is installed:

1. Go to **Settings** → **Add-ons** → **SSH & Web Terminal** (or use your terminal)
2. Run: `pip list | grep aiohttp`
3. If not installed, the integration should install it automatically, but you can manually install:
   ```bash
   pip install aiohttp
   ```

### Step 5: Clear Home Assistant Cache

1. Go to **Developer Tools** → **YAML**
2. Click **Check Configuration**
3. If there are errors, fix them
4. Restart Home Assistant

### Step 6: Check Integration Discovery

1. Go to **Developer Tools** → **Services**
2. Search for `config_entries.reload`
3. Try reloading the config entries

### Step 7: Manual Verification

Check if the integration is loaded:

1. Go to **Developer Tools** → **States**
2. Search for `lubelogger` - you shouldn't see anything yet, but this confirms the domain is recognized
3. Check **Settings** → **Devices & Services** → **Integrations** for any error messages

### Step 8: Test Import

Test if the integration can be imported:

1. SSH into Home Assistant
2. Activate the Home Assistant Python environment
3. Run:
   ```python
   python3 -c "import sys; sys.path.insert(0, '/config/custom_components'); from lubelogger import DOMAIN; print('Import successful:', DOMAIN)"
   ```

### Step 9: Check Manifest.json

Verify `manifest.json` is valid JSON:

```bash
python3 -m json.tool /config/custom_components/lubelogger/manifest.json
```

### Step 10: Full Restart

If all else fails:

1. **Stop** Home Assistant completely
2. **Wait 30 seconds**
3. **Start** Home Assistant again
4. Wait for full startup (check logs)
5. Try adding the integration again

## Common Error Messages

### "Integration not found"

- **Cause**: Integration files not in correct location or import errors
- **Solution**: Verify file structure and check logs for import errors

### "Invalid config"

- **Cause**: Syntax error in Python files or invalid manifest.json
- **Solution**: Check logs for specific error, validate JSON syntax

### "Dependencies not installed"

- **Cause**: `aiohttp` not available
- **Solution**: Restart Home Assistant (it should auto-install), or manually install via pip

### Integration appears but connection fails

- **Cause**: Network connectivity or API endpoint issues
- **Solution**: Verify LubeLogger URL is accessible, check API endpoints match your instance

## Getting More Help

1. **Check Logs**: Always check the full Home Assistant logs for detailed error messages
2. **Enable Debug Logging**: Add to `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.lubelogger: debug
   ```
3. **GitHub Issues**: Open an issue with:
   - Home Assistant version
   - Integration version
   - Full error logs
   - Steps to reproduce

