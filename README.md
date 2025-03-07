# Dashboard Streamlit Analisis Data Peminjaman Sepeda
## Deskripsi
Proyek ini berupa dashbord streamlit yang dikembangkan untuk memganalisis dataset bike-sharing, dataset ini memiliki dua dataset yang terdiri dari day_df dan hour_df. Dataset ini, telah disediakan oleh dicoding pada modul analisis data dengan Python. Sebelum mebuat dashboard perlu melakukan tahapan berikut :
### Data Wrangling
#### Gathering Data
Pada tahap ini melakukan persiapan dan pengumpulan data, dengan melakukan import library dan membaca berkas dataset yang akan dilakukan analisis
...
import pandas as pd

df = pd.read_csv("data.csv", delimiter=",")
#### Assessing Data
Pada tahap ini melakuakan pemeriksaan data, untuk mengetahui apakah ada missing value, nilai yang duplikat, ketidaksesuai tipe data dan lain sebagainya.
...
product_df.isnull().sum() // memeriksa apakah ada missing value
df.duplicated().sum() // memeriksa apakah terdapar duplikasi pada sebuah DataFrame
...
#### Cleaning Data
Pada Tahap ini melakukan pembersihan data dari tahap pemeriksaan data dengan melakukan
...
products_df.dropna(axis=0, inplace=True) //dropping
data.age.fillna(value=data.age.mean(), inplace=True) //imputation
data.close_price.interpolate(method='linear', limit_direction='forward', inplace=True) //interpolation
...
### Exploratory Analysis Data 
Melakukan eksplorasi terhadap data sebelum masuk kedalam tahap visualisasi data
### Visualization Data dan Explanatory Analysis Data
Melakukan visualisasi data dana analisis data dari hasil eksplorasi
## Membuat dan Mengaktifkan Virtual Environment
...
py -m venv main-ds
Set-ExecutionPolicy Unrestricted -Scope Process
main-ds\Scripts\Activate.ps1
...
## Instalasi 
...
#melakukan instalalsi streamlit
pip install streamlit babel
#melakukan instalasi library
pip install matplotlib
pip install seaborn
...
# Menjalankan Program 
...
streamlit run dashboard/dashboard.py
...
