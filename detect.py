
# Import Libraries
import cv2
import time
import mediapipe as mp
import numpy as np 

W=320
H=240

# XXX A list of hand gestures here:
gesture = []
gesture.append({"name": "fist"			, "min":  [np.array([0.95585, 0.00000, 0.49283]), np.array([0.75429, 0.00000, 0.48353]), np.array([0.65380, 0.00000, 0.00000]), np.array([1.00000, 0.00000, 0.29819]), np.array([1.00000, 0.00000, 0.41175]), np.array([0.43636, 0.00000, 0.04044]), np.array([1.00000, 0.00000, 0.00000]), np.array([0.00000, 0.00000, 0.00000]), np.array([0.00000, 0.00000, 0.00000]), np.array([0.00000, 0.00000, 0.00000]), np.array([1.00000, 0.00000, 0.00000]), np.array([0.00000, 0.00000, 0.00000]), np.array([0.00000, 0.50845, 0.00000]), np.array([0.00000, 0.51969, 0.00000]), np.array([0.89156, 0.00000, 0.00000]), np.array([0.00000, 0.00000, 0.00000]), np.array([0.00000, 1.00000, 0.00000]), np.array([0.00000, 0.48320, 0.09232]), np.array([1.00000, 0.00000, 0.00000]), np.array([0.00000, 0.85219, 0.00000]), np.array([0.00000, 0.52110, 0.05636])] , "max":  [np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 1.00000, 1.00000]), np.array([1.00000, 0.00000, 0.85294]), np.array([1.00000, 0.00000, 0.72827]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.92499, 0.50521]), np.array([1.00000, 1.00000, 1.00000]), np.array([1.00000, 1.00000, 0.23109]), np.array([1.00000, 1.00000, 0.80440]), np.array([1.00000, 0.88710, 0.42604]), np.array([1.00000, 1.00000, 1.00000]), np.array([1.00000, 1.00000, 0.22634]), np.array([0.54685, 1.00000, 1.00000]), np.array([1.00000, 1.00000, 0.42188]), np.array([1.00000, 1.00000, 1.00000]), np.array([0.85589, 1.00000, 0.32798]), np.array([0.00000, 1.00000, 1.00000]), np.array([1.00000, 0.77782, 0.52661]), np.array([1.00000, 1.00000, 0.29647]), np.array([0.00000, 1.00000, 1.00000])]})
gesture.append({"name": "hand_spayed"	, "min":  [np.array([1.00000, 0.00000, 0.56291]), np.array([0.55322, 0.00000, 0.81690]), np.array([1.00000, 0.00000, 0.00000]), np.array([1.00000, 0.00000, 0.35356]), np.array([1.00000, 0.00000, 0.32165]), np.array([1.00000, 0.00000, 0.01772]), np.array([1.00000, 0.00000, 0.49401]), np.array([0.00000, 0.00000, 0.91313]), np.array([1.00000, 0.00000, 0.46523]), np.array([0.95858, 0.00000, 0.51306]), np.array([0.97636, 0.00000, 0.55041]), np.array([0.00000, 0.65072, 0.49680]), np.array([1.00000, 0.00000, 0.49030]), np.array([0.97956, 0.00000, 0.50676]), np.array([0.85075, 0.00000, 0.56529]), np.array([0.00000, 1.00000, 0.31072]), np.array([0.90573, 0.00000, 0.48374]), np.array([0.92573, 0.00000, 0.47308]), np.array([0.53076, 0.00000, 0.66849]), np.array([0.54560, 0.00000, 0.70209]), np.array([0.56710, 0.00000, 0.69002])] , "max":  [np.array([1.00000, 0.00000, 0.92124]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.17109, 0.32516]), np.array([1.00000, 0.00000, 0.79006]), np.array([1.00000, 0.00000, 0.75934]), np.array([1.00000, 0.00000, 0.58836]), np.array([1.00000, 0.00000, 0.93064]), np.array([0.11516, 1.00000, 1.00000]), np.array([1.00000, 0.00000, 0.98751]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.00000, 1.00000]), np.array([0.00000, 1.00000, 1.00000]), np.array([1.00000, 0.00000, 0.95073]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.00000, 1.00000]), np.array([0.00000, 1.00000, 0.81206]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.00000, 1.00000]), np.array([1.00000, 0.00000, 1.00000])]})

# TODO Add more gestures



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

while capture.isOpened():

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


	# TODO detect a hand gesture and return the right action / name.

		print("-----")
		for i in gesture:
			matching = 0
			for j in range(0, 21):
				if i["min"][j][0] <= norm_vectors[j][0]:
					if i["min"][j][1] <= norm_vectors[j][1]:
						if i["min"][j][2] <= norm_vectors[j][2]:
							if i["max"][j][0] >= norm_vectors[j][0]:
								if i["max"][j][1] >= norm_vectors[j][1]:
									if i["max"][j][2] >= norm_vectors[j][2]:
										matching = matching + 1

			if matching == 21:
				print(i["name"], ": ", round((matching/21*100), 1), "%  <<< ")
			else:
				print(i["name"], ": ", round((matching/21*100), 1), "%")


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
