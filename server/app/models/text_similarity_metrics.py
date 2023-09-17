from cdifflib import CSequenceMatcher
from django.conf import settings
import pandas as pd
import os

def similar(str1, str2):
	return CSequenceMatcher(None, str1, str2).ratio()

def get_prob_label(text):
	max_prob = {'porb' : -1, 'label' : ''}
	static_text_data = pd.read_csv(os.path.join(settings.PROCESSED_DATA_DIR, 'static_text.csv'))
	print(static_text_data)
	for _, row in static_text_data.iterrows():
		similarity = similar(str(text).lower(), str(row['question']).lower())
		print('Similarity : ', similarity)
		if similarity >= (80/100) and similarity > max_prob['porb']:
			max_prob['porb'] = similarity
			max_prob['label'] = row['label']
	return max_prob
