import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import requests
import subprocess
from tkinter import messagebox
from pathlib import Path
import threading
import time

class ProgramInstaller:
    def __init__(self, root):
        self.root = root
        self.current_language = "tr"
        self.download_folder = str(Path.home() / "Downloads" / "Program_Installer")
        
        os.makedirs(self.download_folder, exist_ok=True)
        
        self.translations = {
            "tr": {
                "title": "Program Yükleyici",
                "select_programs": "İndirmek İstediğiniz Programları Seçin",
                "download_button": "Seçili Programları İndir",
                "warning": "Uyarı",
                "select_warning": "Lütfen en az bir program seçin!",
                "info": "Bilgi",
                "download_started": "İndirme işlemi başladı. Dosyalar şu klasöre kaydedilecek:",
                "download_complete": "İndirme tamamlandı:",
                "download_error": "İndirme hatası:",
                "change_language": "Switch to English",
                "select_all": "Tümünü Seç",
                "deselect_all": "Tümünü Kaldır",
                "downloading": "İndiriliyor...",
                "categories": {
                    "browsers": "Tarayıcılar",
                    "communication": "İletişim",
                    "development": "Geliştirici Araçları",
                    "multimedia": "Multimedya",
                    "gaming": "Oyun & Eğlence",
                    "utilities": "Sistem Araçları",
                    "security": "Güvenlik"
                }
            },
            "en": {
                "title": "Program Installer",
                "select_programs": "Select Programs to Download",
                "download_button": "Download Selected Programs",
                "warning": "Warning",
                "select_warning": "Please select at least one program!",
                "info": "Information",
                "download_started": "Download started. Files will be saved to:",
                "download_complete": "Download completed:",
                "download_error": "Download error:",
                "change_language": "Türkçe'ye Geç",
                "select_all": "Select All",
                "deselect_all": "Deselect All",
                "downloading": "Downloading...",
                "categories": {
                    "browsers": "Browsers",
                    "communication": "Communication",
                    "development": "Development Tools",
                    "multimedia": "Multimedia",
                    "gaming": "Gaming & Entertainment",
                    "utilities": "System Utilities",
                    "security": "Security"
                }
            }
        }

        self.categorized_programs = {
            "browsers": {
                "Google Chrome": {
                    "url": "https://dl.google.com/chrome/install/ChromeStandaloneSetup64.exe",
                    "direct_download": True,
                    "filename": "Chrome_Setup.exe"
                },
                "Mozilla Firefox": {
                    "url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=tr",
                    "direct_download": True,
                    "filename": "Firefox_Setup.exe"
                },
                "Brave Browser": {
                    "url": "https://laptop-updates.brave.com/latest/winx64",
                    "direct_download": True,
                    "filename": "Brave_Setup.exe"
                }
            },
            "utilities": {
                "7-Zip": {
                    "url": "https://www.7-zip.org/a/7z2301-x64.exe",
                    "direct_download": True,
                    "filename": "7zip_Setup.exe"
                },
                "Internet Download Manager": {
                    "url": "https://drive.google.com/file/d/15rEhQFVCPfwiro_zvmTgI0OS9XO0CtT7/view?usp=sharing",
                    "direct_download": False
                },
                "AnyDesk Full Version": {
                    "url": "https://drive.google.com/file/d/1Xe-Tuad2gq1zEn-VE5eiNEQ5EF8rnFaK/view?usp=sharing",
                    "direct_download": False
                },
                "Traffic Monitor": {
                    "url": "https://drive.google.com/file/d/1-MreAWdLb2UPzTfWIZjE2qJLQxgVHeou/view?usp=sharing",
                    "direct_download": False
                },
                "DirectX & Redist Package": {
                    "url": "https://drive.google.com/file/d/11KyIrairbxD9qSBphZ9JTyp5j-yOMDr5/view?usp=sharing",
                    "direct_download": False
                },
                "NVIDIA GeForce Experience": {
                    "url": "https://us.download.nvidia.com/GFE/GFEClient/3.27.0.112/GeForce_Experience_v3.27.0.112.exe",
                    "direct_download": True,
                    "filename": "GeForce_Experience_Setup.exe"
                },
                "Windows & Office Activator": {
                    "url": "https://drive.google.com/file/d/1VxCd9LKAY6VKG7DuP0ClEi-35TFCDYpn/view?usp=sharing",
                    "direct_download": False
                }
            },
            "development": {
                "Visual Studio Code": {
                    "url": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user",
                    "direct_download": True,
                    "filename": "VSCode_Setup.exe"
                },
                "Notepad++": {
                    "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.6.4/npp.8.6.4.Installer.x64.exe",
                    "direct_download": True,
                    "filename": "Notepad_Plus_Plus_Setup.exe"
                }
            }
        }
        
        self.web_redirect_programs = {
            "communication": {
                "Discord": "https://discord.com/download",
                "Discord Canary": "https://discord.com/download/canary",
                "Discord PTB": "https://discord.com/download/ptb",
                "WhatsApp Desktop": "https://www.whatsapp.com/download",
                "Telegram Desktop": "https://desktop.telegram.org/",
                "Zoom": "https://zoom.us/download"
            },
            "multimedia": {
                "VLC Media Player": "https://www.videolan.org/vlc/",
                "Spotify": "https://www.spotify.com/download/",
                "HandBrake": "https://handbrake.fr/downloads.php",
                "Iriun Webcam": "https://iriun.com/"
            },
            "gaming": {
                "Steam": "https://store.steampowered.com/about/",
                "Riot Games": "https://www.riotgames.com/",
                "Razer Synapse": "https://www.razer.com/synapse-3",
                "Vencord": "https://drive.google.com/file/d/15073q_Wh6nddbYR-mflm-pUgmvCHUVJj/view?usp=sharing"
            },
            "security": {
                "NetBird": "https://netbird.io/downloads",
                "Password Safe": "https://pwsafe.org/download.shtml",
                "Nextcloud": "https://nextcloud.com/install/",
                "Flameshot": "https://flameshot.org/"
            }
        }
        
        for category, programs in self.web_redirect_programs.items():
            if category not in self.categorized_programs:
                self.categorized_programs[category] = {}
            for program, url in programs.items():
                self.categorized_programs[category][program] = {
                    "url": url,
                    "direct_download": False
                }
        
        self.root.title(self.get_text("title"))
        self.root.geometry("1000x800")
        
        style = ttk.Style()
        style.configure("TNotebook", padding=10)
        style.configure("TNotebook.Tab", padding=[20, 5], font=('Helvetica', 10))
        style.configure("Download.TButton", padding=10, font=('Helvetica', 11, 'bold'))
        style.configure("Language.TButton", padding=5)
        
        self.create_widgets()
        
    def download_file(self, url, filename):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            filepath = os.path.join(self.download_folder, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True, filepath
        except Exception as e:
            return False, str(e)
    
    def run_installer(self, filepath, program_name):
        try:
            subprocess.Popen(filepath)
            print(f"Setup started: {program_name}")
        except Exception as e:
            print(f"Setup start error ({program_name}): {str(e)}")
    
    def download_selected_programs(self):
        selected = [prog for prog, var in self.checkboxes.items() if var.get()]
        
        if not selected:
            messagebox.showwarning(self.get_text("warning"),
                                 self.get_text("select_warning"))
            return
        
        messagebox.showinfo(self.get_text("info"),
                          f"{self.get_text('download_started')}\n{self.download_folder}")
        
        def download_thread():
            for program in selected:
                for category in self.categorized_programs:
                    if program in self.categorized_programs[category]:
                        program_info = self.categorized_programs[category][program]
                        
                        if program_info["direct_download"]:
                            success, result = self.download_file(
                                program_info["url"],
                                program_info["filename"]
                            )
                            
                            if success:
                                print(f"{self.get_text('download_complete')} {program}")
                                self.run_installer(result, program)
                                time.sleep(2)
                            else:
                                print(f"{self.get_text('download_error')} {program} - {result}")
                        else:
                            webbrowser.open(program_info["url"])
                        break
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def get_text(self, key, category=None):
        if category:
            return self.translations[self.current_language]["categories"][category]
        return self.translations[self.current_language][key]
    
    def select_all(self):
        for var in self.checkboxes.values():
            var.set(True)
            
    def deselect_all(self):
        for var in self.checkboxes.values():
            var.set(False)
            
    def toggle_language(self):
        self.current_language = "en" if self.current_language == "tr" else "tr"
        self.root.title(self.get_text("title"))
        
        for i, category in enumerate(self.categorized_programs):
            self.notebook.tab(i, text=self.get_text("categories", category))
        
        self.download_button.config(text=self.get_text("download_button"))
        self.lang_button.config(text=self.get_text("change_language"))

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        top_frame = ttk.Frame(self.main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(top_frame, 
                              text=self.get_text("select_programs"),
                              font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        self.lang_button = ttk.Button(top_frame,
                                    text=self.get_text("change_language"),
                                    command=self.toggle_language,
                                    style="Language.TButton")
        self.lang_button.grid(row=0, column=1, padx=10)
        
        select_all_btn = ttk.Button(top_frame,
                                  text=self.get_text("select_all"),
                                  command=self.select_all)
        select_all_btn.grid(row=0, column=2, padx=5)
        
        deselect_all_btn = ttk.Button(top_frame,
                                    text=self.get_text("deselect_all"),
                                    command=self.deselect_all)
        deselect_all_btn.grid(row=0, column=3, padx=5)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.checkboxes = {}
        
        for category in self.categorized_programs:
            frame = ttk.Frame(self.notebook, padding="10")
            self.notebook.add(frame, text=self.get_text("categories", category))
            
            for i, (program, info) in enumerate(self.categorized_programs[category].items()):
                var = tk.BooleanVar()
                self.checkboxes[program] = var
                
                label_text = f"{program} {'(Direct)' if info.get('direct_download', False) else '(Web)'}"
                ttk.Checkbutton(frame, text=label_text, 
                              variable=var).grid(row=i, column=0, sticky=tk.W, pady=2)
        
        self.download_button = ttk.Button(self.main_frame,
                                        text=self.get_text("download_button"),
                                        command=self.download_selected_programs,
                                        style="Download.TButton")
        self.download_button.grid(row=2, column=0, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramInstaller(root)
    root.mainloop() 