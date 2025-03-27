import tkinter as tk
from tkinter import messagebox
import os
from pylsl import StreamInfo, StreamOutlet
from PIL import Image, ImageTk
import time
import threading
import cv2
from datetime import datetime
import pygame
import ctypes
from sys import platform

pygame.mixer.init()  # Αρχικοποίηση του mixer

stop_recording = False  # Αρχικοποίηση του flag

# Αρχικοποίηση του παραθύρου Tkinter
root = tk.Tk()
root.title("Ανίχνευση Συναισθημάτων σε Έργα Τέχνης")

# Λίστα των αρχείων εικόνας
images = [
    "C:/Users/athin/Desktop/Diplomatikh/1.Wanderer above the sea of fog (Δέος).png",
    "C:/Users/athin/Desktop/Diplomatikh/2. In the time of Harmony (Απόλαυση).png",
    "C:/Users/athin/Desktop/Diplomatikh/3. The dream of the fisherman's wife (Έκπληξη).png",
    "C:/Users/athin/Desktop/Diplomatikh/4. The Lovers (Συγκίνηση).png",
    "C:/Users/athin/Desktop/Diplomatikh/5. Flaming June (Ηρεμία).png",
    "C:/Users/athin/Desktop/Diplomatikh/6. Campbell's Soup Cans (Απάθεια).png",
    "C:/Users/athin/Desktop/Diplomatikh/7. Saturn Devouring His son (Αηδία).png",
    "C:/Users/athin/Desktop/Diplomatikh/8. Woman with dead child (Θλίψη).png",
    "C:/Users/athin/Desktop/Diplomatikh/9. The Deep (Φόβος).png",
    "C:/Users/athin/Desktop/Diplomatikh/10. The guitar lesson (θυμός).png"
]

# Επιλογές συναισθημάτων
emotions = ["Συγκίνηση", "Ηρεμία", "Φόβος", "Δέος", "Απόλαυση", "Θυμός", "Απάθεια", "Αηδία", "Έκπληξη", "Θλίψη"]

# Λίστα με τα κείμενα
texts = [
"Τίτλος: Wanderer above the sea of fog\n\nΚαλλιτέχνης: Caspar David Friedrich\n\n(Λάδι σε καμβά 98,4 εκ. Χ 74,8 εκ.)",
"Τίτλος: In the Time of Harmony: the Golden Age is not in the Past, it is in the Future\n\nΚαλλιτέχνης: Paul Signac\n\n(Λάδι σε καμβά: 310 εκ. Χ 410 εκ.)",
"Τίτλος: The Dream of the Fisherman's Wife\n\nΚαλλιτέχνης: Hokusai\n\n(Χαρακτικό- Ξυλογραφία: 19 εκ. Χ 27 εκ.)",
"Τίτλος:The Lovers II\n\nΚαλλιτέχνης:Rene Magritte\n\n(Λάδι σε καμβά: 54 εκ. Χ 73,4 εκ.)",
"Τίτλος: Flaming June\n\nΚαλλιτέχνης:Frederic Leighton\n\n(Λάδι σε καμβά 120 εκ. Χ 120 εκ.)",
"Τίτλος:Campbell's Soup Cans\n\nΚαλλιτέχνης:Andy Warhol\n\n(Πολύπτυχο. 32 πίνακες. Ακρυλικό με μεταλλικό σμάλτο σε καμβά 51εκ. Χ 41 εκ.)",
"Τίτλος:Saturn Devouring His Son\n\nΚαλλιτέχνης:Francisco Goya\n\n(Ελαιογραφία σε τοίχο. 146 εκ. Χ 83 εκ.)",
"Τίτλος:Woman with dead child\n\nΚαλλιτέχνης:Kathe kollwitz\n\n(Χαρακτικό- Λιθογραφία: 54,5 εκ. Χ 70 εκ.) ",
"Τίτλος:The Deep\n\nΚαλλιτέχνης:Jackson Pollock\n\n(Σμάλτα και χρώματα λαδιού σε καμβά: 150,2 εκ. Χ 220.4 εκ.)",
"Τίτλος:The Guitar Lesson\n\nΚαλλιτέχνης:Balthus\n\n(Λάδι σε καμβά: 161,3 εκ. Χ 138,4 εκ.)"
]

audio_files = [
    "C:/Users/athin/Desktop/Diplomatikh/01 Caspar David Friedrich.wav",
    "C:/Users/athin/Desktop/Diplomatikh/02 Paul Signac.wav",
    "C:/Users/athin/Desktop/Diplomatikh/03 Hokusai.wav",
    "C:/Users/athin/Desktop/Diplomatikh/04 Rene Magritte.wav",
    "C:/Users/athin/Desktop/Diplomatikh/05 Frederic Leighton.wav",
    "C:/Users/athin/Desktop/Diplomatikh/06 Andy Warhol.wav",
    "C:/Users/athin/Desktop/Diplomatikh/07 Francisco Goya.wav",
    "C:/Users/athin/Desktop/Diplomatikh/08 kathe kollwitz.wav",
    "C:/Users/athin/Desktop/Diplomatikh/09 Jackson Pollock.wav",
    "C:/Users/athin/Desktop/Diplomatikh/10c Balthus.wav"
]

# Stream για συναισθήματα
emotion_info = StreamInfo("EmotionStream", "Markers", 2, 0, 'string', "emotion_stream_id")
emotion_outlet = StreamOutlet(emotion_info)
print("EmotionStream δημιουργήθηκε.")

# Stream για face detection
face_info = StreamInfo("FaceStream", "Markers", 2, 0, 'string', "face_stream_id")
face_outlet = StreamOutlet(face_info)
print("FaceStream δημιουργήθηκε.")



#------------------------------------------------------------------------ΓΡΑΦΙΚΑ part 1------------------------------------------------------------------------------#

# Χρώμα για τη γραμμή τίτλου 
title_bar_color = "#1E1E1E"  

if platform == "win32":
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())  # Παίρνουμε το handle του παραθύρου
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 36, ctypes.byref(ctypes.c_int(int(title_bar_color.replace("#", "0x"), 16))), ctypes.sizeof(ctypes.c_int))

# Dark Theme Colors
bg_color = "#1E1E1E"  #  background 
bg_frames = "#252526"  #  για τα frames
fg_color = "#FFFFFF"  # γραμματοσειρα
btn_bg = "#333333"  #  κουμπιά
btn_fg = "#FFFFFF"  # γράμματα στα κουμπιά
hover_bg = "#444444"  # Χρώμα hover για κουμπιά
root.configure(bg=bg_color)
custom_font = ("Poppins", 12, "bold") # Ορισμός γραμματοσειράς

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# ΑΠΟΘΗΚΕΥΣΗ ΔΕΔΟΜΕΝΩΝ + ΑΠΟΣΤΟΛΗ ΣΤΟ LSL 

from datetime import datetime

def save_image_data(selected_emotions):
    if not selected_emotions:
        print("!!!Δεν επιλέχθηκε κανένα συναίσθημα.")
        return

    for emotion in selected_emotions:
        local_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Αποστολή στο LSL
        sample = [emotion, local_time_str]
        if emotion_outlet is not None:
            try:
                emotion_outlet.push_sample(sample)
                print(f"Συναισθηματικό event: {emotion} | Ώρα: {local_time_str}")
            except Exception as e:
                print(f"!!!Σφάλμα στο EmotionStream: {e}")
        else:
            print("!!!Δεν υπάρχει ενεργό EmotionStream.")

    # Στέλνουμε ένα face event ταυτόχρονα
    face_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    if face_outlet is not None:
        try:
            face_outlet.push_sample(["face", face_time_str])
            print(f"Face event | Ώρα: {face_time_str}")
        except Exception as e:
            print(f"!!!Σφάλμα στο FaceStream: {e}")


# ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΕΡΜΑΤΙΣΜΟ ΠΡΟΓΡΑΜΜΑΤΟΣ            

def terminate_program(): 
    global stop_recording
    stop_recording = True  # Τερματισμός καταγραφής

    print("Τερματισμός προγράμματος...")        

    # Αποστολή των τελευταίων συναισθημάτων αν υπάρχουν
    selected_emotions = [emotion for emotion, var in zip(emotions, emotion_vars) if var.get() == 1]
    if current_image_index < len(images):
        save_image_data(selected_emotions)

    # ΕΛΕΓΧΟΣ και για τα 2 streams
    if 'emotion_outlet' in globals() and emotion_outlet is not None:
        print("ℹΤο EmotionStream θα κλείσει αυτόματα με τον τερματισμό του προγράμματος.")
    else:
        print("Δεν υπάρχει ενεργό EmotionStream.")

    if 'face_outlet' in globals() and face_outlet is not None:
        print("Το FaceStream θα κλείσει αυτόματα με τον τερματισμό του προγράμματος.")
    else:
        print("Δεν υπάρχει ενεργό FaceStream.")  

    # Τερματισμός της κάμερας (αν είναι ακόμα ενεργή)
    if 'face_thread' in globals() and face_thread.is_alive():
        print("Περιμένουμε να σταματήσει η κάμερα...")
        face_thread.join(timeout=2)
        if face_thread.is_alive():
            print("!!! Η κάμερα δεν τερματίστηκε πλήρως")

    # Τερματισμός του παραθύρου Tkinter
    print("Τερματισμός Tkinter...")
    try:
        root.quit()
        root.destroy()
        print("Το παράθυρο έκλεισε επιτυχώς.")
    except tk.TclError:
        print("!!!Το Tkinter έκλεισε ήδη ή δεν ήταν ενεργό.")

# ΕΝΑΛΛΑΓΗ ΣΕ ΕΠΟΜΕΝΗ ΕΙΚΟΝΑ + ΑΠΟΘΗΚΕΥΣΗ ΤΩΝ ΕΠΙΛΟΓΩΝ ΚΑΘΕ ΕΙΚΟΝΑΣ

def next_image():
    global current_image_index
    print(f"Αλλαγή σε εικόνα {current_image_index + 1}")
    selected_emotions = [emotion for emotion, var in zip(emotions, emotion_vars) if var.get() == 1]

    if len(selected_emotions) == 0:
        messagebox.showwarning("Προειδοποίηση", "Παρακαλώ επιλέξτε τουλάχιστον ένα συναίσθημα.")
        return

# Αποθήκευση των δεδομένων για την τρέχουσα εικόνα
    save_image_data(selected_emotions)


    # Εναλλαγή στην επόμενη εικόνα 
    if current_image_index + 1 < len(images):
        current_image_index += 1
        show_image()
    else:
        # Αν είναι η τελευταία εικόνα, αποθηκεύει τα δεδομένα και τερματίζει το πρόγραμμα
        messagebox.showinfo("Τέλος", "Οι επιλογές σας έχουν αποθηκευτεί για όλες τις εικόνες.")
        save_image_data(current_image_index, selected_emotions)  #Διασφάλιση αποθήκευσης της τελευταίας εικόνας
        terminate_program()

    print(f"Τρέχουσα εικόνα: {current_image_index + 1}/{len(images)}")


 # ΣΥΝΑΡΤΗΣΕΙΣ ΓΙΑ ΑΡΧΕΙΟ ΗΧΟΥ         

# Πλαίσιο για τα κουμπιά αναπαραγωγής
control_frame = tk.Frame(root)
control_frame.pack()


def play_audio():
    audio_file = audio_files[current_image_index]
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def pause_audio():
    pygame.mixer.music.pause()

def resume_audio():
    pygame.mixer.music.unpause()

#-----------------------------------------------------------ΓΡΑΦΙΚΑ part 2 (KOYΜΠΙΑ)-----------------------------------------------------------#   

#  ΛΕΙΤΟΥΡΓΙΑ ΓΙΑ ΤΗΝ ΕΜΦΑΝΙΣΗ ΤΗΣ ΕΙΚΟΝΑΣ ΚΑΙ ΤΩΝ ΕΠΙΛΟΓΩΝ

def show_image():
    global image_label

    # Περιμένουμε να ενημερωθεί το μέγεθος του frame
    root.update_idletasks()

    # Παίρνουμε το μέγεθος του right_frame (μετά την ενημέρωση)
    frame_width = right_frame.winfo_width()
    frame_height = right_frame.winfo_height()

    # Αν το frame δεν έχει ενημερωθεί, δίνουμε default τιμές
    if frame_width == 1 or frame_height == 1:
        frame_width = int(screen_width * 0.75)
        frame_height = int(screen_height * 0.9)

    # Φόρτωση της εικόνας
    image_file = images[current_image_index]
    img = Image.open(image_file)

    # Παίρνουμε το αρχικό μέγεθος της εικόνας
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height

    # Υπολογισμός νέων διαστάσεων ώστε να ταιριάζει στο frame διατηρώντας το aspect ratio
    new_width = min(frame_width, img_width)
    new_height = int(new_width / aspect_ratio)

    if new_height > frame_height:
        new_height = frame_height
        new_width = int(new_height * aspect_ratio)

    # Αλλαγή μεγέθους της εικόνας με διατήρηση της ποιότητας
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Μετατροπή σε PhotoImage και ενημέρωση του Label
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img  # Κρατάμε reference για να μην διαγραφεί από τη μνήμη
    image_label.configure(bg=bg_color)

    # Ενημέρωση του κειμένου που εμφανίζεται στο αριστερό frame
    text_label.config(text=texts[current_image_index])
    text_label.configure(bg=bg_color)
    control_frame.configure(bg=bg_color)

    # Ανανέωση των επιλογών στα checkbox (μηδενισμός)
    for var in emotion_vars:
        var.set(0)
     

# Προσαρμογή του παραθύρου στο μέγεθος της οθόνης
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Δημιουργία πλαισίου (frame) για τη διάταξη των στοιχείων
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH)

# Αριστερό πλαίσιο για τις επιλογές (κειμενο, checkboxes, ήχος, κουμπιά)
left_frame = tk.Frame(main_frame, width=int(screen_width * 0.07), bg=bg_color)  # 20% της οθόνης
left_frame.grid(row=0, column=0, padx=0, pady=0, sticky="n")

# Δεξί πλαίσιο για την εικόνα (θα καταλαμβάνει όλο τον διαθέσιμο χώρο)
right_frame = tk.Frame(main_frame,bg=bg_color)
right_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

#Εφαρμογή background στα Frames
main_frame.configure(bg=bg_color)
left_frame.configure(bg=bg_color)
right_frame.configure(bg=bg_color)

# Εφαρμογή στα checkboxes
for checkbox in left_frame.winfo_children():
    if isinstance(checkbox, tk.Checkbutton):
        checkbox.configure(bg=bg_color, activebackground=bg_color)


# Επιτρέπει στο δεξί πλαίσιο να προσαρμόζεται δυναμικά
main_frame.grid_columnconfigure(0, weight=0)  # Αριστερό frame (λιγότερο βάρος)
main_frame.grid_columnconfigure(1, weight=1)  # Δεξί frame (περισσότερος χώρος)
main_frame.grid_rowconfigure(0, weight=1)

# Καμβάς για την εμφάνιση εικόνων
image_label = tk.Label(right_frame,bg=bg_color)
image_label.pack(expand=True, fill=tk.BOTH)

# Περιγραφή Εικόνας (Τίτλος & Κείμενο)
text_label = tk.Label(left_frame, text="", wraplength=300, justify="left", font=custom_font, fg=fg_color, bg=bg_color)
text_label.pack(pady=(10, 40))

# Κενό frame για μετακίνηση προς τα κάτω
spacer = tk.Frame(left_frame, height=20, bg=bg_color)
spacer.pack()

spacer2 = tk.Frame(left_frame, height=30, bg=bg_color)
spacer2.pack()

# Μεταβλητές για τα checkbox των συναισθημάτων
emotion_vars = [tk.IntVar() for _ in emotions]

for i, emotion in enumerate(emotions):
    tk.Checkbutton(
        left_frame,
        text=emotion,
        bg=bg_color,  # Σκούρο φόντο
        fg=fg_color,  # Λευκό κείμενο
        selectcolor=bg_frames,  # Αποφυγή του default μπλε
        activebackground=hover_bg,  # Όταν περνάει το ποντίκι από πάνω
        activeforeground=fg_color,
        variable=emotion_vars[i],
        font=custom_font
    ).pack(anchor="w", pady=3)

# Κενό για απόσταση πριν τα κουμπιά ήχου
spacer2 = tk.Frame(left_frame, height=30)
spacer2.pack()
spacer2.configure(bg=bg_color)

# ΚΟΥΜΠΙΑ ΑΝΑΠΑΡΑΓΩΓΗΣ ΗΧΟΥ
control_frame = tk.Frame(left_frame, bg=bg_color)
control_frame.pack(pady=(10, 20))  # Αυξάνουμε το πάνω και κάτω padding

button_style = {
    "font": custom_font,  # Γραμματοσειρά
    "fg": btn_fg,  # Λευκό κείμενο
    "bg": btn_bg,  # Σκούρο γκρι φόντο
    "bd": 2,  # Λεπτό περίγραμμα
    "relief": tk.RIDGE,  # Minimal αισθητική
    "width": 15,  # Σταθερό μέγεθος κουμπιών
    "height": 1,
    "highlightthickness": 0,
    "cursor": "hand2" , # Αλλάζει τον cursor σε χεράκι
    "padx": 10,  # Κάνει το κουμπί πιο "γεμάτο"
    "pady": 5,  # Βοηθάει στο στρογγύλεμα
}

# Hover Effect (αλλαγή χρώματος όταν περνάει το ποντίκι πάνω από το κουμπί)
def on_enter(e):
    e.widget.config(bg=hover_bg)

def on_leave(e):
    e.widget.config(bg=e.widget.original_bg)

# ΚΟΥΜΠΙΑ Play , Pause, Resume
play_button = tk.Button(control_frame, text="▶ Play",**button_style, command=play_audio)
pause_button = tk.Button(control_frame, text="⏸ Pause",**button_style, command=pause_audio)
resume_button = tk.Button(control_frame, text="▶ Resume",**button_style, command=resume_audio)

#ΚΟΥΜΠΙΑ ΠΛΟΗΓΗΣΗΣ
nav_frame = tk.Frame(left_frame, bg=bg_color)
nav_frame.pack()
nav_frame.configure(bg=bg_color)

next_button = tk.Button(nav_frame, text="Επόμενη", **button_style, command=next_image)
next_button.pack(side=tk.LEFT, padx=20)
for btn in [next_button]:
    btn.configure(bg=bg_color, activebackground=bg_color, highlightthickness=0)

stop_button = tk.Button(nav_frame, text="Τερματισμός", **button_style, command=terminate_program)
stop_button.pack(side=tk.LEFT, padx=20)
for btn in [stop_button]:
    btn.configure(bg=bg_color, activebackground=bg_color, highlightthickness=0)

# Προσθήκη Hover Effect
for btn in [play_button, pause_button, resume_button, next_button, stop_button]:
    btn.original_bg = btn.cget("background")  # Αποθήκευση αρχικού χρώματος


for btn in [play_button, pause_button, resume_button, next_button, stop_button]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


play_button.pack(side=tk.LEFT, padx=5)
pause_button.pack(side=tk.LEFT, padx=5)
resume_button.pack(side=tk.LEFT, padx=5)

# Εφαρμογή στα κουμπιά
for btn in [play_button, pause_button, resume_button]:
    btn.configure(bg=bg_color, activebackground=bg_color, highlightthickness=0)
    btn.original_bg = bg_color  # <-- Εδώ το διορθώνεις


# Αρχική ρύθμιση για την πρώτη εικόνα
current_image_index = 0
show_image()

#--------------------------------------------------------------------------------------------------------------#

# ΚΑΜΕΡΑ + ΑΠΟΣΤΟΛΗ ΣΤΟ LSL
def record_faces(total_duration=2400):
    global stop_recording

    video_folder = "C:/Users/athin/Desktop/Diplomatikh/EmotionData/Videos"
    os.makedirs(video_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_output_path = os.path.join(video_folder, f"video_{timestamp}.avi")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("!!! Η κάμερα δεν άνοιξε.")
        return

    fps = 20.0
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(video_output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print(f"Η Καταγραφή προσώπου ξεκίνησε. Βίντεο: {video_output_path}")

    start_time = time.time()

    try:
        while time.time() - start_time < total_duration and not stop_recording:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


            current_time = datetime.now().strftime("%H:%M:%S")
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, current_time, (10, 40), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            out.write(frame)
            cv2.imshow('Recording', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                print("Ο χρήστης τερμάτισε την καταγραφή.")
                break

    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(" Η καταγραφή ολοκληρώθηκε.")

# Εκκίνηση της καταγραφής προσώπου σε ξεχωριστό νήμα
face_thread = threading.Thread(target=record_faces, args=(2400,))
face_thread.start()


# Έναρξη του παραθύρου
root.mainloop()
