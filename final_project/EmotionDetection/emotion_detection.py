import requests
import json

def emotion_detector(text_to_analyze):# Manejo de entradas vacías
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = json.dumps({"raw_document": {"text": text_to_analyze}})
    try:# Realizar la solicitud POST
        response = requests.post(url, headers=headers, data=input_json)# Manejar el caso de código de estado 400
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }# Lanzar excepciones para otros errores HTTP
        response.raise_for_status()# Procesar la respuesta
        response_dict = response.json()
        emotions = response_dict['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotions, key=emotions.get)
        return {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness'],
            'dominant_emotion': dominant_emotion
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en la solicitud: {e}"}