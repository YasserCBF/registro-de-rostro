import cv2
import os
import numpy as np

def register_user(username):
    """Registra un nuevo usuario tomando su foto."""
    if not os.path.exists('registered_users'):
        os.makedirs('registered_users')

    video_capture = cv2.VideoCapture(0)
    print("Coloca tu rostro frente a la cámara para registrarte.")

    ret, frame = video_capture.read()
    video_capture.release()

    if ret:
        cv2.imwrite(f'registered_users/{username}.jpg', frame)
        print(f"Usuario {username} registrado con éxito.")
    else:
        print("Error al capturar la imagen. Asegúrate de que la cámara esté funcionando.")

def login_user(username):
    """Inicia sesión verificando el rostro del usuario."""
    image_path = f'registered_users/{username}.jpg'
    
    if not os.path.exists(image_path):
        print("Error: La imagen registrada no existe.")
        return False

    registered_image = cv2.imread(image_path)
    
    if registered_image is None:
        print("Error: No se pudo cargar la imagen registrada.")
        return False

    registered_gray = cv2.cvtColor(registered_image, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    registered_faces = face_cascade.detectMultiScale(registered_gray, scaleFactor=1.1, minNeighbors=5)
    
    if len(registered_faces) == 0:
        print("No se pudo detectar el rostro registrado.")
        return False

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Error al capturar el video. Asegúrate de que la cámara esté funcionando.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        current_faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        if len(current_faces) == 0:
            print("No se detectó ningún rostro. Intenta nuevamente.")
            continue

        for (x, y, w, h) in current_faces:
            current_face = gray_frame[y:y+h, x:x+w]
            registered_face = registered_gray[registered_faces[0][1]:registered_faces[0][1]+registered_faces[0][3], 
                                               registered_faces[0][0]:registered_faces[0][0]+registered_faces[0][2]]

            if current_face.shape == registered_face.shape:
                difference = cv2.absdiff(current_face, registered_face)
                if np.sum(difference) < 100000:  # Umbral para determinar si son iguales
                    print("Acceso concedido")
                    video_capture.release()
                    return True

        print("Acceso denegado")

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def main():
    """Función principal que ejecuta el menú de login."""
    while True:
        print("\n--- Menú de Login ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        choice = input("Elige una opción (1/2/3): ")

        if choice == '1':
            username = input("Introduce un nombre de usuario para registrarte: ")
            register_user(username)
        elif choice == '2':
            username = input("Introduce tu nombre de usuario para iniciar sesión: ")
            login_user(username)
        elif choice == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, elige nuevamente.")

if __name__ == "__main__":
    main()