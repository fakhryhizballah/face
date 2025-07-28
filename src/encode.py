import os
import face_recognition
import numpy as np
import cv2

resutsFile = "./database"
fileImage = "./images"
def recognitionImage(filename, username):
    image_path = os.path.join(fileImage, filename)
    if not os.path.isfile(image_path):
        print(f"[ERROR] File {image_path} tidak ada")
        return
    print(f"[INFO] Memproses: {image_path}")
    image = face_recognition.load_image_file(image_path)
    # face_landmarks_list = face_recognition.face_landmarks(image)
    # print(face_landmarks_list)
    # return
    # Deteksi wajah dan ambil encoding
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
        print(f"[INFO] Ditemukan {len(encodings)} wajah")
        if len(encodings) == 1:
            face_encoding = encodings[0]  # Ambil wajah pertama saja
            face_encoding_path = os.path.join(resutsFile, f"{username}.npy")
            np.save(face_encoding_path, face_encoding)
            print(f"[OK] Encoding wajah disimpan di {face_encoding_path}")
            img_path = os.path.join(fileImage, f"{username}.jpg")
            face_location = face_recognition.face_locations(image, model="hog")[0]
            print(face_location)
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            cv2.imwrite(img_path, face_image)
            return
        else:
            print(f"[INFO] Ada lebih dari satu wajah di gambar")
            for idx, face_encoding in enumerate(encodings):
                face_encoding_path = os.path.join(resutsFile, f"{username}_{idx}.npy")
                np.save(face_encoding_path, face_encoding)
                print(f"[OK] Encoding wajah ke-{idx+1} disimpan di {face_encoding_path}")
                img_path = os.path.join(fileImage, f"{username}_{idx}.jpg")
                # face_location = face_recognition.face_locations(image, model="cnn")[idx]
                face_location = face_recognition.face_locations(image, model="hog")[idx]
                print(face_location)
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                cv2.imwrite(img_path, face_image)
                print(f"[OK] Gambar wajah ke-{idx+1} disimpan di {img_path}") 
            return
    else:
        print(f"[WARNING] Tidak ada wajah ditemukan di {filename}")
        return


def verifikasi(filename, username):
    image_path = os.path.join(fileImage, filename)
    if not os.path.isfile(image_path):
        print(f"[ERROR] File {image_path} tidak ada")
        return
    face_encoding_path = os.path.join(resutsFile, f"{username}.npy")
    if not os.path.isfile(face_encoding_path):
        print(f"[ERROR] File {face_encoding_path} tidak ada")
        return
    print(f"[INFO] Memproses: {image_path}")
    image = face_recognition.load_image_file(image_path)
    # Deteksi wajah dan ambil encoding
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
        print(f"[INFO] Ditemukan {len(encodings)} wajah")
        face_encoding = encodings[0]  # Ambil wajah pertama saja
        loaded_encoding = np.load(face_encoding_path)
        result = face_recognition.compare_faces([loaded_encoding], face_encoding, tolerance=0.4)
        print(result)
        if result[0]:
            print(f"[OK] Wajah cocok dengan {username}")
            return True
        else:
            print(f"[ERROR] Wajah tidak cocok dengan {username}")
            return False
    else:
        print(f"[WARNING] Tidak ada wajah ditemukan di {filename}")
        return
    return

def recognition(filename):
    image_path = os.path.join(fileImage, filename)
    if not os.path.isfile(image_path):
        print(f"[ERROR] File {image_path} tidak ada")
        return
    print(f"[INFO] Memproses: {image_path}")
    image = face_recognition.load_image_file(image_path)
    # Deteksi wajah dan ambil encoding
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
        print(f"[INFO] Ditemukan {len(encodings)} wajah")
        known_databases = []
        for idx, face_encoding in enumerate(encodings):
            for file in os.listdir(resutsFile):
                if file.endswith(".npy"):
                    # print(file)
                    face_encoding_path = os.path.join(resutsFile, file)
                    loaded_encoding = np.load(face_encoding_path)
                    results = face_recognition.compare_faces([loaded_encoding], face_encoding, tolerance=0.5)
                    # print(results)
                    if results[0]:
                        name = os.path.splitext(file)[0] 
                        print(f"[OK] Wajah cocok dengan {name}")
                        known_databases.append(name)
        print(known_databases)
        return known_databases


    else:
        print(f"[WARNING] Tidak ada wajah ditemukan di {filename}")
        return