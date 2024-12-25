"""
Este módulo define un servidor Flask que ofrece un endpoint para detectar emociones en un texto.
El texto es procesado mediante la función 'emotion_detector' y devuelve un análisis 
de las emociones detectadas o un mensaje de error.
"""

from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector  # Importa tu función personalizada

# Inicializa la aplicación Flask
app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_endpoint():
    """
    Endpoint para detectar la emoción en un texto proporcionado en una solicitud POST.
    Retorna el análisis de las emociones detectadas o un mensaje de error.
    """

    # Verificar si el cuerpo de la solicitud es válido
    data = request.get_json()

    # Comprobar si no hay datos o si falta el campo "text"
    if not data or "text" not in data:
        return jsonify({"output": "Texto inválido. Por favor, intenta de nuevo."}), 400

    text = data["text"]

    # Manejar entradas vacías
    if not text.strip():
        return jsonify({"output": "Texto inválido. Por favor, intenta de nuevo."}), 400

    # Obtener el resultado del detector de emociones
    result = emotion_detector(text)

    # Manejar casos donde la emoción dominante es None
    if result.get("dominant_emotion") is None:
        return jsonify({"output": "No se pudo detectar ninguna emoción. Intenta de nuevo."}), 400

    # Construir el mensaje de respuesta
    response_message = (
        f"Para la frase dada, las respuestas del sistema son: "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']}, 'sadness': {result['sadness']}. "
        f"La emoción dominante es '{result['dominant_emotion']}'."
    )

    return jsonify({"output": response_message})

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
