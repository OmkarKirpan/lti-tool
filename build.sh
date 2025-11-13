#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p configs
mkdir -p flask_session
mkdir -p keys

# Generate RSA keys if they don't exist
echo "🔑 Checking RSA keys..."
if [ ! -f "keys/private.key" ] || [ ! -f "keys/public.key" ]; then
    echo "🔐 Generating RSA key pair..."
    openssl genrsa -out keys/private.key 2048
    openssl rsa -in keys/private.key -pubout -out keys/public.key
    echo "✅ RSA keys generated successfully"
else
    echo "✅ RSA keys already exist"
fi

# Install Node.js dependencies and build TailwindCSS
echo "🎨 Installing Node.js dependencies..."
npm install

echo "🎨 Building TailwindCSS..."
npm run build

# Note: LTI config should be updated via Render dashboard or environment variables
# The config file should already exist in your repository
if [ ! -f "configs/lti_config.json" ]; then
    echo "⚠️  Warning: configs/lti_config.json not found!"
    echo "⚠️  Please ensure it exists in your repository or update it after deployment"
fi

echo "✅ Build completed successfully!"

