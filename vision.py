import cv2
import numpy as np

# Função para processar a imagem e aplicar uma máscara baseada na cor da bola
def process_image(image):
    """
    Aplica um filtro de cor para detectar a bola em uma imagem.

    Args:
        image (numpy array): Imagem no formato BGR capturada pela GoPro.

    Returns:
        mask (numpy array): Máscara binária que destaca a bola na imagem.
    """
    # Converter a imagem de BGR para HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir o intervalo de cores para a bola laranja (ajuste conforme necessário)
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])

    # Criar uma máscara que isola a cor laranja
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Aplicar suavização para reduzir o ruído
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    return mask

# Função para detectar a bola com base na máscara gerada
def detect_ball(mask):
    """
    Detecta a bola usando a máscara e retorna suas coordenadas e raio.

    Args:
        mask (numpy array): Máscara binária que destaca a bola.

    Returns:
        x (int or None): Coordenada X do centro da bola (ou None se não encontrada).
        y (int or None): Coordenada Y do centro da bola (ou None se não encontrada).
        radius (float or None): Raio da bola detectada (ou None se não encontrada).
    """
    # Detectar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Encontrar o maior contorno, assumindo que seja a bola
        largest_contour = max(contours, key=cv2.contourArea)

        # Verificar se o contorno é grande o suficiente para ser considerado uma bola
        if cv2.contourArea(largest_contour) > 100:  # Ajuste este valor conforme necessário
            # Encontrar o círculo mínimo que envolve o contorno
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            return int(x), int(y), radius

    return None, None, None
