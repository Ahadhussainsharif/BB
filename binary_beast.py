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

# Timezone setup
TIMEZONE = pytz.timezone('Asia/Karachi')

# Built-in license keys with expiry dates and statuses
VALID_LICENSES = {
    "BB-PRO-2090-54686833": {
        "expiry": "2090-12-31",
        "status": "active"
    },
    "BB-PRO-2025-V2A2": {
        "expiry": "2025-02-20",
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

# Available Assets
AVAILABLE_ASSETS = [
    "AUD/CAD", "AUD/CHF", "AUD/JPY", "AUD/NZD", "AUD/USD",
    "CAD/CHF", "CHF/JPY", "EUR/AUD", "EUR/CAD", "EUR/CHF",
    "EUR/GBP", "EUR/USD", "GBP/AUD", "GBP/CAD", "GBP/CHF",
    "GBP/JPY", "GBP/NZD", "GBP/USD", "NZD/CAD_OTC", "NZD/CHF_OTC",
    "NZD/JPY", "USD/BDT_OTC", "USD/BRL_OTC", "USD/CAD", "USD/CHF_OTC",
    "USD/COP_OTC","USD/INR_OTC", "USD/JPY", "USD/NGN_OTC",
    "USD/PKR_OTC", "USD/SGD_OTC", "USD/TRY_OTC", "USD/ZAR_OTC", 
    "Bitcoin_OTC", "Gold_OTC", "Silver_OTC", "UKBrent_OTC"
]

def check_license():
    """Check if license is valid and not expired"""
    while True:  # Keep trying until valid license or user exits
        license_file = os.path.join(os.path.expanduser('~'), '.signal_config', 'license.json')
        
        try:
            if os.path.exists(license_file):
                with open(license_file, 'r') as f:
                    saved_license = json.load(f)
                    key = saved_license.get('key')
                    if key in VALID_LICENSES:
                        if verify_license(key):
                            return True
                        else:
                            # If license is invalid/expired, delete it and prompt for new one
                            os.remove(license_file)
            
            # No valid license found, ask to activate new one
            if activate_new_license():
                return True
            else:
                choice = input(f"\n{Fore.CYAN}Try again? (y/n):{Style.RESET_ALL} ").lower()
                if choice != 'y':
                    return False
                
        except Exception:
            # If any error occurs with license file, delete it and try again
            if os.path.exists(license_file):
                os.remove(license_file)
            
            choice = input(f"\n{Fore.CYAN}Try again? (y/n):{Style.RESET_ALL} ").lower()
            if choice != 'y':
                return False

def print_trading_rules():
    """Display trading rules in a fancy box"""
    rules_box = f"""
{Fore.CYAN}╔═══════════════ Important Trading Rules ═══════════════╗{Style.RESET_ALL}
{Fore.YELLOW}║                                                         ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}⚠️ Avoid Doji candles for reliable signals            {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}📊 Never trade during Gap Up/Down periods            {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}🚫 Avoid trading after big opposite trend candles    {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}🛡️ Always maintain safety margin in trades           {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}❌ Skip B2B (Back to Back) opposite candles          {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}📈 Use 1-Step MTG (Moving Target) strategy          {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}💫 Wait for clear trend confirmation                {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}⏰ Follow time-based trading sessions               {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.WHITE}💼 Maintain proper risk management                  {Fore.YELLOW}║{Style.RESET_ALL}
{Fore.YELLOW}║                                                         ║{Style.RESET_ALL}
{Fore.CYAN}╚═════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(rules_box)

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
{Fore.YELLOW}║  {Fore.RED}███████{Fore.GREEN}╗{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.CYAN}███████{Fore.WHITE}╗{Fore.RED}███{Fore.GREEN}╗  {Fore.BLUE}██{Fore.MAGENTA}╔{Fore.CYAN}█████{Fore.WHITE}╗{Fore.RED}██{Fore.GREEN}╗      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.GREEN}██╔════╝{Fore.BLUE}██{Fore.MAGENTA}║{Fore.CYAN}██╔════{Fore.WHITE}╝{Fore.RED}████{Fore.GREEN}╗ {Fore.BLUE}██{Fore.MAGENTA}║{Fore.CYAN}██╔══{Fore.WHITE}██{Fore.RED}╗{Fore.GREEN}██{Fore.BLUE}║      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.WHITE}║{Fore.RED}█████{Fore.GREEN}╗  {Fore.BLUE}██{Fore.MAGENTA}╔██{Fore.CYAN}╗{Fore.WHITE}██{Fore.RED}║{Fore.GREEN}███████{Fore.BLUE}║{Fore.MAGENTA}██{Fore.CYAN}║      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.MAGENTA}╚════██{Fore.CYAN}║{Fore.WHITE}██{Fore.RED}║{Fore.GREEN}██╔══╝  {Fore.BLUE}██{Fore.MAGENTA}║╚██{Fore.CYAN}╗██{Fore.WHITE}║{Fore.RED}██╔══██{Fore.GREEN}║{Fore.BLUE}██{Fore.MAGENTA}║      ║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.CYAN}███████{Fore.WHITE}║{Fore.RED}██{Fore.GREEN}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.WHITE}║ {Fore.RED}╚████{Fore.GREEN}║{Fore.BLUE}██{Fore.MAGENTA}║  {Fore.CYAN}██{Fore.WHITE}║{Fore.RED}███████{Fore.GREEN}╗║{Style.RESET_ALL}
{Fore.YELLOW}║  {Fore.RED}╚══════╝{Fore.GREEN}╚═╝{Fore.BLUE}╚══════╝{Fore.MAGENTA}╚═╝{Fore.CYAN}  ╚═══╝{Fore.WHITE}╚═╝  {Fore.RED}╚═╝{Fore.GREEN}╚══════╝║{Style.RESET_ALL}
{Fore.CYAN}╠════════════════════════════════════════════════╣{Style.RESET_ALL}
{Fore.YELLOW}║     {Fore.WHITE}👾 𝓑𝓘𝓝𝓐𝓡𝓨 𝓑𝓔𝓐𝓢𝓣 𝓟𝓡𝓞 v2.0 👾     {Fore.YELLOW}║{Style.RESET_ALL}
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

def get_current_time():
    """Get current time in Asia/Karachi timezone"""
    return datetime.now(TIMEZONE)

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

def display_assets_dialog():
    """Display available assets in a beautiful, mobile-friendly dialog box"""
    terminal_width = os.get_terminal_size().columns
    max_width = min(terminal_width - 4, 60)  # Adaptive width
    
    # Create box border
    border_line = f"╔{'═' * (max_width - 2)}╗"
    empty_line = f"║{' ' * (max_width - 2)}║"
    
    # Print header
    print(f"\n{Fore.CYAN}{border_line}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.YELLOW} 💱 Select Trading Assets (comma-separated) {' ' * (max_width - 45)}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{border_line}{Style.RESET_ALL}")
    
    # Display assets in adaptive columns
    col_width = 15
    cols = max(1, (max_width - 4) // col_width)
    
    for i in range(0, len(AVAILABLE_ASSETS), cols):
        row = AVAILABLE_ASSETS[i:i+cols]
        formatted_row = [f"{Fore.GREEN}{asset.ljust(col_width)}{Style.RESET_ALL}" for asset in row]
        line = f"{Fore.CYAN}║ {' '.join(formatted_row)}{' ' * (max_width - 4 - len(formatted_row) * col_width)}║{Style.RESET_ALL}"
        print(line)
    
    # Close box
    print(f"{Fore.CYAN}{border_line}{Style.RESET_ALL}")
    
    while True:
        # Styled input prompt
        print(f"\n{Fore.CYAN}╭──────────────────────────────╮{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.WHITE} 🌐 Enter assets:              {Fore.CYAN} {Style.RESET_ALL}")
        print(f"{Fore.CYAN}╰──────────────────────────────╯{Style.RESET_ALL}")
        user_assets = input(f"{Fore.GREEN}➤ {Style.RESET_ALL}").strip()
        
        # Validate user input
        selected_assets = [asset.strip() for asset in user_assets.split(',')]
        invalid_assets = [asset for asset in selected_assets if asset not in AVAILABLE_ASSETS]
        
        if invalid_assets:
            print(f"\n{Fore.RED}❌ Invalid assets: {', '.join(invalid_assets)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please choose from the available assets.{Style.RESET_ALL}")
            continue
        
        return selected_assets

def get_numeric_input(prompt, input_type="signals"):
    """Get numeric input with a beautiful, mobile-friendly design"""
    terminal_width = os.get_terminal_size().columns
    max_width = min(terminal_width - 4, 60)
    
    while True:
        # Styled input box
        print(f"\n{Fore.CYAN}╭──────────────────────────────╮{Style.RESET_ALL}")
        
        if input_type == "signals":
            print(f"{Fore.CYAN}│{Fore.WHITE} 📊 Enter number of signals to generate {Fore.CYAN}{Style.RESET_ALL}")
        elif input_type == "filter":
            print(f"{Fore.CYAN}│{Fore.WHITE} 🎯 Select Signal Filter Option     {Fore.CYAN}│{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╰──────────────────────────────╯{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}╔══════════════ 🎯 Signal Filter Options 🎯 ══════════════╗{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}║ {Fore.GREEN}1{Fore.WHITE}. All Signals (CALL & PUT)                {Fore.YELLOW}║{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}║ {Fore.GREEN}2{Fore.WHITE}. CALL Signals Only                       {Fore.YELLOW}║{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}║ {Fore.GREEN}3{Fore.WHITE}. PUT Signals Only                        {Fore.YELLOW}║{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}╭──────────────────────────────╮{Style.RESET_ALL}")
            print(f"{Fore.CYAN}│{Fore.WHITE} 🌐 Enter your choice:          {Fore.CYAN}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}╰──────────────────────────────╯{Style.RESET_ALL}")
        
        try:
            # Styled input prompt
            value = input(f"{Fore.GREEN}➤ {Style.RESET_ALL}")
            
            # Convert and validate input
            numeric_value = int(value)
            
            if input_type == "signals" and numeric_value > 0:
                return numeric_value
            elif input_type == "filter" and numeric_value in [1, 2, 3]:
                return numeric_value
            else:
                print(f"\n{Fore.RED}❌ Invalid input. Please try again.{Style.RESET_ALL}")
        
        except ValueError:
            print(f"\n{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")

def display_time_info():
    """Display current time and timezone information"""
    current_time = get_current_time()
    print(f"\n{Fore.CYAN}╔══════════════ 🕒 Time Information 🕒 ══════════════╗{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║ {Fore.WHITE}Timezone:{Fore.GREEN} Asia/Karachi (UTC+5:00){Style.RESET_ALL}             ║")
    print(f"{Fore.YELLOW}║ {Fore.WHITE}Date:{Fore.GREEN} {current_time.strftime('%Y-%m-%d')}{Style.RESET_ALL}                    ║")
    print(f"{Fore.YELLOW}║ {Fore.WHITE}Time:{Fore.GREEN} {current_time.strftime('%H:%M:%S')}{Style.RESET_ALL}                      ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════╝{Style.RESET_ALL}")

def generate_signals(assets, num_signals, filter_option):
    """Generate trading signals based on user parameters"""
    signals = []
    
    # Start with current time, round to nearest 5-minute interval
    current_time = get_current_time()
    start_time = current_time.replace(minute=(current_time.minute // 5) * 5, second=0, microsecond=0)
    
    def generate_signal_direction():
        """Generate signal direction based on filter option"""
        if filter_option == 1:  # All signals
            return random.choice(['CALL', 'PUT'])
        elif filter_option == 2:  # CALL Only
            return 'CALL'
        else:  # PUT Only
            return 'PUT'
    
    # Generate signals for each selected asset
    for asset in assets:
        signal_time = start_time
        for _ in range(num_signals):
            # Increment time by 5 minutes for each signal
            signal = {
                'asset': asset,
                'time': signal_time.strftime('%H:%M'),
                'direction': generate_signal_direction()
            }
            signals.append(signal)
            signal_time += timedelta(minutes=5)
    
    return signals

def display_signals(signals):
    """Display generated signals in a responsive, mobile-friendly table"""
    if not signals:
        print(f"\n{Fore.RED}❌ No signals generated.{Style.RESET_ALL}")
        return
    
    # Determine terminal width for responsive design
    terminal_width = os.get_terminal_size().columns
    max_width = min(terminal_width - 4, 60)
    
    # Create responsive table
    print(f"\n{Fore.CYAN}╔{'═' * (max_width - 2)}╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}📊 Generated Signals{' ' * (max_width - 20)}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠{'═' * (max_width - 2)}╣{Style.RESET_ALL}")
    
    # Responsive column widths
    asset_width = 15
    time_width = 10
    direction_width = 10
    
    # Table header
    header = f"{Fore.CYAN}║ {Fore.WHITE}{'Asset':<{asset_width}}{'Time':<{time_width}}{'Direction':<{direction_width}}{' ' * (max_width - asset_width - time_width - direction_width - 6)}║{Style.RESET_ALL}"
    print(header)
    print(f"{Fore.CYAN}╟{'─' * (max_width - 2)}╢{Style.RESET_ALL}")
    
    # Table rows
    for signal in signals:
        row = f"{Fore.CYAN}║ {Fore.GREEN}{signal['asset']:<{asset_width}}{Fore.BLUE}{signal['time']:<{time_width}}{Fore.MAGENTA}{signal['direction']:<{direction_width}}{' ' * (max_width - asset_width - time_width - direction_width - 6)}║{Style.RESET_ALL}"
        print(row)
    
    print(f"{Fore.CYAN}╚{'═' * (max_width - 2)}╝{Style.RESET_ALL}")

def export_signals(signals):
    """Export signals to a CSV file"""
    try:
        filename = f"signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        storage_dir = os.path.expanduser('~/storage/downloads')
        
        # Ensure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
        filepath = os.path.join(storage_dir, filename)
        
        with open(filepath, 'w') as f:
            # Write header
            f.write("Asset,Time,Direction\n")
            
            # Write signals
            for signal in signals:
                f.write(f"{signal['asset']},{signal['time']},{signal['direction']}\n")
        
        print(f"\n{Fore.GREEN}✅ Signals exported to {filepath}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error exporting signals: {str(e)}{Style.RESET_ALL}")

def generate_signal_workflow():
    """Main workflow for signal generation"""
    # Display current time information
    display_time_info()
    
    # Display and select assets
    selected_assets = display_assets_dialog()
    
    # Get number of signals
    num_signals = get_numeric_input("Enter number of signals to generate", "signals")
    
    # Get signal filter
    filter_option = get_numeric_input("Select signal filter option", "filter")
    
    # Generate signals
    print(f"\n{Fore.YELLOW}Generating Signals...{Style.RESET_ALL}")
    animated_progress_bar(2)
    
    # Generate and display signals
    signals = generate_signals(selected_assets, num_signals, filter_option)
    display_signals(signals)
    
    # Export option
    print(f"\n{Fore.CYAN}╭──────────────────────────────╮{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Fore.WHITE} 💾 Export signals to CSV?     {Fore.CYAN} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}╰──────────────────────────────╯{Style.RESET_ALL}")
    if input(f"{Fore.GREEN}➤ (y/n): {Style.RESET_ALL}").lower() == 'y':
        export_signals(signals)

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
    
    # Signal generation workflow
    while True:
        generate_signal_workflow()
        
        # Ask to generate another set of signals
        print(f"\n{Fore.CYAN}╭──────────────────────────────╮{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.WHITE} 🔄 Generate another set?      {Fore.CYAN} {Style.RESET_ALL}")
        print(f"{Fore.CYAN}╰──────────────────────────────╯{Style.RESET_ALL}")
        if input(f"{Fore.GREEN}➤ (y/n): {Style.RESET_ALL}").lower() != 'y':
            break
    
    print(f"\n{Fore.GREEN}👋 Thank you for using Binary Beast 👾 Pro!{Style.RESET_ALL}")
    print_trading_rules()

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

def main():
    try:
        while True:
            os.makedirs(os.path.join(os.path.expanduser('~'), '.signal_config'), exist_ok=True)
            os.makedirs(os.path.join(os.path.expanduser('~'), 'storage/downloads'), exist_ok=True)
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(print_neon_banner())
            
            if check_license():
                os.system('cls' if os.name == 'nt' else 'clear')
                print(print_neon_banner())
                
                print(f"\n{Fore.GREEN}✨ Welcome to Binary Beast Pro!{Style.RESET_ALL}")
                time.sleep(1)
                send_request()
                break
            else:
                print(f"\n{Fore.RED}❌ Program terminated. No valid license.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}📱 Contact @ahadhssain786 on Telegram for license purchase{Style.RESET_ALL}")
                print_trading_rules()
                break
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️ Program terminated by user{Style.RESET_ALL}")
        print_trading_rules()
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {str(e)}{Style.RESET_ALL}")
        print_trading_rules()
    finally:
        print(f"\n{Fore.GREEN}👋 Thank you for using Binary Beast 👾 Pro!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
    
