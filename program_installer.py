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
        self.version = "1.0.0"
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
                "download_speed": "İndirme Hızı:",
                "remaining_time": "Kalan Süre:",
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
                "download_speed": "Download Speed:",
                "remaining_time": "Time Remaining:",
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
                    "url": "https://drive.usercontent.google.com/download?id=15rEhQFVCPfwiro_zvmTgI0OS9XO0CtT7&export=download&authuser=0&confirm=t&uuid=9c132578-086c-4aa3-b29f-51e6c3c8f5bb&at=AIrpjvMzLmf2LSezOT7tnu-TCH9K%3A1736602074815",
                    "direct_download": True
                },
                "AnyDesk Full Version": {
                    "url": "https://drive.usercontent.google.com/download?id=1Xe-Tuad2gq1zEn-VE5eiNEQ5EF8rnFaK&export=download&authuser=0&confirm=t&uuid=fcefe3c0-136b-4b63-a779-859ef580de9a&at=AIrpjvNDOPdVylNSuBlb1papPMKc%3A1736602155234",
                    "direct_download": True
                },
                "Traffic Monitor": {
                    "url": "https://drive.usercontent.google.com/download?id=1-MreAWdLb2UPzTfWIZjE2qJLQxgVHeou&export=download&authuser=0",
                    "direct_download": True
                },
                "DirectX & Redist Package": {
                    "url": "https://drive.usercontent.google.com/download?id=11KyIrairbxD9qSBphZ9JTyp5j-yOMDr5&export=download&authuser=0&confirm=t&uuid=43e62fd1-fb14-4f70-a8c5-205aa575491a&at=AIrpjvPyYUYIqqp82pIm0NTXzKMG%3A1736602253037",
                    "direct_download": True
                },
                "NVIDIA GeForce Experience": {
                    "url": "https://us.download.nvidia.com/GFE/GFEClient/3.27.0.112/GeForce_Experience_v3.27.0.112.exe",
                    "direct_download": True,
                    "filename": "GeForce_Experience_Setup.exe"
                },
                "Windows & Office Activator": {
                    "url": "https://drive.usercontent.google.com/download?id=1VxCd9LKAY6VKG7DuP0ClEi-35TFCDYpn&export=download&authuser=0",
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
                "Discord": {
                    "url": "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",
                    "direct_download": True,
                    "filename": "Discord_Setup.exe"
                },
                "Discord Canary": {
                    "url": "https://canary.discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",
                    "direct_download": True,
                    "filename": "Discord_Canary_Setup.exe"
                },
                "Discord PTB": {
                    "url": "https://discord.com/api/download/ptb?platform=win",
                    "direct_download": True,
                    "filename": "Discord_PTB_Setup.exe"
                },
                "WhatsApp Desktop": {
                    "url": "https://get.microsoft.com/installer/download/9NKSQGP7F2NH?cid=website_cta_psi",
                    "direct_download": True,
                    "filename": "WhatsApp_Setup.exe"
                },
                "Telegram Desktop": {
                    "url": "https://telegram.org/dl/desktop/win64",
                    "direct_download": True,
                    "filename": "Telegram_Setup.exe"
                },
                "Zoom": {
                    "url": "https://zoom.us/client/6.3.5.54827/ZoomInstallerFull.exe?archType=x64",
                    "direct_download": True,
                    "filename": "Zoom_Setup.exe"
                }
            },
            "multimedia": {
                "VLC Media Player": {
                    "url": "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe",
                    "direct_download": True,
                    "filename": "VLC_Setup.exe"
                },
                "Spotify": {
                    "url": "https://download.scdn.co/SpotifySetup.exe",
                    "direct_download": True,
                    "filename": "Spotify_Setup.exe"
                },
                "HandBrake": {
                    "url": "https://handbrake.fr/rotation.php?file=HandBrake-1.9.0-x86_64-Win_GUI.exe",
                    "direct_download": True,
                    "filename": "HandBrake_Setup.exe"
                },
                "Iriun Webcam": {
                    "url": "https://1758658189.rsc.cdn77.org/IriunWebcam-2.8.10.exe",
                    "direct_download": True,
                    "filename": "IriunWebcam_Setup.exe"
                }
            },
            "gaming": {
                "Steam": {
                    "url": "https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe",
                    "direct_download": True,
                    "filename": "Steam_Setup.exe"
                },
                "Riot Games": {
                    "url": "https://valorant.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.live.ap.exe",
                    "direct_download": True,
                    "filename": "RiotGames_Setup.exe"
                }
            },
            "security": {
                "NetBird": {
                    "url": "https://pkgs.netbird.io/windows/x64",
                    "direct_download": True,
                    "filename": "NetBird_Setup.exe"
                },
                "Password Safe": {
                    "url": "https://github.com/pwsafe/pwsafe/releases/download/3.67.0/pwsafe-3.67.0.exe",
                    "direct_download": True,
                    "filename": "PasswordSafe_Setup.exe"
                },
                "Flameshot": {
                    "url": "https://github.com/flameshot-org/flameshot/releases/download/v12.1.0/Flameshot-12.1.0-win64.msi",
                    "direct_download": True,
                    "filename": "Flameshot_Setup.msi"
                }
            }
        }
        
        for category, programs in self.web_redirect_programs.items():
            if category not in self.categorized_programs:
                self.categorized_programs[category] = {}
            for program, info in programs.items():
                self.categorized_programs[category][program] = info
        
        self.root.title(f"{self.get_text('title')} v{self.version}")
        self.root.geometry("1000x800")
        
        style = ttk.Style()
        style.configure("TNotebook", padding=10)
        style.configure("TNotebook.Tab", padding=[20, 5], font=('Helvetica', 10))
        style.configure("Download.TButton", padding=10, font=('Helvetica', 11, 'bold'))
        style.configure("Language.TButton", padding=5)
        
        self.create_widgets()
        
    def download_file(self, url, filename):
        try:
            session = requests.Session()
            response = session.get(url, stream=True)
            response.raise_for_status()
            
            filepath = os.path.join(self.download_folder, filename)
            total_size = int(response.headers.get('content-length', 0))
            
            if hasattr(self, 'progress_var'):
                self.progress_var.set(0)
            
            block_size = 1024 * 1024  # 1MB blocks
            downloaded = 0
            start_time = time.time()
            update_interval = 0.1  # Update UI every 0.1 seconds
            last_update = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        current_time = time.time()
                        if (current_time - last_update) >= update_interval:
                            if hasattr(self, 'progress_var') and hasattr(self, 'speed_label'):
                                elapsed_time = current_time - start_time
                                if elapsed_time > 0:
                                    speed = downloaded / (1024 * 1024 * elapsed_time)
                                    if total_size > 0:
                                        progress = (downloaded / total_size) * 100
                                        self.progress_var.set(progress)
                                        remaining = (total_size - downloaded) / (downloaded / elapsed_time)
                                        
                                        self.speed_label.config(
                                            text=f"{self.get_text('download_speed')} {speed:.1f} MB/s"
                                        )
                                        self.time_label.config(
                                            text=f"{self.get_text('remaining_time')} {int(remaining)}s"
                                        )
                                    
                                    self.root.update_idletasks()
                                    last_update = current_time
            
            session.close()
            return True, filepath
        except Exception as e:
            return False, str(e)
    
    def run_installer(self, filepath, program_name):
        try:
            subprocess.Popen([filepath], shell=True)
            print(f"Setup started: {program_name}")
        except Exception as e:
            print(f"Setup start error ({program_name}): {str(e)}")
            messagebox.showerror("Hata", f"Program başlatılamadı: {program_name}\nHata: {str(e)}")
    
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
        
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, 
                                      orient="horizontal",
                                      length=300,
                                      mode="determinate",
                                      variable=self.progress_var)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.speed_label = ttk.Label(progress_frame, text="")
        self.speed_label.grid(row=1, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(progress_frame, text="")
        self.time_label.grid(row=2, column=0, sticky=tk.W)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
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
        self.download_button.grid(row=3, column=0, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramInstaller(root)
    root.mainloop() 