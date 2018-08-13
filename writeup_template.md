# **Finding Lane Lines on the Road** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"
[image2]: ./reference_images/Gaussian_blue.jpg "Gaussian"
[image3]: ./reference_images/masked.jpg "Masked"
[image4]: ./reference_images/Canny.jpg "Canny"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 6 steps. 
1. The image was converted to grayscale
![alt text][image1]
2. Then a gaussian blur was applied. I chose a kernel size of 3 as opposed to 5 because the image was already quite blurry
![alt text][image2]
3. A Canny edge detector was then applied with a low threshold of 75 and a high threshold of 225
![alt text][image3]
4. Next, two masks were applied to the image, one large trapezoid and one smaller trapezoid within the first, to mask as much of the image as possible without covering any of the lanes in the image. This was tested on the videos by drawing the polygon itself onto the video.
![alt text][image4]
5. A hough transform was applied to the image next. I chose a rho of 2 pixels and a theta of (pi/180)\*2 radians. My threshold was set to 20 votes, and the mininum line length and maximum line gap is 10 and 75 respectively. 
6. The next step is to split the line segments detected in the hough transform into two groups, one for the left line and one for the right. 

In order to draw a single line on the left and right lanes, I used a line of best fit for each side of the image, using the points from both ends of the line segments. 

### 2. Identify potential shortcomings with your current pipeline

Using a line of best fit like this has drawbacks in that the detected lines can be very noisy from frame to frame. Some sort of smoothing would make the pipeline more robust.  

Another shortcoming is that a first degree line of best fit was used. This means that lanes that curve a significant amount wouldn't be detected accuratly by my pipeline. 


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to set a smaller region of interest for the detected points, this would reduce the amount of erroneous lines detected by the pipeline. 

Another potential improvement could be to dynamically detect the curvature of the lines, and adjust the line of best fit accordingly. Maybe by using a second degree polynomial. 
