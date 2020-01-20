import os

likelihood = {'unknown': 0, 'very_unlikely': 1, 'unlikely': 2, 'possible': 3, 'likely': 4, 'very_likely': 5, '_EDITABLE': 0}
weight = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, '_EDITABLE': 0}
score_ranges = {'Good': range(int(5.2650 * 1000),int(6.2651 * 1000)), 
                'Average': range(int(3.665 * 1000), int(5.2650 * 1000)),
                'Bad': range(int(3.665 * 1000)), '_EDITABLE': 1, '_PLACEHOLDER': 'Enter range as (0.0000, 0.0000)'}

min_detection_confidence = 0.9
blur_threshold = 35
frames_per_second = 1/20
json_path = os.environ.get('GOOGLE_VISION_API_KEY')
enhancment_median = 127.5
sharpness_factor = 2
ip_cam_url = "http://192.168.0.23:8080/shot.jpg"
max_pics_saved = 9
seconds_to_run = 2
number_of_processes = 5
number_of_threads = 5
text_size = 100
text_color = (255, 0, 0)
text_font = "arial.ttf"
save_path = "Generated_Images"
face_ratio = 0.5