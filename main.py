import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("500x300")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Sélectionnez un dossier à organiser :", font=ctk.CTkFont(size=16))
        self.label.pack(pady=20)

        self.path_entry = ctk.CTkEntry(self, width=350)
        self.path_entry.pack(pady=10)

        self.browse_button = ctk.CTkButton(self, text="Parcourir", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        self.organize_button = ctk.CTkButton(self, text="Organiser", command=self.organize_files)
        self.organize_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder)

    def organize_files(self):
        folder_path = self.path_entry.get()
        if not os.path.isdir(folder_path):
            messagebox.showerror("Erreur", "Dossier invalide.")
            return

        file_types = {
            "Images": ['.png', '.jpg', '.jpeg', '.gif'],
            "Documents": ['.pdf', '.docx', '.txt'],
            "Audio": ['.mp3', '.wav'],
            "Videos": ['.mp4', '.avi', '.mov'],
            "Archives": ['.zip', '.rar', '.7z']
        }

        files_moved = 0
        other_dir = os.path.join(folder_path, "Autres")
        os.makedirs(other_dir, exist_ok=True)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                moved = False
                for folder, extensions in file_types.items():
                    if ext in extensions:
                        target_dir = os.path.join(folder_path, folder)
                        os.makedirs(target_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(target_dir, file))
                        files_moved += 1
                        moved = True
                        break
                if not moved:
                    shutil.move(file_path, os.path.join(other_dir, file))
                    files_moved += 1

        self.status_label.configure(text=f"{files_moved} fichiers organisés avec succès.")
        messagebox.showinfo("Terminé", f"{files_moved} fichiers organisés.")

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
