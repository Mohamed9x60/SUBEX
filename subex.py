import os
import csv
import socket
import requests
import tldextract
from knock import KNOCKPY
from colorama import Fore, Style, Back
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

class Subex:
    def __init__(self):
        self.results = []

        # Colors for output
        self.colors = [
            Fore.RED,
            Fore.RED + Style.BRIGHT,
            Fore.RED + Style.NORMAL,
            Fore.RED + Style.DIM,
            Fore.RED + Style.RESET_ALL + Back.YELLOW,
            Fore.GREEN,
            Fore.GREEN + Style.BRIGHT,
            Fore.GREEN + Style.NORMAL,
            Fore.GREEN + Style.DIM,
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW,
            Fore.YELLOW,
            Fore.YELLOW + Style.BRIGHT,
            Fore.YELLOW + Style.NORMAL,
            Fore.YELLOW + Style.DIM,
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW,
            Fore.BLUE,
            Fore.BLUE + Style.BRIGHT,
            Fore.BLUE + Style.NORMAL,
            Fore.BLUE + Style.DIM,
            Fore.BLUE + Style.RESET_ALL + Back.YELLOW,
            Fore.MAGENTA,
            Fore.MAGENTA + Style.BRIGHT,
            Fore.MAGENTA + Style.NORMAL,
            Fore.MAGENTA + Style.DIM,
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW,
            Fore.CYAN,
            Fore.CYAN + Style.BRIGHT,
            Fore.CYAN + Style.NORMAL,
            Fore.CYAN + Style.DIM,
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW,
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW,  # وردي
            Fore.MAGENTA + Style.BRIGHT + Style.RESET_ALL + Back.YELLOW,  # وردي فاتح
            Fore.MAGENTA + Style.NORMAL + Style.RESET_ALL + Back.YELLOW,  # وردي عادي
            Fore.MAGENTA + Style.DIM + Style.RESET_ALL + Back.YELLOW,  # وردي داكن
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # وردي متوسط الوضوح وفاتح
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # وردي متوسط الوضوح وعادي
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # وردي متوسط الوضوح وداكن
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # وردي مظلم وفاتح
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # وردي مظلم وعادي
            Fore.MAGENTA + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # وردي مظلم وداكن
            Fore.MAGENTA + Style.BRIGHT + Style.RESET_ALL + Back.YELLOW,  # وردي فاتح وفاتح
            Fore.MAGENTA + Style.NORMAL + Style.RESET_ALL + Back.YELLOW,  # وردي عادي وعادي
            Fore.MAGENTA + Style.DIM + Style.RESET_ALL + Back.YELLOW,  # وردي داكن وداكن
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW,  # بنفسجي
            Fore.CYAN + Style.BRIGHT + Style.RESET_ALL + Back.YELLOW,  # بنفسجي فاتح
            Fore.CYAN + Style.NORMAL + Style.RESET_ALL + Back.YELLOW,  # بنفسجي عادي
            Fore.CYAN + Style.DIM + Style.RESET_ALL + Back.YELLOW,  # بنفسجي داكن
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # بنفسجي متوسط الوضوح وفاتح
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # بنفسجي متوسط الوضوح وعادي
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # بنفسجي متوسط الوضوح وداكن
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # بنفسجي مظلم وفاتح
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # بنفسجي مظلم وعادي
            Fore.CYAN + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # بنفسجي مظلم وداكن
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW,  # فيروزي
            Fore.YELLOW + Style.BRIGHT + Style.RESET_ALL + Back.YELLOW,  # فيروزي فاتح
            Fore.YELLOW + Style.NORMAL + Style.RESET_ALL + Back.YELLOW,  # فيروزي عادي
            Fore.YELLOW + Style.DIM + Style.RESET_ALL + Back.YELLOW,  # فيروزي داكن
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # فيروزي متوسط الوضوح وفاتح
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # فيروزي متوسط الوضوح وعادي
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # فيروزي متوسط الوضوح وداكن
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # فيروزي مظلم وفاتح
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # فيروزي مظلم وعادي
            Fore.YELLOW + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # فيروزي مظلم وداكن
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW,  # برتقالي
            Fore.GREEN + Style.BRIGHT + Style.RESET_ALL + Back.YELLOW,  # برتقالي فاتح
            Fore.GREEN + Style.NORMAL + Style.RESET_ALL + Back.YELLOW,  # برتقالي عادي
            Fore.GREEN + Style.DIM + Style.RESET_ALL + Back.YELLOW,  # برتقالي داكن
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # برتقالي متوسط الوضوح وفاتح
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # برتقالي متوسط الوضوح وعادي
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # برتقالي متوسط الوضوح وداكن
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # برتقالي مظلم وفاتح
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # برتقالي مظلم وعادي
            Fore.GREEN + Style.RESET_ALL + Back.YELLOW + Style.DIM,  # برتقالي مظلم وداكن
            Fore.RED + Style.RESET_ALL + Back.YELLOW,  # أحمر
            Fore.RED + Style.BRIGHT + Style.RESET_ALL + Back.YELLOW,  # أحمر فاتح
            Fore.RED + Style.NORMAL + Style.RESET_ALL + Back.YELLOW,  # أحمر عادي
            Fore.RED + Style.DIM + Style.RESET_ALL + Back.YELLOW,  # أحمر داكن
            Fore.RED + Style.RESET_ALL + Back.YELLOW + Style.BRIGHT,  # أحمر متوسط الوضوح وفاتح
            Fore.RED + Style.RESET_ALL + Back.YELLOW + Style.NORMAL,  # أحمر متوسط الوضوح وعادي
            Fore.RED + Style.RESET_ALL + Back.YELLOW + Style.DIM  # أحمر متوسط الوضوح وداكن
        ]

    def start(self):
        self.banner()
        self.domain()

    def ask_save_result(self):
        while True:
            response = input(Fore.CYAN + "Do you want to save the result? (y/n): ")
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def input_url(self):
        return input("Enter URL: ")

    def choose_file_type(self):
        print(Fore.RESET + "Choose file type:")
        print("1. Text file (txt)")
        print("2. CSV file (csv)")
        print("3. XML file (xml)")
        print("4. HTML file (html)")
        print("5. Back to main menu")
        print("6. Exit")
        choice = input("Enter your choice: ")
        return choice

    def save_to_txt(self, filename):
        with open(filename, 'w') as file:
            file.write("Welcome to Subex!\n")
            file.write("Programmer: Mohamed Fouad :)\n")
            file.write("GitHub: https://github.com/Mohamed9x60\n\n")
            for item in self.results:
                file.write(str(item) + '\n')

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Data'])
            for item in self.results:
                writer.writerow([item])

    def save_to_xml(self, filename):
        root = ET.Element("Results")
        for item in self.results:
            result_element = ET.SubElement(root, "Result")
            result_element.text = str(item)
        tree = ET.ElementTree(root)
        tree.write(filename)

    def save_to_html(self, filename):
        with open(filename, "w") as file:
            file.write("<html><body>")
            file.write("<h1>Welcome to Subex!</h1>")
            file.write("<p>Programmer: Mohamed Fouad :)</p>")
            file.write("<p>GitHub: <a href='https://github.com/Mohamed9x60'>https://github.com/Mohamed9x60</a></p>")
            file.write("<h2>Results:</h2>")
            file.write("<ul>")
            for item in self.results:
                file.write("<li>{}</li>".format(item))
            file.write("</ul>")
            file.write("</body></html>")

    def add_tool_info_to_file(self, filename):
        with open(filename, 'r+') as file:
            contents = file.read()
            file.seek(0, 0)
            file.write("<h3 style='color:blue;'>Welcome to Subex!</h3>\n")
            file.write("<p style='color:blue;'>Programmer: Mohamed Fouad</p>\n")
            file.write("<p style='color:blue;'>GitHub: <a href='https://github.com/Mohamed9x60'>https://github.com/Mohamed9x60</a></p>\n\n")
            file.write(contents)

    def domain(self):
        os.system('clear')
        self.banner()
        try:
            if self.ask_save_result():
                url = self.input_url()
                results = KNOCKPY(url, dns=None, useragent=None, timeout=None, threads=None, recon=True, bruteforce=True, wordlist=None)
                print("Results:")
                for result in results:
                    self.results.append(result)
                    self.print_result(result)

                file_type_choice = self.choose_file_type()
                filename = input(Fore.CYAN + "Enter file name : ")
                if file_type_choice == '1':
                    self.save_to_txt(filename + '.txt')
                    print(Fore.GREEN + "Results saved to {}.txt".format(filename))
                elif file_type_choice == '2':
                    self.save_to_csv(filename + '.csv')
                    print(Fore.GREEN + "Results saved to {}.csv".format(filename))
                elif file_type_choice == '3':
                    self.save_to_xml(filename + '.xml')
                    print(Fore.GREEN + "Results saved to {}.xml".format(filename))
                elif file_type_choice == '4':
                    self.save_to_html(filename + '.html')
                    print(Fore.GREEN + "Results saved to {}.html".format(filename))
                elif file_type_choice == '5':
                    self.start()
                elif file_type_choice == '6':
                    print(Fore.RED + "Exiting...")
                    print(Fore.YELLOW + "Thank you for using my tool, Engineer Mohamed Fouad :)")
                    return
                else:
                    print(Fore.RED + "Invalid choice")
            else:
                print(Fore.GREEN + "Results not saved")
                print(Fore.YELLOW + "Thank you for using my tool, Engineer Mohamed Fouad :)")

        except Exception as e:
            print(Fore.RED + "An error occurred:", str(e))

    def print_result(self, result):
        domain = result['domain']
        ip = result['ip']
        risk_level = result.get(Fore.CYAN + 'risk_level', 'Unknown')
        description = result.get(Fore.BLUE + 'description', 'No description available')

        if risk_level == 'High':
            domain_color = Fore.RED
        elif risk_level == 'Medium':
            domain_color = Fore.ORANGE
        elif risk_level == 'Low':
            domain_color = Fore.YELLOW
        else:
            domain_color = Fore.GREEN

        print(domain_color + f"Domain: {domain}   IP: {ip}   Risk Level: {risk_level}")
        print(Fore.RESET + f"Description: {description}\n")

    def banner(self):
        print(Fore.BLUE + r'''
         ____  _   _ ____  _______  __
        / ___|| | | | __ )| ____\ \/ /
        \___ \| | | |  _ \|  _|  \  /
         ___) | |_| | |_) | |___ /  \
        |____/ \___/|____/|_____/_/\_\
                                       Free Palestine@
    ''')
        print(Fore.YELLOW + "Welcome to"+ Fore.BLUE + " Subex!")
        print(Fore.YELLOW + "Programmer: "+ Fore.RED + " Mohamed Fouad :)")
        print(Fore.YELLOW + "GitHub:"+ Fore.BLUE + " https://github.com/Mohamed9x60\n")

    def fetch_url(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print("An error occurred while fetching URL:", str(e))
            return False

    def validate_urls(self, urls):
        validated_urls = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.fetch_url, url) for url in urls]
            for future in futures:
                result = future.result()
                if result:
                    validated_urls.append(url)
        return validated_urls

subex = Subex()
subex.start()
