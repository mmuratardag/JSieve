# JSieve - JavaScript Extractor & Enumerator

```bash
      ╦╔═╗ ┬┌─┐┬  ┬┌─┐
      ║╚═╗ │├┤ └┐┌┘├┤ 
     ╚╝╚═╝ ┴└─┘ └┘ └─┘
JavaScript Extractor & Enumerator v0.1
```

<div align="center">
<a href="https://python.org"><img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Python Version"/></a>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
<a href="https://github.com/mmuratardag/JSieve/issues"><img src="https://img.shields.io/github/issues/mmuratardag/JSieve" alt="GitHub Issues"/></a>
<a href="https://github.com/mmuratardag/JSieve/stargazers"><img src="https://img.shields.io/github/stars/mmuratardag/JSieve" alt="GitHub Stars"/></a>
<img src="https://img.shields.io/github/downloads/mmuratardag/JSieve/total?style=flat-square&color=green" alt="Downloads"/>
</div>


**A tool for JavaScript extraction and directory enumeration**

## 🎯 Overview

JSieve is a comprehensive web security tool designed for bug bounty hunters, penetration testers, and security researchers. It automates the process of extracting JavaScript files from web applications and provides advanced directory enumeration capabilities to discover hidden endpoints and assets.

## ✨ Features

- 🕸️ **JavaScript Extraction**: Automatically downloads external JavaScript files and extracts inline scripts
- 📁 **Directory Enumeration**: Multi-threaded directory discovery using customizable wordlists
- 🔍 **Function Detection**: Identifies JavaScript functions in inline scripts for code analysis
- 🚀 **Multi-threaded Performance**: Concurrent processing for faster enumeration
- 📊 **Progress Tracking**: Real-time progress bars and colored output
- ⚙️ **Flexible Configuration**: Customizable timeouts, delays, and thread counts
- 💾 **Organized Output**: Structured file organization with detailed results

## 🛠️ Installation

### Method 1: Recommended Installation (Modern)
```bash
git clone https://github.com/mmuratardag/JSieve.git
cd JSieve
pip install -e .
```
*This method automatically installs all dependencies and uses modern Python packaging standards.*

### Method 2: Manual Installation  
```bash
git clone https://github.com/mmuratardag/JSieve.git
cd JSieve
pip install -r requirements.txt
pip install -e .
```

### Method 3: From PyPI  (coming soon)
```bash
pip install jsieve
```

### ✅ Verify Installation
After installation, verify JSieve is working correctly:
```bash
jsieve --version
jsieve --help
```

## 🚀 Quick Start

### Basic JavaScript Extraction
```bash
jsieve https://example.com -o output_directory
```

### With Directory Enumeration
```bash
jsieve https://example.com -o js_files --directories wordlists/common.txt wordlists/directory-list-2.3-medium.txt
```

### Advanced Usage
```bash
jsieve https://target.com \
    --output ./results \
    --directories common.txt custom_dirs.txt \
    --threads 50 \
    --timeout 5 \
    --delay 0.1
```

## 📋 Usage Examples

### Example 1: Basic Extraction
```bash
$ jsieve https://example.com
      ╦╔═╗ ┬┌─┐┬  ┬┌─┐
      ║╚═╗ │├┤ └┐┌┘├┤ 
     ╚╝╚═╝ ┴└─┘ └┘ └─┘
JavaScript Extractor & Enumerator v0.1

[*] Fetching HTML from: https://example.com
[*] Parsing content to find all JavaScript...
[*] Found 3 external JavaScript file(s).
[+] Downloaded: jquery.min.js
[+] Downloaded: bootstrap.js
[+] Downloaded: app.js
[*] Found 2 inline JavaScript block(s).
[+] Process complete. All files saved in 'js_output'.
```

### Example 2: Directory Enumeration
```bash
$ jsieve https://example.com --directories wordlists/common.txt
[*] Starting Directory Enumeration with 20 threads...
[*] Loaded 4614 unique directories to check...
Scanning: 100%|████████████| 4614/4614 [02:15<00:00, 34.1dir/s]
[+] Found directory: https://example.com/admin
  [->] JS file: https://example.com/admin/admin.js
  [->] Function: validateForm
[+] Found directory: https://example.com/api
[+] Directory Enumeration Complete!
    - Directories found: 15
    - JavaScript files found: 8
    - Unique functions found: 23
```

## 📖 Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `url` | - | Target URL to crawl | Required |
| `--output` | `-o` | Output directory for downloaded files | `js_output` |
| `--directories` | - | List of wordlist files for directory enumeration | None |
| `--threads` | `-t` | Number of concurrent threads | `20` |
| `--timeout` | - | Request timeout in seconds | `3` |
| `--delay` | - | Delay between requests (seconds) | `0` |
| `--version` | `-v` | Show version information | - |

## 📂 Output Structure

JSieve organizes its output in a structured manner:

```
output_directory/
├── jquery.min.js           # External JavaScript files
├── bootstrap.js
├── app.js
├── inline_script_1.js      # Extracted inline scripts
├── inline_script_2.js
└── enumeration_results.txt # Directory enumeration results
```

### enumeration_results.txt Format
```
=== Found Directories ===
https://example.com/admin
https://example.com/api
https://example.com/backup

=== JavaScript Files ===
https://example.com/admin/admin.js
https://example.com/api/api.js

=== Functions ===
validateForm
submitData
processResponse
```

## 🗂️ Wordlists

JSieve comes with two built-in wordlists:

- **[`common.txt`](wordlists/common.txt)**: ~4,600 common directory names
- **[`directory-list-2.3-medium.txt`](wordlists/directory-list-2.3-medium.txt)**: ~220,000 directory names from DirBuster

### Using Custom Wordlists
```bash
jsieve https://example.com --directories /path/to/custom_wordlist.txt
```

## ⚡ Performance Tips

1. **Adjust Thread Count**: Increase threads for faster enumeration on stable targets.
   
   ```bash
   jsieve https://example.com --threads 50
   ```
   
2. **Add Delays**: Prevent rate limiting on sensitive targets.
   ```bash
   jsieve https://example.com --delay 0.5
   ```

3. **Optimize Timeout**: Balance between speed and reliability
   ```bash
   jsieve https://example.com --timeout 2
   ```

## 🔧 Requirements

- Python 3.6+
- requests
- beautifulsoup4
- colorama
- tqdm
- lxml

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss the changes you would like to make.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Use Cases

- **Bug Bounty Hunting**: Discover hidden JavaScript files and endpoints
- **Penetration Testing**: Enumerate web application structure
- **Security Research**: Analyze client-side code and API endpoints
- **Web Application Assessment**: Map application attack surface

## 🔒 Ethical Usage  🔃 ⚠️ Disclaimer 

JSieve is intended for authorized security testing, legitimate security research, and testing purposes only. Users are responsible for complying with applicable laws and regulations. Only test systems you own or have explicit permission to test.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [wordlists](https://www.kali.org/tools/wordlists/) for the directory wordlist
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [tqdm](https://github.com/tqdm/tqdm) for progress bars

## 📞 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/mmuratardag/JSieve/issues)
- 📚 **Documentation**: [GitHub Pages](https://mmuratardag.github.io/JSieve)
- ⭐ **Star this repo** if you find it useful!

## 👨‍💻 Contact & Links

- **JSieve Documentation**: [Project Page](https://mmuratardag.github.io/JSieve)
- **LinkedIn**: [mmuratardag](https://www.linkedin.com/in/mmuratardag)
- **Portfolio**: [mmuratardag.github.io/portfolio](https://mmuratardag.github.io/portfolio_website/portfolio.html)

## ✅ Potential  TO-DOs ❎
1. **Add User-Agent rotation** to avoid detection
2. **Export formats**: Add JSON/CSV export options for enumeration results
3. **Recursive crawling**: Option to follow links and crawl multiple pages
4. **JavaScript analysis**: Basic static analysis of downloaded scripts (looking for API keys, endpoints, etc.)
5. **Cookie/session support**: Allow authenticated scanning

---

<div align="center">
Built with ❤️ and <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"/> by <a href="https://github.com/mmuratardag">M. Murat Ardag</a>
</div>