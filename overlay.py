import cv2 as cv
import numpy as np


def do_canny(frame):
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)  # convert frame to grayscale
    blur = cv.GaussianBlur(gray, (5, 5), 0)  # apply Gaussian blur to the grayscale image
    canny = cv.Canny(blur, 50, 150)  # perform Canny edge detection
    return canny


def do_segment(frame):
    height = frame.shape[0]  # get the height of the frame
    polygons = np.array(
        [[(0, height), (800, height), (380, 290)]])  # define the region of interest (ROI) using polygons
    mask = np.zeros_like(frame)
    cv.fillPoly(mask, polygons, 255)  # create a mask for the ROI
    segment = cv.bitwise_and(frame, mask)  # apply the mask to the frame
    return segment


def calculate_lines(frame, lines):
    left = []
    right = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)  # fit a first-degree polynomial (line) to the points
            slope = parameters[0]
            y_intercept = parameters[1]

            if slope < 0:
                left.append((slope, y_intercept))
            else:
                right.append((slope, y_intercept))

        if left and right:
            left_avg = np.average(left, axis=0)
            right_avg = np.average(right, axis=0)
            left_line = calculate_coordinates(frame, left_avg)  # calculate coordinates for left line
            right_line = calculate_coordinates(frame, right_avg)  # calculate coordinates for right line
            return np.array([left_line, right_line])

    return None


def calculate_coordinates(frame, parameters):  # calculating the coordinates
    slope, intercept = parameters
    y1 = frame.shape[0]
    y2 = int(y1 - 150)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def visualize_lines(frame, lines):
    lines_visualize = np.zeros_like(frame)

    if lines is not None and len(lines) >= 2:
        for x1, y1, x2, y2 in lines:
            cv.line(lines_visualize, (x1, y1), (x2, y2), (0, 255, 0), 5)

        if lines is not None and len(lines) >= 2:
            x1 = int((lines[0][0] + lines[1][0]) / 2)
            y1 = int((lines[0][1] + lines[1][1]) / 2)
            x2 = int((lines[0][2] + lines[1][2]) / 2)
            y2 = int((lines[0][3] + lines[1][3]) / 2)

            start_point = (x1, y1)
            end_point = (x2, y2)
            cv.line(lines_visualize, start_point, end_point, (0, 0, 255), 5)

    return lines_visualize


def video_overlay():
    cap = cv.VideoCapture(0)
    while (cap.isOpened()):
        ret, frame = cap.read()
        canny = do_canny(frame)
        segment = do_segment(canny)
        hough = cv.HoughLinesP(segment, 2, np.pi / 180, 100, np.array([]), minLineLength=100, maxLineGap=50)
        lines = calculate_lines(frame, hough)
        lines_visualize = visualize_lines(frame, lines)
        output = cv.addWeighted(frame, 0.9, lines_visualize, 1, 1)

        ret, buffer = cv.imencode('.jpg', output)
        frame_data = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

        if cv.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
