import requests
from colorama import init, Fore, Back, Style
import time
import sys
import random
from datetime import datetime, timedelta
import threading
import itertools
import os
import platform
import json
import hashlib
import pytz

# Initialize colorama for cross-platform colored output
init()

# Built-in license keys with expiry dates and statuses
VALID_LICENSES = {
    "BB-PRO-2024-V2A1": {
        "expiry": "2025-02-14",
        "status": "active"
    },
    "BB-PRO-2025-V2A2": {
        "expiry": "2025-05-12",
        "status": "active"
    },
    "BB-PRO-2025-V2A3": {
        "expiry": "2025-08-15",
        "status": "active"
    },
    "BB-PRO-2025-V2A4": {
        "expiry": "2025-12-25",
        "status": "active"
    }
}

def check_license():
    """Check if license is valid and not expired"""
    license_file = os.path.join(os.path.expanduser('~'), '.signal_config', 'license.json')
    
    try:
        if os.path.exists(license_file):
            with open(license_file, 'r') as f:
                saved_license = json.load(f)
                key = saved_license.get('key')
                if key in VALID_LICENSES:
                    return verify_license(key)
    except:
        pass
    
    return activate_new_license()

def activate_new_license():
    """Activate a new license key"""
    print(f"\n{Fore.CYAN}╔══════════════ 🔑 License Activation 🔑 ══════════════╗{Style.RESET_ALL}")
    key = input(f"{Fore.CYAN}║{Style.RESET_ALL} Enter License Key: ").strip()
    print(f"{Fore.CYAN}║{Style.RESET_ALL}")
    
    if key not in VALID_LICENSES:
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}❌ Invalid License Key{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}Contact @ahadhssain786 on Telegram{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
        return False
    
    # Save valid license
    license_data = {
        'key': key,
        'activated_date': datetime.now().strftime('%Y-%m-%d'),
        'expiry_date': VALID_LICENSES[key]['expiry']
    }
    
    try:
        os.makedirs(os.path.join(os.path.expanduser('~'), '.signal_config'), exist_ok=True)
        with open(os.path.join(os.path.expanduser('~'), '.signal_config', 'license.json'), 'w') as f:
            json.dump(license_data, f)
    except:
        pass
    
    return verify_license(key)

def verify_license(key):
    """Verify license expiry and show status"""
    if VALID_LICENSES[key]['status'] != 'active':
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}❌ License is not active!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}Contact @ahadhssain786 for support{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
        return False

    expiry_date = datetime.strptime(VALID_LICENSES[key]['expiry'], '%Y-%m-%d')
    current_date = datetime.now()
    
    if current_date > expiry_date:
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}❌ License Expired!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}Expired on: {VALID_LICENSES[key]['expiry']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}Contact @ahadhssain786 to renew{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
        return False
    
    days_remaining = (expiry_date - current_date).days
    
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}✅ License Activated Successfully!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}📅 Days Remaining: {days_remaining}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}🔚 Expires on: {VALID_LICENSES[key]['expiry']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    return True

def show_license_info():
    """Display current license information"""
    license_file = os.path.join(os.path.expanduser('~'), '.signal_config', 'license.json')
    try:
        if os.path.exists(license_file):
            with open(license_file, 'r') as f:
                license_data = json.load(f)
                key = license_data.get('key')
                if key in VALID_LICENSES:
                    expiry_date = datetime.strptime(VALID_LICENSES[key]['expiry'], '%Y-%m-%d')
                    current_date = datetime.now()
                    days_remaining = (expiry_date - current_date).days
                    
                    print(f"\n{Fore.CYAN}╔══════════════ License Status ══════════════╗{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}║ {Fore.WHITE}Key: {key}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}║ {Fore.WHITE}Expires: {VALID_LICENSES[key]['expiry']}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}║ {Fore.WHITE}Days Left: {days_remaining}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}╚═════════════════════════════════════════╝{Style.RESET_ALL}")
    except:
        pass

def get_termux_info():
    """Get basic system information for Termux"""
    try:
        info = {
            "OS": platform.system(),
            "Python Version": platform.python_version(),
            "Device": platform.machine(),
            "Platform": platform.platform()
        }
        return info
    except:
        return {}

def print_neon_banner():
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.RED}███████{Fore.GREEN}╗{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.CYAN}███████{Fore.WHITE}╗{Fore.RED}███{Fore.GREEN}╗  {Fore.BLUE}██{Fore.MAGENTA}╗{Fore.CYAN}█████{Fore.WHITE}╗{Fore.RED}██{Fore.GREEN}╗      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.GREEN}██╔════╝{Fore.BLUE}██{Fore.MAGENTA}║{Fore.CYAN}██╔════{Fore.WHITE}╝{Fore.RED}████{Fore.GREEN}╗ {Fore.BLUE}██{Fore.MAGENTA}║{Fore.CYAN}██╔══{Fore.WHITE}██{Fore.RED}╗{Fore.GREEN}██{Fore.BLUE}║      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.WHITE}║{Fore.RED}█████{Fore.GREEN}╗  {Fore.BLUE}██{Fore.MAGENTA}╔██{Fore.CYAN}╗{Fore.WHITE}██{Fore.RED}║{Fore.GREEN}███████{Fore.BLUE}║{Fore.MAGENTA}██{Fore.CYAN}║      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.MAGENTA}╚════██{Fore.CYAN}║{Fore.WHITE}██{Fore.RED}║{Fore.GREEN}██╔══╝  {Fore.BLUE}██{Fore.MAGENTA}║╚██{Fore.CYAN}╗██{Fore.WHITE}║{Fore.RED}██╔══██{Fore.GREEN}║{Fore.BLUE}██{Fore.MAGENTA}║      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.CYAN}███████{Fore.WHITE}║{Fore.RED}██{Fore.GREEN}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.WHITE}║ {Fore.RED}╚████{Fore.GREEN}║{Fore.BLUE}██{Fore.MAGENTA}║  {Fore.CYAN}██{Fore.WHITE}║{Fore.RED}███████{Fore.GREEN}╗║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.RED}╚══════╝{Fore.GREEN}╚═╝{Fore.BLUE}╚══════╝{Fore.MAGENTA}╚═╝{Fore.CYAN}  ╚═══╝{Fore.WHITE}╚═╝  {Fore.RED}╚═╝{Fore.GREEN}╚══════╝║{Style.RESET_ALL}
{Fore.CYAN}╠════════════════════════════════════════════════╣{Style.RESET_ALL}
{Fore.YELLOW}║     {Fore.WHITE}🌟 𝓑𝓘𝓝𝓐𝓡𝓨 𝓑𝓔𝓐𝓢𝓣 𝓟𝓡𝓞 v2.0 🌟     {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.CYAN}╚════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    return banner

def print_system_info():
    info = get_termux_info()
    if info:
        box = f"""
{Fore.CYAN}╔══════════════ 🖥️ System Info 🖥️ ══════════════╗{Style.RESET_ALL}
{Fore.YELLOW}║                                                  ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.GREEN}🔧 OS:{Fore.WHITE} {info['OS']:<37} {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.BLUE}📱 Device:{Fore.WHITE} {info['Device']:<33} {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.MAGENTA}🔋 Platform:{Fore.WHITE} {info['Platform'][:30]:<27} {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.CYAN}🐍 Python:{Fore.WHITE} {info['Python Version']:<33} {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║                                                  ║{Style.RESET_ALL}
{Fore.CYAN}╚══════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        for line in box.split('\n'):
            print(line)
            time.sleep(0.1)

def print_developer_box():
    box = f"""
{Fore.CYAN}╔══════════════ 👨‍💻 Developer Info 👨‍💻 ══════════════╗{Style.RESET_ALL}
{Fore.YELLOW}║                                                  ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.GREEN}🎨 Developer:{Fore.WHITE} ★彡 𝓗𝓪𝓭𝓲 彡★                    {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.BLUE}📱 Contact:{Fore.WHITE} 💫 @ahadhssain786 (TG) 💫     {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.MAGENTA}🌐 Version:{Fore.WHITE} 2.0 Pro                         {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.CYAN}📅 Last Update:{Fore.WHITE} 2024-02-13                    {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║                                                  ║{Style.RESET_ALL}
{Fore.CYAN}╚══════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    for line in box.split('\n'):
        print(line)
        time.sleep(0.1)

def print_tips():
    tips = [
        "💡 Tip: Save your configuration for quick access next time",
        "💡 Tip: Use the batch mode for multiple currency pairs",
        "💡 Tip: Export results to CSV for better analysis",
        "💡 Tip: Check the documentation for advanced features",
        "💡 Tip: Updated configurations provide better results",
        "💡 Tip: Keep your Termux packages updated",
        "💡 Tip: Use termux-wake-lock to prevent sleep",
        "💡 Tip: Backup your configurations regularly"
    ]
    print(f"\n{Fore.CYAN}📝 Quick Tips:{Style.RESET_ALL}")
    for tip in random.sample(tips, 2):  # Show 2 random tips
        print(f"{Fore.YELLOW}{tip}{Style.RESET_ALL}")

def animated_progress_bar(duration):
    width = 40  # Reduced width for better mobile display
    animation = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    
    start_time = time.time()
    while (time.time() - start_time) < duration:
        for i, char in enumerate(animation):
            color = colors[i % len(colors)]
            progress = int(((time.time() - start_time) / duration) * width)
            bar = '█' * progress + '░' * (width - progress)
            percentage = int((progress / width) * 100)
            sys.stdout.write(f'\r{color}Processing {char} [{bar}] {percentage}%{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.1)
    print()

def get_input(prompt, default=""):
    print(f"{Fore.CYAN}╭──────────────────────────────╮{Style.RESET_ALL}")
    value = input(f"{Fore.CYAN}│ {Fore.GREEN}💎 {prompt}{Style.RESET_ALL}: ").strip() or default
    print(f"{Fore.CYAN}╰──────────────────────────────╯{Style.RESET_ALL}")
    return value

def save_configuration(params):
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.signal_config')
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, 'signal_config.json')
        
        with open(config_file, 'w') as f:
            json.dump(params, f, indent=4)
        print(f"{Fore.GREEN}✅ Configuration saved successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error saving configuration: {str(e)}{Style.RESET_ALL}")

def load_configuration():
    try:
        config_file = os.path.join(os.path.expanduser('~'), '.signal_config', 'signal_config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def generate_signal_animation():
    frames = [
        "⚡ 🔮 Generating Signal 🔮 ⚡",
        "🔄 📊 Processing Data 📊 🔄",
        "📈 💫 Analyzing Markets 💫 📈",
        "🌟 ✨ Creating Magic ✨ 🌟"
    ]
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN]
    
    for _ in range(3):
        for i, frame in enumerate(frames):
            sys.stdout.write(f'\r{colors[i % len(colors)]}{frame}{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.4)
    print()

def export_results(data, filename=None):
    try:
        if filename is None:
            filename = f"signal_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        storage_dir = os.path.expanduser('~/storage/downloads')
        if os.path.exists(storage_dir):
            filename = os.path.join(storage_dir, filename)
        
        with open(filename, 'w') as f:
            if isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"{key},{value}\n")
            elif isinstance(data, str):
                f.write(data)
        print(f"{Fore.GREEN}✅ Results exported to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error exporting results: {str(e)}{Style.RESET_ALL}")

def print_startup_message():
    messages = [
        "🚀 Initializing Binary Beast Pro...",
        "🔍 Checking system resources...",
        "📡 Establishing market connection...",
        "⚡ Loading signal algorithms..."
    ]
    for msg in messages:
        print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
        time.sleep(0.5)

def gather_params():
    print(f"\n{Fore.YELLOW}🎮 Configure Signal Parameters 🎮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'═' * 40}{Style.RESET_ALL}")
    
    saved_config = load_configuration()
    if saved_config:
        use_saved = input(f"{Fore.CYAN}Found saved configuration. Use it? (y/n):{Style.RESET_ALL} ").lower() == 'y'
        if use_saved:
            return saved_config, {'User-Agent': 'Mozilla/5.0'}

    params = {
        'start_time': get_input("⏰ Start time (e.g., 09:00)", "09:00"),
        'end_time': get_input("⌛ End time (e.g., 18:00)", "18:00"),
        'days': get_input("📅 Trading days", "5"),
        'pairs': get_input("💱 Currency pairs (comma-separated)"),
        'mode': get_input("🔄 Mode (blackout/normal)", "normal"),
        'min_percentage': get_input("📊 Minimum percentage", "50"),
        'filter': get_input("🔍 Filter value", "1"),
        'separate': get_input("📋 Separate", "1")
    }

    if input(f"\n{Fore.CYAN}Save this configuration for future use? (y/n):{Style.RESET_ALL} ").lower() == 'y':
        save_configuration(params)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.0.0 Mobile Safari/537.36'
    }
    
    return params, headers

def send_request():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Startup sequence
    print_startup_message()
    
    # Print banner and info boxes
    print(print_neon_banner())
    time.sleep(0.5)
    print_system_info()
    time.sleep(0.5)
    print_developer_box()
    print_tips()
    
    url = "https://alltradingapi.com/signal_list_gen/qx_signal.js"
    
    try:
        params, headers = gather_params()
        
        print(f"\n{Fore.YELLOW}🚀 Initializing Signal Generation 🚀{Style.RESET_ALL}")
        generate_signal_animation()
        animated_progress_bar(3)
        
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            print(f"\n{Fore.GREEN}{'═' * 50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}✨ Signal Generated Successfully! ✨{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'═' * 50}{Style.RESET_ALL}")
            
            try:
                data = response.json()
                print_signal_result(data)
                
                if input(f"\n{Fore.CYAN}Export results to CSV? (y/n):{Style.RESET_ALL} ").lower() == 'y':
                    filename = get_input("📁 Enter filename (default: signal_results.csv)", "signal_results.csv")
                    export_results(data, filename)
                    
            except ValueError:
                print(f"\n{Fore.YELLOW}⚠️ Response Format:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{response.text}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ Generation Failed (Code: {response.status_code}){Style.RESET_ALL}")
            print(f"{Fore.RED}Error: {response.text}{Style.RESET_ALL}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n{Fore.RED}❌ Connection Error: Could not connect to the server{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please check your internet connection and try again{Style.RESET_ALL}")
    except requests.exceptions.Timeout:
        print(f"\n{Fore.RED}❌ Timeout Error: The request timed out{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}The server is taking too long to respond{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"\n{Fore.RED}❌ Request Error: {str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
    
    finally:
        print(f"\n{Fore.MAGENTA}{'═' * 50}{Style.RESET_ALL}")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Fore.CYAN}🕒 Generated at: {current_time}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'═' * 50}{Style.RESET_ALL}")
        
        if input(f"\n{Fore.CYAN}Generate another signal? (y/n):{Style.RESET_ALL} ").lower() == 'y':
            send_request()
        else:
            print(f"\n{Fore.GREEN}👋 Thank you for using Binary Beast Pro! Goodbye!{Style.RESET_ALL}")

def main():
    try:
        # Create necessary directories
        os.makedirs(os.path.join(os.path.expanduser('~'), '.signal_config'), exist_ok=True)
        os.makedirs(os.path.join(os.path.expanduser('~'), 'storage/downloads'), exist_ok=True)
        
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print banner
        print(print_neon_banner())
        time.sleep(0.5)
        
        # Show current license info if exists
        show_license_info()
        
        # Check license before proceeding
        if not check_license():
            print(f"\n{Fore.RED}❌ Please activate a valid license to use Binary Beast Pro{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📱 Contact @ahadhssain786 on Telegram for license purchase{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.GREEN}✨ Welcome to Binary Beast Pro!{Style.RESET_ALL}")
        time.sleep(1)
        send_request()
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️ Program terminated by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {str(e)}{Style.RESET_ALL}")
    finally:
        print(f"\n{Fore.GREEN}👋 Thank you for using Binary Beast Pro!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
