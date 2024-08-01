import streamlit as st
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import re

# フォントファイルのパス
font_path = 'NotoSansCJKjp-Regular.otf'

# ディレクトリの作成
if not os.path.exists('known_faces'):
    os.makedirs('known_faces')

# 既知の顔データのロード
def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir('known_faces'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_path = os.path.join('known_faces', filename)
            img = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(img)
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(os.path.splitext(filename)[0])
    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_known_faces()

# 画像ファイルのアップロード
st.title("顔認識アプリ")
st.sidebar.title("メニュー")
menu = st.sidebar.selectbox("選択してください", ["顔認識", "顔の登録", "ウェブカメラで顔認証"])

def get_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

if menu == "顔認識":
    st.header("アップロードした画像から顔認識")
    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png"])

    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        font = get_font(font_path, 24)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=2)
            draw.text((left, top - 25), name, font=font, fill=(255, 0, 0, 255))

        st.image(pil_image, caption='認識結果', use_column_width=True)

elif menu == "顔の登録":
    st.header("顔の登録")
    registration_method = st.radio("登録方法を選択してください", ("画像をアップロード", "ウェブカメラで撮影"))
    name = st.text_input("名前をローマ字で入力してください")

    if registration_method == "画像をアップロード":
        uploaded_file = st.file_uploader("登録する顔画像をアップロードしてください", type=["jpg", "png"])

        if st.button("登録"):
            if uploaded_file is not None and name:
                if re.match("^[a-zA-Z\s]+$", name):
                    image = np.array(Image.open(uploaded_file))
                    face_locations = face_recognition.face_locations(image)
                    if face_locations:
                        img_path = f'known_faces/{name}.jpg'
                        Image.fromarray(image).save(img_path)
                        known_face_encodings, known_face_names = load_known_faces()
                        st.success(f"{name} を登録しました！")
                    else:
                        st.error("顔が検出されませんでした。")
                else:
                    st.error("名前はローマ字のみで入力してください。")
            else:
                st.error("画像と名前を入力してください。")

    elif registration_method == "ウェブカメラで撮影":
        if st.button("撮影開始"):
            cap = cv2.VideoCapture(0)
            stframe = st.empty()

            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("カメラが検出されませんでした。")
                    break

                stframe.image(frame, channels="BGR")

                if st.button("撮影"):
                    rgb_frame = frame[:, :, ::-1]
                    face_locations = face_recognition.face_locations(rgb_frame)
                    if face_locations:
                        img_path = f'known_faces/{name}.jpg'
                        Image.fromarray(rgb_frame).save(img_path)
                        known_face_encodings, known_face_names = load_known_faces()
                        st.success(f"{name} を登録しました！")
                        break
                    else:
                        st.error("顔が検出されませんでした。")
                        break

            cap.release()

elif menu == "ウェブカメラで顔認証":
    st.header("ウェブカメラで顔認証")
    if st.button("認証開始"):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            pil_frame = Image.fromarray(rgb_frame)
            draw = ImageDraw.Draw(pil_frame)
            font = get_font(font_path, 24)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=2)
                draw.text((left, top - 25), name, font=font, fill=(255, 0, 0, 255))

            stframe.image(np.array(pil_frame), channels="RGB")

        cap.release()
olumn_width=True)

if __name__ == "__main__":
    main()
