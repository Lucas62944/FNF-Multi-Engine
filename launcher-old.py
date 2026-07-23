import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import shutil

class FNFLauncherV1
    def __init__(self, root)
        self.root = root
        self.root.title(FNF Launcher v1.0.0)
        self.root.geometry(500x500)

        self.mods_dir = mods
        if not os.path.exists(self.mods_dir)
            os.makedirs(self.mods_dir)

        self.lbl_title = tk.Label(self.root, text=FNF Launcher, font=(Arial, 18, bold))
        self.lbl_title.pack(pady=10)

        self.mods_listbox = tk.Listbox(self.root, font=(Arial, 11), width=50, height=12)
        self.mods_listbox.pack(pady=10)

        self.btn_add = tk.Button(self.root, text=Adicionar Mod, command=self.add_mod, bg=#2196F3, fg=white)
        self.btn_add.pack(pady=5)

        self.btn_play = tk.Button(self.root, text=INICIAR JOGO, font=(Arial, 12, bold), bg=#4CAF50, fg=white, command=self.play_game)
        self.btn_play.pack(pady=15)

        self.update_mods()

    def update_mods(self)
        self.mods_listbox.delete(0, tk.END)
        if os.path.exists(self.mods_dir)
            for item in os.listdir(self.mods_dir)
                if os.path.isdir(os.path.join(self.mods_dir, item))
                    self.mods_listbox.insert(tk.END, item)

    def add_mod(self)
        src = filedialog.askdirectory(title=Selecione a pasta do Mod)
        if src
            dest = os.path.join(self.mods_dir, os.path.basename(src))
            shutil.copytree(src, dest)
            self.update_mods()

    def play_game(self)
        exes = [f for f in os.listdir(.) if f.endswith(.exe)]
        if exes
            subprocess.Popen(exes[0])
        else
            messagebox.showerror(Erro, Nenhum .exe encontrado no diretório do launcher.)

if __name__ == __main__
    root = tk.Tk()
    app = FNFLauncherV1(root)
    root.mainloop()
