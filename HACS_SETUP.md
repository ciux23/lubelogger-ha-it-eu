# HACS Setup Guide

## Fixing the "version cannot be used with HACS" Error

The error you're seeing means HACS is trying to use a commit hash as a version. Here's how to fix it:

### Step 1: Push to GitHub

If you haven't already, push this repository to GitHub:

```bash
git init
git add .
git commit -m "Initial commit: LubeLogger Home Assistant integration"
git branch -M main
git remote add origin https://github.com/larry/lubelogger-ha.git
git push -u origin main
```

### Step 2: Create a Release/Tag

HACS needs a proper release to determine the version. Create a release:

1. Go to your GitHub repository
2. Click **Releases** → **Create a new release**
3. Tag version: `v1.0.0`
4. Release title: `v1.0.0`
5. Description: `Initial release of LubeLogger Home Assistant integration`
6. Click **Publish release**

Or use the command line:

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

### Step 3: Verify HACS Files

Make sure these files exist in your repository root:

- ✅ `hacs.json` (not `.hacs.json`)
- ✅ `custom_components/lubelogger/manifest.json` (without version field)
- ✅ `README.md`

### Step 4: Add to HACS

1. In Home Assistant, go to **HACS** → **Integrations**
2. Click the three dots menu (⋮) → **Custom repositories**
3. Add:
   - **Repository**: `https://github.com/larry/lubelogger-ha`
   - **Category**: Integration
4. Click **Add**
5. Search for "LubeLogger" in HACS
6. Click **Download**
7. Restart Home Assistant

### Step 5: Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ ADD INTEGRATION"**
3. Search for **"LubeLogger"**
4. Enter your LubeLogger details

## Important Notes

- **Version Management**: HACS manages versions through GitHub releases/tags. Don't include a `version` field in `manifest.json` for HACS-managed integrations.
- **Updates**: When you want to release an update, create a new GitHub release with a new version tag (e.g., `v1.0.1`).
- **hacs.json**: This file tells HACS about your integration. It must be in the repository root.

## Troubleshooting

### Still Getting Version Error

1. **Clear HACS cache**: 
   - Go to **HACS** → **Settings** → **Clear HACS cache**
   - Restart Home Assistant

2. **Check repository structure**:
   - Ensure `hacs.json` is in the root (not in a subdirectory)
   - Ensure `custom_components/lubelogger/` exists with all files

3. **Verify release exists**:
   - Check your GitHub repository → **Releases** tab
   - At least one release should exist

4. **Check HACS logs**:
   - Go to **Settings** → **System** → **Logs**
   - Filter for "hacs" to see detailed error messages

### Integration Not Appearing in HACS

1. Make sure the repository is public (or you have proper access)
2. Verify the repository URL is correct
3. Check that `hacs.json` is valid JSON
4. Ensure the integration follows Home Assistant integration structure

