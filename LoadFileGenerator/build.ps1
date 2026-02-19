# Build script for Windows using vcpkg

# Set error action
$ErrorActionPreference = "Stop"

Write-Host "=== Load File Generator Build Script ===" -ForegroundColor Cyan

# Check if vcpkg is installed
if (-not (Test-Path "C:\vcpkg\vcpkg.exe")) {
    Write-Host "vcpkg not found. Please install vcpkg first:" -ForegroundColor Yellow
    Write-Host "git clone https://github.com/Microsoft/vcpkg.git C:\vcpkg" -ForegroundColor Yellow
    Write-Host "C:\vcpkg\bootstrap-vcpkg.bat" -ForegroundColor Yellow
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies via vcpkg..." -ForegroundColor Green
& C:\vcpkg\vcpkg.exe install qt5-base:x64-windows podofo:x64-windows

# Create build directory
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
New-Item -ItemType Directory -Path "build" | Out-Null
Set-Location "build"

# Configure with CMake
Write-Host "Configuring with CMake..." -ForegroundColor Green
cmake .. -DCMAKE_TOOLCHAIN_FILE="C:/vcpkg/scripts/buildsystems/vcpkg.cmake" -DCMAKE_BUILD_TYPE=Release

# Build
Write-Host "Building project..." -ForegroundColor Green
cmake --build . --config Release

# Check if build succeeded
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Build Successful ===" -ForegroundColor Green
    Write-Host "Executable location: build\bin\Release\LoadFileGenerator.exe" -ForegroundColor Cyan
} else {
    Write-Host "`n=== Build Failed ===" -ForegroundColor Red
    exit 1
}

Set-Location ..
