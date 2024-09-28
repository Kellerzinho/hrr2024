from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

class Camera:
    def __init__(self, resolution=(640, 480), framerate=32):
        """
        Inicializa a PiCamera com a resolução e framerate especificados.

        Args:
            resolution (tuple): Resolução da câmera (largura, altura).
            framerate (int): Taxa de quadros por segundo da câmera.
        """
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        
        # Dar tempo para a câmera inicializar
        time.sleep(0.1)

    def capture_frame(self):
        """
        Captura uma única imagem da PiCamera e a retorna em formato BGR.

        Returns:
            frame (numpy array): Imagem capturada pela câmera no formato BGR.
        """
        self.raw_capture.truncate(0)  # Limpar o buffer anterior
        self.camera.capture(self.raw_capture, format="bgr")
        frame = self.raw_capture.array  # Captura a imagem em formato numpy array
        return frame

    def stream(self):
        """
        Inicia o stream da PiCamera, permitindo capturar frames continuamente.

        Yields:
            frame (numpy array): Frame capturado em tempo real no formato BGR.
        """
        for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            image = frame.array  # Captura a imagem no formato numpy array
            yield image  # Retorna a imagem capturada
            
            # Limpar o buffer de captura para o próximo frame
            self.raw_capture.truncate(0)

    def stop_camera(self):
        """
        Para a câmera e fecha os recursos.
        """
        self.camera.close()
