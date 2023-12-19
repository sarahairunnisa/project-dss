# Import modul sqrt dari library math dan modul re
from math import sqrt
import re

# Definisi kelas Topsis
class Topsis:
    # Konstruktor untuk inisialisasi objek Topsis
    def __init__(self, data, weights, impacts) -> None:
        self.data = data
        # Dictionary untuk memetakan nama fitur dengan nama kolom dalam dataset
        self.features = {
            'Processor': 'Processor',
            'Screen': 'Screen',
            'InternalMemory': 'InternalMemory',
            'TotalStorage': 'TotalStorage',
            'Weight': 'Weight',
            'BatteryCells': 'BatteryCells',
        }
        self.weights = weights  # Bobot untuk setiap fitur
        self.impacts = impacts  # Dampak (1 atau 0) untuk setiap fitur
        self.ideal = {}  # Dictionary untuk nilai ideal
        self.negativeIdeal = {}  # Dictionary untuk nilai ideal negatif

    # Fungsi untuk menghitung jarak Euclidean dari suatu data
    def euclideanDistance(self, data) -> float:
        return sqrt(sum([i ** 2 for i in data]))

    # Fungsi untuk normalisasi data
    def normalize(self) -> None:
        for key, value in self.features.items():
            # Menambahkan kolom normalized untuk setiap fitur dalam dataset
            self.data[value + 'Normalized'] = self.data[key] / self.euclideanDistance(self.data[key])
            self.data[value + 'Normalized'] *= self.weights[list(self.features.keys()).index(key)]

    # Fungsi untuk mencari nilai ideal dan nilai ideal negatif
    def idealNegativeSolution(self) -> None:
        for key, value in self.features.items():
            if self.impacts[list(self.features.keys()).index(key)] == 1:
                self.ideal[value] = self.data[value + 'Normalized'].max()
                self.negativeIdeal[value] = self.data[value + 'Normalized'].min()
            elif self.impacts[list(self.features.keys()).index(key)] == 0:
                self.ideal[value] = self.data[value + 'Normalized'].min()
                self.negativeIdeal[value] = self.data[value + 'Normalized'].max()
    
    # Fungsi untuk menghitung ukuran pemisahan
    def separationMeasures(self) -> None:
        for _, value in self.features.items():
            # Menambahkan kolom untuk ukuran pemisahan terhadap nilai ideal dan nilai ideal negatif
            self.data[value + 'SeparationMeasureIdeal'] = pow(self.data[value + 'Normalized'] - self.ideal[value], 2)
            self.data[value + 'SeparationMeasureNegativeIdeal'] = pow(self.data[value + 'Normalized'] - self.negativeIdeal[value], 2)
        
        # Menambahkan kolom total ukuran pemisahan untuk nilai ideal dan nilai ideal negatif
        self.data['SeparationMeasureIdeal'] = self.data[[f'{value}SeparationMeasureIdeal' for value in self.features.values()]].sum(axis=1)
        self.data['SeparationMeasureNegativeIdeal'] = self.data[[f'{value}SeparationMeasureNegativeIdeal' for value in self.features.values()]].sum(axis=1)

        # Menghitung akar kuadrat dari total ukuran pemisahan
        self.data['SeparationMeasureIdeal'] = self.data['SeparationMeasureIdeal'].apply(sqrt)
        self.data['SeparationMeasureNegativeIdeal'] = self.data['SeparationMeasureNegativeIdeal'].apply(sqrt)

    # Fungsi untuk menghitung skor kinerja
    def performanceScore(self) -> None:
        # Menambahkan kolom totalRelativeCloseness yang merupakan hasil perhitungan skor kinerja
        self.data['totalRelativeCloseness'] = self.data['SeparationMeasureNegativeIdeal'] / (self.data['SeparationMeasureIdeal'] + self.data['SeparationMeasureNegativeIdeal'])

    # Fungsi untuk meranking data
    def rank(self) -> None:
        # Meranking data berdasarkan totalRelativeCloseness secara menurun
        self.data = self.data.sort_values(by=['totalRelativeCloseness'], ascending=False)

    # Fungsi untuk menjalankan seluruh algoritma TOPSIS
    def run(self) -> None:
        # Menambahkan kolom OriginalIndex untuk menyimpan indeks awal sebelum dilakukan pengurutan
        self.data['OriginalIndex'] = range(len(self.data))
        # Memanggil fungsi-fungsi yang diperlukan
        self.normalize()
        self.idealNegativeSolution()
        self.separationMeasures()
        self.performanceScore()
        self.rank()
        # Menghapus kolom OriginalIndex setelah pengurutan
        self.data = self.data.drop(columns=['OriginalIndex'])

    # Fungsi untuk mendapatkan nama laptop yang direkomendasikan
    def getName(self) -> None:
        name = []
        for i in range(15):
            # Mengambil 15 nama laptop teratas setelah pengurutan
            name.append(self.data['Name'].iloc[i])
        return name
    
    # Fungsi untuk mendapatkan URL gambar laptop yang direkomendasikan
    def getEmbed(self) -> None:
        embed = []
        for i in range(15):
            # Mengambil 15 URL gambar laptop teratas setelah pengurutan
            embed.append(self.data['ImageURLs'].iloc[i])
        return embed
    
    # Fungsi untuk mendapatkan persentase relative closeness untuk 15 laptop teratas
    def getPercentage(self) -> None:
        return self.data['totalRelativeCloseness'].iloc[0:15]

