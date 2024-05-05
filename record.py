
# Import Libraries
import cv2
import time
import mediapipe as mp
import numpy as np 



np.set_printoptions(formatter={'float': lambda x: "{:.5f}".format(x)})

def custom_array_repr(arr):
	ret = "["

	if len(arr) >= 1:
		ret = ret + 'np.' + np.array_repr(arr[0], precision=3, suppress_small=True)

	for i in arr[1:]:
		ret = ret + ', ' + 'np.' + np.array_repr(i, precision=3, suppress_small=True)

	ret = ret + "]"
	return ret


W=320
H=240

# Grabbing the Holistic Model from Mediapipe and
# Initializing the Model
mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5
)

# Initializing the drawing utils for drawing the facial landmarks on image
mp_drawing = mp.solutions.drawing_utils

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, W)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
# Initializing current time and precious time for calculating the FPS
previousTime = 0
currentTime = 0



timer = 200 # TODO idk, 10s?

# The min/max vectors for recording
min_vectors = []
max_vectors = []

while capture.isOpened() and timer > 0:
	timer = timer - 1
	print(timer)
	# capture frame by frame
	ret, frame = capture.read()

	# Converting the from BGR to RGB
	image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# Making predictions using holistic model
	# To improve performance, optionally mark the image as not writeable to
	# pass by reference.
	image.flags.writeable = False
	results = holistic_model.process(image)
	image.flags.writeable = True

	# Converting back the RGB image to BGR
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


	# TODO NOT NEEDED!
	# Drawing the Facial Landmarks
	# mp_drawing.draw_landmarks(
	# image,
	# results.face_landmarks,
	# mp_holistic.FACEMESH_CONTOURS,
	# mp_drawing.DrawingSpec(
	# 	color=(255,0,255),
	# 	thickness=1,
	# 	circle_radius=1
	# ),
	# mp_drawing.DrawingSpec(
	# 	color=(0,255,255),
	# 	thickness=1,
	# 	circle_radius=1
	# )
	# )

	# Drawing Right hand Land Marks
	mp_drawing.draw_landmarks(
	image, 
	results.right_hand_landmarks, 
	mp_holistic.HAND_CONNECTIONS
	)

	# Drawing Left hand Land Marks
	mp_drawing.draw_landmarks(
	image, 
	results.left_hand_landmarks, 
	mp_holistic.HAND_CONNECTIONS
	)
	

	# XXX We assume only the right hand for now!

	connection_list = [(3, 4), (0, 5), (17, 18), (0, 17), (13, 14), (13, 17), (18, 19), (5, 6), (5, 9), (14, 15), (0, 1), (9, 10), (1, 2), (9, 13), (10, 11), (19, 20), (6, 7), (15, 16), (2, 3), (11, 12), (7, 8)]


	# If hand on screen.
	tmp = results.right_hand_landmarks
	if tmp:

		# Get vectors of relative hand coords.
		print("on screen!")
		keypoints = []
		for data_point in tmp.landmark:

			data = np.array([data_point.x, data_point.y, data_point.z])
			keypoints.append(data)

		# Normalize them
		norm_vectors = []
		if len(keypoints) == 21:
			for i in range(0, 21):
				coord_a = keypoints[i]
				for j in connection_list:
					if j[0] == i:
						coord_b = keypoints[j[1]]

						vec_norm = np.array([coord_b[0] - coord_a[0], coord_b[1] - coord_a[1], coord_b[2] - coord_a[2]])
						data_norm = (vec_norm - vec_norm.min()) / (vec_norm.max() - vec_norm.min())
						norm_vectors.append(data_norm)


		# Find the min vectors
		if len(min_vectors) == 0:
			# init
			min_vectors = np.copy(norm_vectors)
			max_vectors = np.copy(norm_vectors)
		else:
			# update
			for i in range(0, 21):
				min_vectors[i][0] = min(min_vectors[i][0], norm_vectors[i][0])
				min_vectors[i][1] = min(min_vectors[i][1], norm_vectors[i][1])
				min_vectors[i][2] = min(min_vectors[i][2], norm_vectors[i][2])

				max_vectors[i][0] = max(max_vectors[i][0], norm_vectors[i][0])
				max_vectors[i][1] = max(max_vectors[i][1], norm_vectors[i][1])
				max_vectors[i][2] = max(max_vectors[i][2], norm_vectors[i][2])


	# Print found result
	if timer == 1:
		print("---")
		print(" ")
		print("{\"name\": \"TODO\", \"min\": ", custom_array_repr(min_vectors), ", \"max\": ", custom_array_repr(max_vectors), "}")
		print(" ")
		print("---")

	# Calculating the FPS
	currentTime = time.time()
	fps = 1 / (currentTime-previousTime)
	previousTime = currentTime
	
	# Displaying FPS on the image
	cv2.putText(image, str(int(fps))+" FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

	# Display the resulting image
	cv2.imshow("Facial and Hand Landmarks", image)

	# Enter key 'q' to break the loop
	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

# When all the process is done
# Release the capture and destroy all windows
capture.release()
cv2.destroyAllWindows()
