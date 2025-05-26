def detect(keypoints, state, reps, threshold=50):
    r_knee = keypoints[13]
    l_knee = keypoints[14]
    r_hip = keypoints[11]
    l_hip = keypoints[12]
    r_shoulder = keypoints[5]

    if r_knee[1] > r_hip[1] and l_knee[1] > l_hip[1] and abs(r_shoulder[1] - r_hip[1]) > threshold:
        if r_knee[1] > r_hip[1] + threshold and state == "up":
            state = "down"
        elif r_knee[1] < r_hip[1] - threshold and state == "down":
            state = "up"
            reps += 1
    return "Squats", reps, state