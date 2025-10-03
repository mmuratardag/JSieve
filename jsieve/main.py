import requests
import sys
import os
import urllib.parse
import argparse
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from colorama import Fore, Style, init
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time
import warnings
import re

# Initialize colorama
init(autoreset=True)

# Suppress XML parsing warning for HTML documents
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# ASCII Art Banner
def print_banner():
    banner = f"""{Fore.CYAN}
      ╦╔═╗ ┬┌─┐┬  ┬┌─┐
      ║╚═╗ │├┤ └┐┌┘├┤ 
     ╚╝╚═╝ ┴└─┘ └┘ └─┘
    {Fore.YELLOW}JavaScript Extractor & Enumerator v0.1
    {Fore.GREEN}https://mmuratardag.github.io/JSieve
    {Fore.BLUE}{'='*50}{Style.RESET_ALL}
    """
    print(banner)

# Lock for thread-safe console output
print_lock = Lock()

def parse_content(content, content_type=None):
    """
    Parse content with appropriate parser based on content type.
    """
    # Check if content appears to be XML
    if content_type and 'xml' in content_type.lower():
        try:
            # Try to parse as XML if lxml is available
            return BeautifulSoup(content, 'xml')
        except:
            # Fall back to HTML parser
            return BeautifulSoup(content, 'html.parser')
    else:
        # Default to HTML parser
        return BeautifulSoup(content, 'html.parser')

def check_directory(dir_url, timeout=3, delay=0):
    """
    Checks a single directory and extracts JavaScript information if found.
    Returns a tuple: (status, dir_url, js_files, functions)
    """
    if delay > 0:
        time.sleep(delay)
    
    try:
        r = requests.get(dir_url, timeout=timeout, allow_redirects=False)
        if r.status_code == 200:
            # Get content type from headers
            content_type = r.headers.get('Content-Type', '')
            soup = parse_content(r.text, content_type)
            
            js_files = []
            functions = []
            
            # Find .js files
            for script in soup.find_all("script", src=True):
                src = script.get('src')
                if src and src.endswith('.js'):
                    js_url = urllib.parse.urljoin(dir_url, src)
                    js_files.append(js_url)
            
            # Find inline JavaScript functions
            for script in soup.find_all("script", src=False):
                if script.text and "function " in script.text:
                    # Improved function name extraction
                    # Match function declarations and expressions
                    pattern = r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
                    found_functions = re.findall(pattern, script.text)
                    functions.extend(found_functions)
            
            return (True, dir_url, js_files, functions)
        else:
            return (False, dir_url, [], [])
    except requests.RequestException:
        return (False, dir_url, [], [])

def enumerate_directories(target_url, directory_files, output_dir, max_threads=20, timeout=3, delay=0):
    """
    Enumerates directories from the provided files using concurrent requests.
    """
    print(f"{Fore.CYAN}[*] Starting Directory Enumeration with {max_threads} threads...")
    
    # Load all directories from files
    directories = []
    for file in directory_files:
        try:
            with open(file, 'r') as f:
                # Remove empty lines and duplicates
                new_dirs = [line.strip() for line in f if line.strip()]
                directories.extend(new_dirs)
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Directory file not found: {file}")
            continue
    
    # Remove duplicates while preserving order
    directories = list(dict.fromkeys(directories))
    print(f"{Fore.CYAN}[*] Loaded {len(directories)} unique directories to check...")
    
    found_directories = []
    all_js_files = []
    all_functions = set()
    
    # Progress bar for overall progress
    with tqdm(total=len(directories), desc=f"{Fore.CYAN}Scanning", unit="dir") as pbar:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Submit all tasks
            future_to_dir = {}
            for directory in directories:
                dir_url = urllib.parse.urljoin(target_url, directory)
                future = executor.submit(check_directory, dir_url, timeout, delay)
                future_to_dir[future] = directory
            
            # Process completed tasks
            for future in as_completed(future_to_dir):
                directory = future_to_dir[future]
                try:
                    success, dir_url, js_files, functions = future.result()
                    
                    if success:
                        found_directories.append(dir_url)
                        all_js_files.extend(js_files)
                        all_functions.update(functions)
                        
                        # Thread-safe console output
                        with print_lock:
                            tqdm.write(f"{Fore.GREEN}[+] Found directory: {dir_url}")
                            for js_file in js_files:
                                tqdm.write(f"{Fore.YELLOW}  [->] JS file: {js_file}")
                            for func in functions:
                                tqdm.write(f"{Fore.BLUE}  [->] Function: {func}")
                    
                except Exception as e:
                    with print_lock:
                        tqdm.write(f"{Fore.RED}[!] Error checking {directory}: {e}")
                
                pbar.update(1)
    
    # Summary
    print(f"\n{Fore.GREEN}[+] Directory Enumeration Complete!")
    print(f"{Fore.CYAN}    - Directories found: {len(found_directories)}")
    print(f"{Fore.CYAN}    - JavaScript files found: {len(all_js_files)}")
    print(f"{Fore.CYAN}    - Unique functions found: {len(all_functions)}")
    
    # Optionally save results to a file
    if found_directories:
        results_file = os.path.join(output_dir, "enumeration_results.txt")
        with open(results_file, 'w') as f:
            f.write("=== Found Directories ===\n")
            for dir_url in found_directories:
                f.write(f"{dir_url}\n")
            f.write("\n=== JavaScript Files ===\n")
            for js_file in all_js_files:
                f.write(f"{js_file}\n")
            f.write("\n=== Functions ===\n")
            for func in sorted(all_functions):
                f.write(f"{func}\n")
        print(f"{Fore.GREEN}[+] Results saved to: {results_file}")

def download_js_file(url, output_dir, timeout=10):
    """
    Helper function to download a JavaScript file.
    """
    try:
        file_name = os.path.basename(urllib.parse.urlparse(url).path)
        if not file_name:
            file_name = f"script_{hash(url)}.js"
        
        save_path = os.path.join(output_dir, file_name)
        js_content = requests.get(url, timeout=timeout).text
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return True, save_path
    except Exception as e:
        return False, str(e)

def get_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Crawls a URL to download all external and extract all inline JavaScript, with an optional directory enumeration feature.",
        epilog="Example: jsieve http://example.url -o ./js_output --directories common.txt directory-list-2.3-medium.txt"
    )
    parser.add_argument("url", help="The target URL to crawl.")
    parser.add_argument(
        "-o", "--output",
        default="js_output",
        help="Directory to save the downloaded/extracted files (default: js_output)."
    )
    parser.add_argument(
        "--directories",
        nargs='+',
        help="A list of text files containing common directory names to enumerate."
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=20,
        help="Number of concurrent threads for directory enumeration (default: 20)."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=3,
        help="Request timeout in seconds for directory enumeration (default: 3)."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0,
        help="Delay between requests in seconds to avoid rate limiting (default: 0)."
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    return parser

def main():
    """Main function for JSieve."""
    try:
        # Print ASCII banner
        print_banner()
        
        parser = get_parser()
        args = parser.parse_args()
        target_url = args.url
        output_dir = args.output

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"{Fore.GREEN}[+] Created output directory: {output_dir}")

        if args.directories:
            enumerate_directories(
                target_url, 
                args.directories, 
                output_dir,
                max_threads=args.threads,
                timeout=args.timeout,
                delay=args.delay
            )

        print(f"\n{Fore.CYAN}[*] Fetching HTML from: {target_url}")
        r = requests.get(target_url, timeout=10)
        r.raise_for_status()
        
        # Get content type from headers
        content_type = r.headers.get('Content-Type', '')
        
        print(f"{Fore.CYAN}[*] Parsing content to find all JavaScript...")
        soup = parse_content(r.text, content_type)

        # --- Stage 1: Download External JavaScript Files (also using threading) ---
        external_scripts = soup.find_all('script', {"src": True})

        if external_scripts:
            print(f"{Fore.GREEN}[*] Found {len(external_scripts)} external JavaScript file(s).")
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for script in external_scripts:
                    src = script.get('src')
                    full_url = urllib.parse.urljoin(target_url, src)
                    future = executor.submit(download_js_file, full_url, output_dir)
                    futures.append((future, full_url))
                
                for future, url in tqdm(futures, desc=f"{Fore.CYAN}Downloading Scripts", unit="file"):
                    success, result = future.result()
                    if success:
                        tqdm.write(f"{Fore.GREEN}    [+] Downloaded: {os.path.basename(result)}")
                    else:
                        tqdm.write(f"{Fore.RED}    [-] Failed to download {url}: {result}")
        else:
            print(f"{Fore.YELLOW}[!] No external JavaScript files found.")

        # --- Stage 2: Extract Inline JavaScript ---
        inline_scripts = soup.find_all('script', src=False)
        # Filter out empty script tags
        inline_scripts = [tag for tag in inline_scripts if tag.string and tag.string.strip()]

        if inline_scripts:
            print(f"{Fore.GREEN}[*] Found {len(inline_scripts)} inline JavaScript block(s).")
            inline_counter = 1
            for tag in tqdm(inline_scripts, desc=f"{Fore.CYAN}Extracting Scripts", unit="block"):
                inline_code = tag.get_text(strip=True)
                file_name = f"inline_script_{inline_counter}.js"
                save_path = os.path.join(output_dir, file_name)
                try:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(inline_code)
                    inline_counter += 1
                except Exception as e:
                    tqdm.write(f"{Fore.RED}    [-] Could not save inline script {inline_counter}: {e}")
        else:
            print(f"{Fore.YELLOW}[!] No inline JavaScript blocks found.")

        print(f"\n{Fore.GREEN}[+] Process complete. All files saved in '{output_dir}'.")
        print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}\n")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[!] An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()