def detect(keypoints, state, reps, threshold=50):
    r_shoulder = keypoints[5]
    l_shoulder = keypoints[6]
    r_hip = keypoints[11]
    l_hip = keypoints[12]
    r_ankle = keypoints[15]
    l_ankle = keypoints[16]

    if abs(r_shoulder[0] - l_shoulder[0]) > abs(r_hip[0] - l_hip[0]) * 1.5:
        if abs(r_ankle[1] - l_ankle[1]) < threshold and state == "up":
            state = "down"
        elif abs(r_ankle[1] - l_ankle[1]) > threshold * 2 and state == "down":
            state = "up"
            reps += 1
    return "Jumping Jacks", reps, state