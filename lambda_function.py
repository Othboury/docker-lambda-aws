# Define imports
try:
    import unzip_requirements
except ImportError:
    pass

import json
from io import BytesIO
import time
import os

import boto3
import numpy as np
import librosa

from network.Transformer import Transformer

from keras.models import load_model
from tensorflow import keras

#Function to extract the features of an audio file
def features_extractor(file):
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    
    return mfccs_scaled_features

#Function to upload the classification model from the S3 bucket
def loadModel(bucket:str, key:str):
    s3 = boto3.client('s3')
    with BytesIO() as f:
        s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=f)
        f.seek(0)
        loaded_model = load_model(f)
    return loaded_model
 
#The lambda_function that calls the other fucntions and do the prediction
def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    bucket_name = event['Records'][0]['s3']['bcuket']['name']
    key = event['Records'][0]['s3']['object']['key']
    key = urllib.parse.unquote_plus(key, encoding = 'utf-8')
    
    message = 'This file got uploaded ' + key + 'to this bucket ' + bucket_name
    print(message)
    
    file = s3_client.get_object(Bucket = bucket_name, Key=key)
    logger.info('Extracting features...')
    mfccs_scaled_features = features_extractor(file)
    mfccs_scaled_features = mfccs_scaled_features.reshape(1,-1)
    logger.info('Features extracted...')
    logger.info('Loading model from file...')
    loaded_model = loadModel( bucket_name, "model/mosquito_classification_model.h5")
    logger.info('Model loaded from file...')
    logger.info(f'Performing predictions...')
    predicted_label=loaded_model.predict(mfccs_scaled_features)
    classes_x=np.argmax(predicted_label,axis=1)
    prediction_class = labelencoder.inverse_transform(classes_x)
    
    response = json.dumps(predictions.tolist())

    return {
        'statusCode': 200,
        'headers':{
            'Content-type':'application/json'
        },
        'body': response
    }
    
