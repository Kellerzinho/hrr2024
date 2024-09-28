import time
import cv2
from picamera import Camera  # Importar o módulo da PiCamera
from vision import process_image, detect_ball
from control import control_robot, recover_ball

def main():
    # Inicializar a câmera com resolução e framerate
    frame_width, frame_height = 640, 480  # Ajustar conforme a resolução da câmera
    camera = Camera(resolution=(frame_width, frame_height), framerate=32)

    # Loop principal para rastreamento da bola
    for image in camera.stream():  # Capturar imagens continuamente
        # Verifica se a captura de imagem foi bem-sucedida
        if image is None:
            print("Falha no stream da imagem.")
            continue

        # Processar a imagem para detectar a bola
        mask = process_image(image)

        # Detectar a posição da bola
        x, y, radius = detect_ball(mask)

        if x is not None and y is not None:
            # Se a bola for detectada, controlar o robô para centralizar a bola
            control_robot(x, y, frame_width, frame_height)
        else:
            # Se a bola não for detectada, tentar recuperar a visão da bola
            print("Bola fora de vista! Tentando recuperar...")
            recover_ball(image)

        # Exibir a imagem processada para depuração
        cv2.imshow('Ball Tracking', mask)

        # Verificar se o usuário pressionou a tecla 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Esperar um pequeno intervalo antes da próxima iteração
        time.sleep(0.1)

    # Encerrar a captura de vídeo e liberar recursos
    camera.stop_camera()  # Fechar a câmera
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
