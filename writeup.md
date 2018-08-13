# **Finding Lane Lines on the Road** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

---

**Finding Lane Lines on the Road**


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"
[image2]: ./reference_images/Gaussian_blue.png "Gaussian"
[image3]: ./reference_images/masked.png "Masked"
[image4]: ./reference_images/Canny.png "Canny"

---

### Reflection

### 1. Pipeline Description.

My pipeline consisted of 7 steps. 
1. The image was converted to grayscale

![alt text][image1]

2. Then a gaussian blur was applied. I chose a kernel size of 3 as opposed to 5 because the image was already quite blurry

![alt text][image2]

3. A Canny edge detector was then applied with a low threshold of 75 and a high threshold of 225

![alt text][image4]

4. Next, two masks were applied to the image, one large trapezoid and one smaller trapezoid within the first, to mask as much of the image as possible without covering any of the lanes in the image. This was tested on the videos by drawing the polygon itself onto the video.
shortcoming
![alt text][image3]

5. A hough transform was applied to the image next. I chose a rho of 2 pixels and a theta of (pi/180)\*2 radians. My threshold was set to 20 votes, and the mininum line length and maximum line gap is 10 and 75 respectively. 

6. The next step is to split the line segments detected in the hough transform into two groups, one for the left line and one for the right. 
shortcoming
7. In order to draw a single line on the left and right lanes, I used a line of best fit for each side of the image, using the points from both ends of the line segments. The x,y coordinates of both ends of the line segments were derived from the slope and constant returned from numpy's polyfit function. A first degree fit was used. 

### 2. Potential Shortcomings of the pipeline

Using a line of best fit like this has drawbacks in that the detected lines can be very noisy from frame to frame. Some sort of smoothing would make the pipeline more robust. A moving avergage with a window of previous lines could be used, reducing the noise by a significant amount.

Another shortcoming is that a first degree line of best fit was used. This means that lanes that curve a significant amount wouldn't be detected accuratly by my pipeline. However accuratly drawing the line would be more difficult. 


### 3. Possible improvements to the pipeline

A possible improvement would be to set a smaller region of interest for the detected points, this would reduce the amount of erroneous lines detected by the pipeline. 

Another potential improvement could be to dynamically detect the curvature of the lines, and adjust the line of best fit accordingly. Maybe by using a second degree polynomial. 
