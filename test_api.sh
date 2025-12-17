#!/bin/bash
# Test script to check LubeLogger API

URL="http://10.0.0.61:8447"
USERNAME="larry"
PASSWORD="gkYtUYYdqwuN2R2i9JEr"

echo "Testing LubeLogger API connection..."
echo ""

echo "1. Testing /api/Vehicle/GetAllVehicles"
curl -v -u "$USERNAME:$PASSWORD" "$URL/api/Vehicle/GetAllVehicles" 2>&1 | head -30
echo ""
echo ""

echo "2. Testing /api/Vehicle"
curl -v -u "$USERNAME:$PASSWORD" "$URL/api/Vehicle" 2>&1 | head -30
echo ""
echo ""

echo "3. Testing root /api"
curl -v -u "$USERNAME:$PASSWORD" "$URL/api" 2>&1 | head -30

