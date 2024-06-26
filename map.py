from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

class Peta:
    def __init__(self):
        self.skala = 10
        self.panjang = 0
        self.lebar = 150 * self.skala
        self.tinggi = 150 * self.skala
        self.batas = self.skala
        self.panjang_jalan = 20 * self.skala
        self.lebar_jalan = 20
        self.persimpangan = []
        self.jarak = 10
        
        # Menginisialisasi dan mengacak elemen-elemen
        self.sudut = [Image.open("env/cornerL.png").resize((20,20)), Image.open("env/cornerR.png").resize((20,20))]
        random.shuffle(self.sudut)
        
        self.jalan = [Image.open("env/jalanx.png"), Image.open("env/jalany.jpg")]
        random.shuffle(self.jalan)
        
        self.bangunan = [Image.open("building/building1.jpg"), Image.open("building/medium2-x.jpg"), Image.open("building/large-x.jpg"), Image.open("building/large2-x.jpg"), Image.open("building/small-x.jpg")]
        random.shuffle(self.bangunan)
        
        self.bangunan2 = [Image.open("building/medium2-y.jpg"), Image.open("building/large-y.jpg"), Image.open("building/large2-y.jpg"), Image.open("building/small-x.jpg")]
        random.shuffle(self.bangunan2)
        
        self.lingkungan = [Image.open("env/treeA.jpg"), Image.open("env/bushA.png"), Image.open("env/bushB.jpg"), Image.open("env/batuA.jpg")]
        random.shuffle(self.lingkungan)
        
        self.peta = Image.new("RGBA", (self.lebar, self.tinggi), "gray")
        self.gambar_peta = ImageDraw.Draw(self.peta)

    def batasX(self, x): return 0 if x <= 0 else (x if x < self.lebar else self.lebar)
    def batasY(self, y): return 0 if y <= 0 else (y if y < self.tinggi else self.tinggi)

    def buatJalan(self, posisi, arah):
        self.panjang += 1
        if self.panjang > 150 and (posisi[0] <= 0 or posisi[0] >= self.lebar or posisi[1] <= 0 or posisi[1] >= self.tinggi): return
        self.persimpangan.append(posisi)
        langkah = random.choice([1, 1])
        simpul_berikutnya = (posisi[0] + self.lebar_jalan if arah == "y" else posisi[0] + self.panjang_jalan * langkah,
                             posisi[1] + self.lebar_jalan if arah == "x" else posisi[1] + self.panjang_jalan * langkah)
        if simpul_berikutnya not in self.persimpangan: self.persimpangan.append(simpul_berikutnya)
        valid = [posisi[0] <= 0 and arah == "y", posisi[1] <= 0 and arah == "x", simpul_berikutnya[1] >= self.tinggi and arah == "x", posisi[0] >= self.tinggi and arah == "x"]
        simpul_berikutnya = (self.batasX(simpul_berikutnya[0]), self.batasY(simpul_berikutnya[1]))
        xsort, ysort = sort([posisi[0], simpul_berikutnya[0]]), sort([posisi[1], simpul_berikutnya[1]])
        if xsort[1] >= self.lebar or xsort[1] <= 0:
            self.persimpangan.append((self.batasX(xsort[1]), posisi[1]))
        if ysort[1] >= self.tinggi or ysort[1] <= 0:
            self.persimpangan.append((posisi[0] + 10, self.batasY(ysort[1])))
        if not sum(valid):
            self.gambar_peta.rectangle(((xsort[0], ysort[0]), (xsort[1], ysort[1])), "black")
            if arah == "y":
                self.gambar_peta.line(((xsort[0] + 10, ysort[0] + 10), (xsort[0] + 10, ysort[1] - 10)), "white", 1)
            else:
                self.gambar_peta.line(((xsort[0] + 20, ysort[0] + 10), (xsort[1] - 10, ysort[0] + 10)), "white", 1)

        nextX = self.lebar if simpul_berikutnya[0] <= 0 else (simpul_berikutnya[0] - (20 if arah == "y" else 0) if simpul_berikutnya[0] < self.lebar else 0)
        nextY = self.tinggi if simpul_berikutnya[1] <= 0 else (simpul_berikutnya[1] - (20 if arah == 'x' else 0) if simpul_berikutnya[1] < self.tinggi else 0)
        self.simpul_terakhir = (nextX, nextY)
        self.simpul_terakhir2 = posisi
        self.buatJalan((nextX, nextY), random.choice(["x", "y"]))

    def buatPeta(self):
        self.persimpangan = [(0, 0), (0, self.tinggi), (self.lebar, 0), (self.lebar, self.tinggi)]
        self.panjang = 0
        self.simpul_terakhir = (random.randrange(0, self.lebar, self.panjang_jalan), random.choice([0, self.tinggi]))
        self.simpul_terakhir2 = (random.randrange(0, self.lebar, self.panjang_jalan), random.choice([0, self.tinggi]))
        self.peta = Image.new("RGBA", (self.lebar, self.tinggi), (100, 100, 100))
        self.gambar_peta = ImageDraw.Draw(self.peta)
        self.buatJalan(self.simpul_terakhir, "y")
        self.peta.save("peta1.png")
        self.pemetaan()
        self.peta.save("peta2.png")
        return self.peta

    def buatBangunan(self, posisi):
        x = posisi[0][0]
        def dapatkanBangunanX(x):
            return [bangunan for bangunan in self.bangunan if bangunan.size[0] + x < posisi[1][0] - self.batas]

        def dapatkanBangunanY(x, y):
            return [bangunan for bangunan in self.lingkungan if bangunan.size[0] + x < posisi[1][0] - self.batas and bangunan.size[1] + y < posisi[1][1] - 50]

        while x < posisi[1][0]:
            kandidat = dapatkanBangunanX(x)
            if len(kandidat):
                bangun = random.choice(kandidat)
                self.gambar_peta.rectangle(((x, posisi[0][1]), (x + bangun.size[0] + 20, posisi[0][1] + bangun.size[1])), "green")
                self.peta.paste(bangun, (x, posisi[0][1]))
                x += bangun.size[0] + self.jarak
            else:
                break
        x = posisi[0][0]
        y = posisi[0][1] + 50 + self.batas
        while y < posisi[1][1] - 50:
            tertinggi = 50
            while x < posisi[1][0]:
                kandidat = dapatkanBangunanY(x, y)
                if len(kandidat):
                    bangun = random.choice(kandidat)
                    self.gambar_peta.rectangle(((x, y), (x + bangun.size[0] + 20, y + bangun.size[1])), "green")
                    self.peta.paste(bangun, (x, random.randint(y, y + (tertinggi - bangun.size[1]))))
                    tertinggi = max(bangun.size[1], tertinggi)
                    x += bangun.size[0] + self.batas
                else:
                    break
            y += tertinggi + self.batas
        x = posisi[0][0]

        if abs(posisi[1][1] - posisi[0][1]) < 120:
            return
        while x < posisi[1][0]:
            kandidat = dapatkanBangunanX(x)
            if len(kandidat):
                bangun = random.choice(kandidat)
                self.gambar_peta.rectangle(((x, posisi[1][1] - bangun.size[1]), (x + bangun.size[0] + 20, posisi[1][1] - bangun.size[1] + bangun.size[1])), "green")
                self.peta.paste(bangun, (x, posisi[1][1] - bangun.size[1]))
                x += bangun.size[0] + self.jarak
            else:
                break

    def pemetaan(self):
        teks = ["" for _ in range(len(self.persimpangan))]

        for idx, titik in enumerate(self.persimpangan):
            if titik[1] > self.tinggi:
                continue
            dekatX, dekatY = 0, 0
            for tetangga in self.persimpangan:
                if titik != tetangga and titik[0] > 0 and titik[1] > 0:
                    dekatX = tetangga[0] if (tetangga[0] > dekatX and tetangga[0] < titik[0] and titik[1] == tetangga[1]) else dekatX
                    dekatY = tetangga[1] if (tetangga[1] > dekatY and tetangga[1] < titik[1]) else dekatY
            if idx < len(teks) and teks[idx] != "":
                teks[idx] = ""

            if titik[1] == 1500:
                print(titik, ": ", dekatX, dekatY)
            if titik[0] - dekatX >= 30 and titik[1] - dekatY >= 30:
                if (titik[0], dekatY) not in self.persimpangan:
                    teks.append("aha")
                    self.persimpangan.append((titik[0], dekatY - 20))
                self.gambar_peta.rectangle(((dekatX + 10, dekatY + 10), (titik[0] - 10, titik[1] - 10)), "green")
                self.buatBangunan(((dekatX + 10, dekatY + 10), (titik[0] - 10, titik[1] - 10)))

petaSaya = Peta()
faktor_zoom = 1.0
LEBAR_AWAL = 500
TINGGI_AWAL = 400
lebar_viewport = 400
tinggi_viewport = 400
viewport_x = LEBAR_AWAL // 2 - (lebar_viewport // 2)
viewport_y = TINGGI_AWAL // 2 - (tinggi_viewport // 2)
peta_baru = None

def perbarui_peta():
    global peta_baru, label_peta
    peta_baru = petaSaya.buatPeta()
    print(petaSaya.persimpangan)
    peta_terpotong = peta_baru.crop((viewport_x, viewport_y, viewport_x + lebar_viewport, viewport_y + tinggi_viewport))
    peta_ubah_ukuran = peta_terpotong.resize((LEBAR_AWAL, TINGGI_AWAL))
    img_tk = ImageTk.PhotoImage(peta_ubah_ukuran)
    label_peta.config(image=img_tk)
    label_peta.image = img_tk
    perbarui()

def perbarui():
    global peta_baru
    peta_terpotong = peta_baru.crop((viewport_x * faktor_zoom, viewport_y * faktor_zoom, viewport_x * faktor_zoom + lebar_viewport * faktor_zoom, viewport_y * faktor_zoom + tinggi_viewport * faktor_zoom))
    peta_ubah_ukuran = peta_terpotong.resize((LEBAR_AWAL, TINGGI_AWAL))
    img_tk = ImageTk.PhotoImage(peta_ubah_ukuran)
    label_peta.config(image=img_tk)
    label_peta.image = img_tk

def perbesar():
    global faktor_zoom
    if faktor_zoom < 5.0:
        faktor_zoom += 0.1
        perbarui()

def perkecil():
    global faktor_zoom
    if faktor_zoom > 0.5:
        faktor_zoom -= 0.1
        perbarui()

def scroll(event):
    global viewport_x, viewport_y, faktor_zoom
    if event.delta > 0:
        if faktor_zoom > 0.5: faktor_zoom -= 0.1
    else:
        if faktor_zoom < 4.0:
            faktor_zoom += 0.1
    perbarui()

def saat_tombol_ditekan(event):
    global viewport_y, viewport_x
    if event.keysym == 'a':
        viewport_x -= 20
    elif event.keysym == 's':
        viewport_y += 20
    elif event.keysym == 'd':
        viewport_x += 20
    elif event.keysym == 'w':
        viewport_y -= 20
    perbarui()

root = tk.Tk()
root.title("Generator Peta")
root.bind("<MouseWheel>", scroll)
root.bind("<KeyPress-a>", saat_tombol_ditekan)
root.bind("<KeyPress-s>", saat_tombol_ditekan)
root.bind("<KeyPress-d>", saat_tombol_ditekan)
root.bind("<KeyPress-w>", saat_tombol_ditekan)
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_peta = ttk.Label(frame)
label_peta.grid(row=0, column=0, padx=10, pady=10)

tombol_generate = ttk.Button(root, text="Buat Peta", command=perbarui_peta)
tombol_generate.grid(row=1, column=0, pady=10)

perbarui_peta()
root.mainloop()
