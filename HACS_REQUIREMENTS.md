# HACS Requirements Checklist

To pass HACS validation, you need to complete these steps on your GitHub repository:

## ✅ Code Requirements (Already Done)

- [x] Integration files in `custom_components/lubelogger/`
- [x] Valid `manifest.json` with version
- [x] Valid `hacs.json` file
- [x] Config schema defined in `__init__.py`

## ⚠️ GitHub Repository Requirements

These need to be set on your GitHub repository page:

### 1. Repository Description

1. Go to your repository on GitHub
2. Click the **⚙️ Settings** gear icon (or click "Edit" next to "About")
3. Add a description, for example:
   ```
   Home Assistant integration for LubeLogger - vehicle maintenance and fuel mileage tracker
   ```
4. Click **Save changes**

### 2. Repository Topics

1. On your repository page, click the **⚙️ Settings** gear icon (or "Add topics")
2. Add these topics:
   - `home-assistant`
   - `homeassistant`
   - `hacs`
   - `integration`
   - `lubelogger`
   - `vehicle`
   - `maintenance`
3. Click **Save changes**

### 3. Repository Issues (Optional but Recommended)

- Enable Issues in repository settings if not already enabled
- This allows users to report problems

## Validation Status

After fixing the above, the HACS validation should show:

- ✅ Description check - PASS
- ✅ Topics check - PASS  
- ✅ hacs.json validation - PASS (after removing invalid keys)
- ⚠️ Brands check - This is expected to fail for new integrations (can be ignored for now)

## Notes

- The `brands` validation failure is normal for new integrations and won't prevent installation
- The `hacs.json` file has been simplified to only include required fields
- Repository description and topics must be set on GitHub, not in code files

