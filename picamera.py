import time
import cv2
from picamera2 import Picamera2, Preview

class Camera:
    def __init__(self, resolution=(640, 480), framerate=32):
        """
        Inicializa a Picamera2 com a resolução e framerate especificados.

        Args:
            resolution (tuple): Resolução da câmera (largura, altura).
            framerate (int): Taxa de quadros por segundo da câmera.
        """
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"format": 'RGB888', "size": resolution}))
        
        # Começar a visualização (opcional)
        self.camera.start_preview(Preview.QTGL)
        
        # Dar tempo para a câmera inicializar
        time.sleep(1)  # Aumentei o tempo para a inicialização

    def capture_frame(self):
        """
        Captura uma única imagem da Picamera2 e a retorna em formato BGR.

        Returns:
            frame (numpy array): Imagem capturada pela câmera no formato BGR.
        """
        # Captura uma única imagem
        frame = self.camera.capture_array()
        return frame  # Retorna a imagem capturada em formato numpy array

    def stream(self):
        """
        Inicia o stream da Picamera2, permitindo capturar frames continuamente.

        Yields:
            frame (numpy array): Frame capturado em tempo real no formato BGR.
        """
        while True:
            frame = self.camera.capture_array()  # Captura o frame em formato numpy array
            yield frame  # Retorna a imagem capturada

    def stop_camera(self):
        """
        Para a câmera e fecha os recursos.
        """
        self.camera.close()