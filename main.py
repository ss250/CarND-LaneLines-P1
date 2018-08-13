#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy.polynomial.polynomial import polyfit
import cv2
import os

# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML

# %matplotlib inline

def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # you should return the final output (image where lines are drawn on lanes)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Define a kernel size and apply Gaussian smoothing
    kernel_size = 3
    gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

    # Define our parameters for Canny and apply
    low_threshold = 75
    high_threshold = 225
    edges = cv2.Canny(gray, low_threshold, high_threshold)

    # edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Next we'll create a masked edges image using cv2.fillPoly()
    mask = np.zeros_like(edges)   
    ignore_mask_color = 255   

    # This time we are defining a four sided polygon to mask
    imshape = image.shape

    xsize = imshape[1]
    ysize = imshape[0]

    vmask = 1.63 # proportion of image from bottom
    hmask = 60  # pixels from left and right
    top_line = 40

    vertices = np.array([[
        (hmask, ysize), # bottom left
        (xsize/2 - top_line, ysize/vmask), # top left
        (xsize/2 + top_line, ysize/vmask), # top right
        (xsize - hmask, ysize) # bottom right
    ]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    edges = cv2.bitwise_and(edges, mask)

    # define an inner mask
    vertices = np.array([[
        (hmask + 220, ysize),
        (xsize/2, ysize/vmask), 
        (xsize/2, ysize/vmask), 
        (xsize - hmask - 220, ysize)
    ]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, 0)

    edges = cv2.bitwise_and(edges, mask)

    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 2 # distance resolution in pixels of the Hough grid
    theta = (np.pi/180)*2 # angular resolution in radians of the Hough grid
    threshold = 20     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 10 #minimum number of pixels making up a line
    max_line_gap = 75    # maximum gap in pixels between connectable line segments
    line_image = np.copy(image)*0 # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

    # create line of best fit for left line segments and right line segments, using 1st degree polyfit
    left_lines = [line for line in lines if ((line[0][0] < xsize/2) and (line[0][2] < xsize/2))]
    right_lines = [line for line in lines if ((line[0][0] > xsize/2) and (line[0][2] > xsize/2))]

    left_b, left_m = polyfit([line[0][0] for line in left_lines] + [line[0][2] for line in left_lines], 
                             [line[0][1] for line in left_lines] + [line[0][3] for line in left_lines], 1)

    right_b, right_m = polyfit([line[0][0] for line in right_lines] + [line[0][2] for line in right_lines], 
                             [line[0][1] for line in right_lines] + [line[0][3] for line in right_lines], 1)
    cv2.line(line_image, (int((ysize - left_b)/left_m), ysize), (int(xsize/2 - 25), int(left_m*(xsize/2 - 25) + left_b)), (255, 0, 0), 5)
    cv2.line(line_image, (int((ysize - right_b)/right_m), ysize), (int(xsize/2 + 25), int(right_m*(xsize/2 + 25) + right_b)), (255, 0, 0), 5)

    # Draw the lines on the edge image
    result = cv2.addWeighted(image, 0.8, line_image, 1, 0)

    return result

def test_image(path):
    #reading in an image
    image = mpimg.imread(path)
    #printing out some stats and plotting
    print('This image is:', type(image), 'with dimensions:', image.shape)
    plt.imshow(process_image(image))  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')
    plt.show()


def test_video(file):
    ## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
    ## To do so add .subclip(start_second,end_second) to the end of the line below
    ## Where start_second and end_second are integer values representing the start and end of the subclip
    ## You may also uncomment the following line for a subclip of the first 5 seconds
    ##clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
    clip1 = VideoFileClip("test_videos/" + file)
    white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
    white_clip.write_videofile("test_videos_output/" + file, audio=False)

def main():

    images = os.listdir("test_images/")
    videos = os.listdir("test_videos/")

#     for image_file in images:
#         test_image("test_images/" + image_file)

    for video_file in videos:
        test_video(video_file)


if __name__ == "__main__":
    main()
