import streamlit as st
import face_recognition
import cv2
import numpy as np
from PIL import Image
import io

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.equalizeHist(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image

def get_face_encoding(image):
    try:
        image = preprocess_image(image)
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            return face_encodings[0]
        else:
            st.warning("Error: No faces found in the image")
            return None
    except Exception as e:
        st.error(f"Exception occurred while processing image: {e}")
        return None

def main():
    st.title("顔認識アプリケーション")

    # 既知の顔画像をアップロード
    known_images = []
    known_names = []

    uploaded_files = st.file_uploader("既知の顔画像をアップロード", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            image = Image.open(io.BytesIO(bytes_data))
            st.image(image, caption=f"既知の顔画像: {uploaded_file.name}", use_column_width=True)
            known_face_encoding = get_face_encoding(np.array(image))

            if known_face_encoding is not None:
                known_images.append(known_face_encoding)
                known_names.append(st.text_input(f"名前を入力: {uploaded_file.name}", value="Unknown"))

    # ウェブカメラで写真を撮影
    if st.button("ウェブカメラで写真を撮影"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, caption="ウェブカメラで撮影した画像", use_column_width=True)

            # 一時的に画像を保存して顔認識
            image_to_check = frame_rgb
            image_to_check = preprocess_image(image_to_check)
            face_locations = face_recognition.face_locations(image_to_check)
            face_encodings = face_recognition.face_encodings(image_to_check, face_locations)

            if len(face_locations) == 0 or len(face_encodings) == 0:
                st.warning("Error: No faces found in the webcam image.")
            else:
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(known_images, face_encoding, tolerance=0.5)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_images, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]

                    # 結果を表示
                    st.write(f"Found {name} at ({top}, {right}, {bottom}, {left})")

                    # 結果を画像に描画
                    cv2.rectangle(frame_rgb, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame_rgb, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                st.image(frame_rgb, caption="認識結果", use_column_width=True)

if __name__ == "__main__":
    main()
