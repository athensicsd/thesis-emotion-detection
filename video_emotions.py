import pandas as pd
from datetime import datetime
import cv2
from deepface import DeepFace
import os

video_paths = [
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/1.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/2.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/3.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/4.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/5.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/6.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/7.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/8.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/9.mp4",
    r"C:/Users/athin/Desktop/Face_Rec/sample23_splitted/10.mp4"
]

output_file = 'sample23_emotions.xlsx'
FRAME_STEP = 10 # αναλύω κάθε 10ο frame

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    
    for video_idx, video_path in enumerate(video_paths, 1):
        print(f"\nΕπεξεργασία βίντεο {video_idx} -> {video_path}")
        
        if not os.path.exists(video_path):
            print(" Το αρχείο δεν υπάρχει, το προσπερνάω.")
            continue
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(" Δεν μπόρεσα να ανοίξω το βίντεο, το προσπερνάω.")
            continue
        
        video_frames_data = []
        frame_number = 0
        analyzed_frames = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f" Τέλος βίντεο. Σύνολο raw frames: {frame_number}, αναλύθηκαν: {analyzed_frames}")
                break
            
            frame_number += 1

            # Πηδάμε frames για ταχύτητα
            if frame_number % FRAME_STEP != 0:
                continue
            
            try:
                result = DeepFace.analyze(
                    frame,
                    actions=['emotion'],
                    enforce_detection=False
                )

                if isinstance(result, list):
                    result = result[0]

                emotions = result['emotion']
                dominant_emotion = result['dominant_emotion']
                
                frame_data = {
                    'frame_number': frame_number,
                    'timestamp': datetime.now(),
                    'dominant_emotion': dominant_emotion,
                    'angry': emotions.get('angry'),
                    'disgust': emotions.get('disgust'),
                    'fear': emotions.get('fear'),
                    'happy': emotions.get('happy'),
                    'sad': emotions.get('sad'),
                    'surprise': emotions.get('surprise'),
                    'neutral': emotions.get('neutral')
                }
                
                video_frames_data.append(frame_data)
                analyzed_frames += 1

                if analyzed_frames % 50 == 0:
                    print(f" Βίντεο {video_idx}: αναλύθηκαν {analyzed_frames} frames (raw frame {frame_number})")
                
            except Exception as e:
                print(f" Σφάλμα στο frame {frame_number}: {e}")
                continue
        
        cap.release()
        
        df = pd.DataFrame(video_frames_data)
        sheet_name = f"Video_{video_idx}"[:31]
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"Αποθηκεύτηκε το βίντεο {video_idx} με {len(df)} γραμμές στο sheet '{sheet_name}'")

print(f"\nΌλα τα βίντεο αποθηκεύτηκαν στο {output_file}")