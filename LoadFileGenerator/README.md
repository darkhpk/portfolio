# Load File Generator

A high-performance C++ application for generating DAT and OPT load files from PDF documents with metadata. Built with Qt6 and optimized for processing large document sets efficiently.

## Features

- **Professional Qt GUI**: Modern, intuitive interface with progress tracking
- **Fast PDF Processing**: Multi-threaded page counting using PoDoFo library
- **CSV Metadata Import**: Parse and map metadata from CSV files to documents
- **DAT File Generation**: Industry-standard Concordance format with delimiters
- **OPT File Generation**: Image reference files for document management systems
- **Volume Management**: Automatically organize documents into configurable volumes
- **Bates Numbering**: Sequential numbering with customizable start values
- **Folder Structure**: Professional output organization (IMAGES, NATIVES, TEXT)

## Requirements

### Build Dependencies

- **CMake** 3.16 or higher
- **Qt5** (Core, Gui, Widgets)
- **PoDoFo** 0.9.x or higher (PDF processing library)
- **C++17** compatible compiler
  - MSVC 2019+ (Windows)
  - GCC 8+ (Linux)
  - Clang 7+ (macOS)

### Installing Dependencies on Windows

#### Using vcpkg (Recommended)

```powershell
# Install vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# Install Qt5
.\vcpkg install qt5-base:x64-windows

# Install PoDoFo
.\vcpkg install podofo:x64-windows

# Integrate with Visual Studio
.\vcpkg integrate install
```

#### Using Qt Installer

1. Download Qt Online Installer from https://www.qt.io/download
2. Install Qt5.x with MSVC 2019 component
3. Add Qt to PATH: `C:\Qt\5.x.x\msvc2019_64\bin`

## Building the Application

### Windows (Visual Studio)

```powershell
# Create build directory
mkdir build
cd build

# Configure with CMake
cmake .. -DCMAKE_TOOLCHAIN_FILE="C:/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake"

# Build
cmake --build . --config Release

# Executable will be in build/bin/Release/LoadFileGenerator.exe
```

### Alternative Build (Qt Creator)

1. Open `CMakeLists.txt` in Qt Creator
2. Configure project with Qt5 kit
3. Build → Build Project
4. Run the application

## Usage

### Step-by-Step Guide

1. **Load PDF Files**
   - Click "Browse PDF Folder"
   - Select folder containing PDF documents
   - Files will appear in the list

2. **Import Metadata CSV**
   - Click "Browse CSV"
   - Select CSV file with document metadata
   - CSV should have headers matching field names
   - Optional: Include "FileName" column to match PDFs

3. **Configure Output Settings**
   - Click "Browse Output" to select destination folder
   - Set "Start Bates Number" (default: 1)
   - Set "Documents Per Volume" (default: 1000)

4. **Generate Load Files**
   - Click "Generate Load Files"
   - Monitor progress in the log window
   - Output files will be created:
     - `loadfile.dat` - Metadata database file
     - `loadfile.opt` - Image reference file
     - `VOL001/`, `VOL002/`, etc. - Volume folders

### CSV Metadata Format

Example CSV structure:

```csv
FileName,Author,DateCreated,Subject,DocType
document1.pdf,John Doe,2024-01-15,Contract,Legal
document2.pdf,Jane Smith,2024-01-16,Email,Communication
```

### Output Structure

```
OutputFolder/
├── loadfile.dat
├── loadfile.opt
├── VOL001/
│   ├── IMAGES/
│   ├── NATIVES/
│   └── TEXT/
├── VOL002/
│   ├── IMAGES/
│   ├── NATIVES/
│   └── TEXT/
...
```

## DAT File Format

- Delimiter: ASCII 20 (0x14)
- Text Qualifier: ASCII 254 (0xFE)
- Encoding: UTF-8
- Fields: DOCID, BEGBATES, ENDBATES, PGCOUNT, VOLUME, [metadata fields]

## OPT File Format

Each line represents one page:
```
VOL001/IMAGES/DOC000001_0001.tif,Y,,,0000001
VOL001/IMAGES/DOC000001_0002.tif,Y,,,0000002
```

Format: `ImagePath,DocumentBreak,FolderBreak,BoxBreak,PageID`

## Performance

- **Multi-threaded**: Uses all available CPU cores for PDF processing
- **Memory efficient**: Streams large CSV files
- **Scalable**: Tested with 100,000+ documents
- **Fast**: ~1000 PDFs/minute on modern hardware (varies by PDF complexity)

## Troubleshooting

### Build Issues

**Qt5 not found:**
```powershell
cmake .. -DCMAKE_PREFIX_PATH="C:/Qt/5.x.x/msvc2019_64"
```

**PoDoFo not found:**
```powershell
# Make sure vcpkg integration is enabled
vcpkg integrate install
```

### Runtime Issues

**DLL not found:**
- Ensure Qt5 DLLs are in PATH or same folder as .exe
- Copy from: `C:\Qt\5.x.x\msvc2019_64\bin\`

**PDF processing errors:**
- Check PDF files are not corrupted
- Ensure read permissions on PDF folder

## License

This project is provided as-is for document management purposes.

## Support

For issues or questions, refer to the log output in the application for detailed error messages.

## Version History

- **1.0.0** - Initial release
  - Qt5 GUI
  - Multi-threaded PDF processing
  - DAT/OPT generation
  - Volume management
  - CSV metadata support
