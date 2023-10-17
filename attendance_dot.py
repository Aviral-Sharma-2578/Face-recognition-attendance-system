import os
import cv2
import insightface
import pandas as pd
import numpy as np

# Load the InsightFace model for face recognition
model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=0, det_size=(640, 640))

# Load the group photo
group_image_path = 'group.jpg'
group_img = cv2.imread(group_image_path)

# Load and process student images
student_folder = 'images'
student_images = os.listdir(student_folder)

student_data = []
for student_image in student_images:
    student_id = os.path.splitext(student_image)[0]
    student_image_path = os.path.join(student_folder, student_image)
    img = cv2.imread(student_image_path)
    faces = model.get(img)

    if faces:
        student_data.append({'student_id': student_id, 'face_features': faces[0].embedding})

# Load the group photo again
group_img = cv2.imread(group_image_path)
# gray_group_img = cv2.cvtColor(group_img, cv2.COLOR_BGR2GRAY)

# Create a CSV file to store the results
results = []
for student in student_data:
    for face in model.get(group_img):
        similarity = np.dot(face.embedding, student['face_features']) / (np.linalg.norm(face.embedding) * np.linalg.norm(student['face_features']))
        if similarity > 0.4:  # Adjust the threshold as needed
            results.append({'student_id': student['student_id'], 'attendance': 'Present'})
            break
    else:
        results.append({'student_id': student['student_id'], 'attendance': 'Absent'})

# Save the results to a CSV file
results_df = pd.DataFrame(results)
results_df.to_csv('attendance.csv', index=False)

print("Attendance data saved to attendance.csv")
