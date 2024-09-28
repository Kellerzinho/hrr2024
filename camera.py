import cv2
import urllib.request
import numpy as np

# URL do stream de vídeo da GoPro (ajuste para o modelo e configuração da GoPro)
# Normalmente a GoPro usa algo como http://10.5.5.9:8080/live/amba.m3u8 ou http://10.5.5.9:8080/live/amba.jpg
GOPRO_IP = "10.5.5.9"
STREAM_URL = f"http://{GOPRO_IP}:8080/live/amba.jpg"

def capture_image():
    try:
        # Abrir URL da GoPro e obter imagem
        with urllib.request.urlopen(STREAM_URL) as response:
            image_data = response.read()

        # Converter bytes da imagem para um formato legível pelo OpenCV
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return image  # Retorna a imagem no formato BGR
    except Exception as e:
        print(f"Erro ao capturar imagem da GoPro: {e}")
        return None
