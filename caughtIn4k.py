import cv2
import os
import time
import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from datetime import datetime, timedelta

class CameraRecorder:
    def __init__(self, camera_index=0, output_dir="recordings"):
        self.camera_index = camera_index
        self.output_dir = output_dir
        self.cap = None
        self.is_recording = False
        self.out = None
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def start_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Camera', cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Resize the frame to fit the window size while maintaining the aspect ratio
            height, width = frame.shape[:2]
            window_width = cv2.getWindowImageRect('Camera')[2]
            window_height = cv2.getWindowImageRect('Camera')[3]
            aspect_ratio = width / height
            if window_width / window_height > aspect_ratio:
                new_height = window_height
                new_width = int(aspect_ratio * new_height)
            else:
                new_width = window_width
                new_height = int(new_width / aspect_ratio)
            
            frame_resized = cv2.resize(frame, (new_width, new_height))

            # Add timestamp to the frame
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame_resized, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Draw a box indicating recording status if not recording
            if not self.is_recording:
                box_color = (255, 0, 0)  # Blue box for not recording
                cv2.rectangle(frame_resized, (10, 50), (200, 90), box_color, -1)
                cv2.putText(frame_resized, "Not Recording", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                box_color = (0, 0, 255)  # Red box for recording
                cv2.rectangle(frame_resized, (10, 50), (200, 90), box_color, -1)
                cv2.putText(frame_resized, "Recording", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # If recording, write the frame without the red box indicator
            if self.is_recording and self.out is not None:
                frame_no_box = frame.copy()
                cv2.putText(frame_no_box, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                self.out.write(frame_no_box)

            cv2.imshow('Camera', frame_resized)

            key = cv2.waitKey(1)
            if key == ord('q'):  # 'q' to quit
                self.stop_recording()
                break
            elif key == ord(' '):  # Spacebar to toggle recording
                if self.is_recording:
                    self.stop_recording()
                else:
                    self.start_recording()

        self.cap.release()
        cv2.destroyAllWindows()

    def start_recording(self):
        self.is_recording = True
        self.out = self.get_video_writer()
        print("Recording started...")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.out is not None:
                self.out.release()
                self.out = None
            print("Recording stopped.")

    def get_video_writer(self):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"{current_time}.avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return cv2.VideoWriter(output_path, fourcc, fps, (width, height))

class DailyAndMonthlyManage:
    def __init__(self, camera_recorder):
        self.camera_recorder = camera_recorder
        self.start_time = None

    def start(self):
        self.camera_recorder.start_camera()
        self.start_time = datetime.now()
        self.manage_recordings()

    def manage_recordings(self):
        while True:
            current_time = datetime.now()
            if self.camera_recorder.is_recording and (current_time - self.start_time).seconds >= 10:
                self.camera_recorder.stop_recording()
                self.camera_recorder.start_recording()
                self.start_time = current_time
            self.delete_old_recordings()
            time.sleep(1)

    def delete_old_recordings(self):
        now = datetime.now()
        cutoff = now - timedelta(seconds=60)
        for filename in os.listdir(self.camera_recorder.output_dir):
            file_path = os.path.join(self.camera_recorder.output_dir, filename)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < cutoff:
                    os.remove(file_path)
                    print(f"Deleted old recording: {filename}")

if __name__ == "__main__":
    recorder = CameraRecorder()
    manager = DailyAndMonthlyManage(recorder)
    manager.start()

def show_message():
    tray_icon.showMessage(
        "Hello",
        "This is a message from the system tray icon",
        QSystemTrayIcon.MessageIcon.Information,
        2000
    )

def exit_app():
    QApplication.quit()

app = QApplication(sys.argv)

# Create the system tray icon
tray_icon = QSystemTrayIcon(QIcon("icon.png"), parent=app)
tray_icon.setToolTip("System Tray Icon Example")

# Create the context menu
menu = QMenu()

show_message_action = QAction("Show Message")
show_message_action.triggered.connect(show_message)
menu.addAction(show_message_action)

exit_action = QAction("Exit")
exit_action.triggered.connect(exit_app)
menu.addAction(exit_action)

tray_icon.setContextMenu(menu)

# Show the tray icon
tray_icon.show()

# Ensure the application keeps running
sys.exit(app.exec())