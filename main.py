import pickle
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Data(BaseModel):
		tx_olt: float
		tx_onu: float

		rx_olt: float
		rx_onu: float

		temp_olt: float
		temp_onu: float

		pwrspl_olt: float
		pwrspl_onu: float

		bias_olt: float
		bias_onu: float

#? fungsi untuk mengebalikan hasil decision 
def show_path(clf, data, feature_names):
	n_nodes = clf.tree_.node_count
	children_left = clf.tree_.children_left
	children_right = clf.tree_.children_right
	feature = clf.tree_.feature
	threshold = clf.tree_.threshold

	node_indicator = clf.decision_path([data])

	leave_id = clf.apply([data])

	sample_id = 0
	node_index = node_indicator.indices[node_indicator.indptr[sample_id]:node_indicator.indptr[sample_id + 1]]

	result = []
	for node_id in node_index[:-1]:
		if leave_id[sample_id] != node_id:	# <-- changed != to ==
			if (data[feature[node_id]] <= threshold[node_id]): 
				threshold_sign = "<="
			else: 
				threshold_sign = ">"
			result.append(f"- {feature_names[feature[node_id]]}: {data[feature[node_id]]} {threshold_sign} {threshold[node_id]}")

	return result

#? Loading Model dan Nama attribute
clf = pickle.load(open('.\Klasifikasi_Koneksi_DT_v3.pkl', 'rb'))
feature_names = ['network_onu_pwr_spl', 'network_onu_temp', 'network_onu_bias_curr',
			 'network_onu_rx_pwr', 'network_onu_tx_pwr', 'network_olt_pwr_spl',
			 'network_olt_temp', 'network_olt_bias_curr', 'network_olt_tx_pwr',
			 'network_olt_rx_pwr']

@app.get("/")
def read_root(text):
    return {"Hello": text}

@app.put("/predict")
def read_item(data: Data):

		#? object data di rubah menjadi array 
		data_arr = [data.pwrspl_onu, data.temp_onu, data.bias_onu, data.rx_onu, data.tx_onu,
								data.pwrspl_olt, data.temp_olt, data.bias_olt, data.tx_olt, data.rx_olt]

		#? diprediksi mengunakan model yang sudah di import						
		prediksi = clf.predict([data_arr])

		#? Jika hasil prediksinya 1 maka akan kembalikan status ONLINE
		if (prediksi == 1):
			return { "Status" : "ONLINE"}

		#? Jika hasil prediksi 0 maka akan dikemalikan Status OFFLINE dan
		#? attribute yang membuatnya OFFLINE	
		else:
			path = show_path(clf,data_arr,feature_names)
			return { "Status" : "OFFLINE", "Info" : path}
