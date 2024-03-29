# ML-API-IHZ

# Instalasi Python

Pastikan sudah terinstall python dan pip dalam system anda, jika system anda mengunakan linux
bisa mengikuti command di bawah ini

`
sudo apt install python3-pip
`

jika system mengunakan OS windows atau yang lain bisa minjau situs resmi python untuk instalasi python
https://www.python.org/downloads/

# Instalasi Dependency 
Agar code dapat berjalan di perlukan beberapa dependecy, dapat langsung menjalankan command di terminal 
berikut satu demi satu jika python dan pip sudah terinstall

```
pip install fastapi
pip install uvicorn[standard]
pip install scikit-learn
```

# Menjalankan API
untuk menjalankan API cukup mejalankan command berikut di terminal
```
uvicorn main:app --reload
```

secara default dia akan jalan secara lokal di 127.0.0.1 dengan port 8000 
Output jika runnning berhasil
![image](/Hasil_Running.png) 

jika ingin di jalankan di port dan address host yang berbeda bisa mengunakan option --host dan --port
```
uvicorn --host [host address] --port [nilai port]  main:app --reload 
```

contoh hasil running mengunakan port dan address host yang berbeda

![image](/Hasil_Running_2.png)  


# Mengganti Model
untuk mengganti model, cukup rename pada main.py model pkl yang diinginkan 
```
clf = pickle.load(open('.\nama_model.pkl', 'rb'))
```

secara default akan menjalankan model file model_minimal_samples_5000.pkl 
Snipshoot codenya
```
#? Loading Model dan Nama attribute
clf = pickle.load(open('.\model_minimal_samples_5000.pkl', 'rb'))
feature_names = ['network_onu_pwr_spl', 'network_onu_temp', 'network_onu_bias_curr',
			 'network_onu_rx_pwr', 'network_onu_tx_pwr', 'network_olt_pwr_spl',
			 'network_olt_temp', 'network_olt_bias_curr', 'network_olt_tx_pwr',
			 'network_olt_rx_pwr']
```

jika ingin mengubah modelnya ke model lain, hanya mengubah sesuai nama file modelnya. Contoh
```
#? Loading Model dan Nama attribute
clf = pickle.load(open('.\model_without_minimal_samples.pkl', 'rb'))
feature_names = ['network_onu_pwr_spl', 'network_onu_temp', 'network_onu_bias_curr',
			 'network_onu_rx_pwr', 'network_onu_tx_pwr', 'network_olt_pwr_spl',
			 'network_olt_temp', 'network_olt_bias_curr', 'network_olt_tx_pwr',
			 'network_olt_rx_pwr']
```

# Menggunakan API
untuk mengunakan API bisa dengan menyiapkan body parameternya berupa format JSON dengan format seperti berikut
```
{
    "tx_olt": 0,
    "tx_onu": 0,
    "rx_olt": 0,
    "rx_onu": 0,
    "temp_olt": 0,
    "temp_onu": 0,
    "pwrspl_olt": 0,
    "pwrspl_onu": 0,
    "bias_olt": 0,
    "bias_onu": 0
}
```

dan untuk URL API mengunakan format sebagai berikut

```
http://[Host]:[Port]/predict
```

dan request method yang digunakan adalah **PUT**
API akan mengembalikan JSON juga dengan dua tipe format, yaitu format jika statusnya ONLINE dan format jika statusnya OFFLINE
yang membedakan utama hanya saat di OFFLINE dimana akan memberikan array of string yang menyatakan permasalahnya dimana

## Hasil return API saat mengklasifikasi ONLINE
```
{
    "Status": "ONLINE"
}
```
## Hasil return API saat mengklasifikasi OFFLINE
```
{
    "Status": "OFFLINE",
    "Info": [
        "- network_onu_bias_curr: 0.0 <= 0.5",
        "- network_olt_rx_pwr: -22.0 > -62.39104461669922",
        "- network_onu_tx_pwr: -22.0 <= 2.062000036239624"
    ]
}
```

## Contoh mengunakan POSTMAN
### Saat ONLINE
![image](https://user-images.githubusercontent.com/46880550/120590764-45663800-c465-11eb-9a2c-799044e827dd.png)
### Saat OFFLINE
![image](https://user-images.githubusercontent.com/46880550/120592052-63349c80-c467-11eb-98f1-f5b49c5a8947.png)


## Contoh mengunakan javascript dengan XMLHttpRequest
```
var xhttp = new XMLHttpRequest();

xhttp.onreadystatechange = function () {
  if (this.readyState == 4 && this.status == 200) {
    console.log(JSON.parse(this.responseText));
  }
};

data = {
    "tx_olt": -33,
    "tx_onu": -22,
    "rx_olt": -22,
    "rx_onu": -22,
    "temp_olt": 50,
    "temp_onu": 50,
    "pwrspl_olt": 1,
    "pwrspl_onu": 1,
    "bias_olt": 1,
    "bias_onu": 1
};

xhttp.open("PUT", "http://192.168.100.41:8000/predict", true);
xhttp.send(JSON.stringify(data));
```





