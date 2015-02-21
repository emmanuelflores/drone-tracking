// drone-tracking-demo.cpp

#include <iostream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

// main entry point
int main(int argc, char** argv)
{
  // set video capture properties for MacBook' iSight camera
  cv::VideoCapture cap;
  cap.set(CV_CAP_PROP_FRAME_WIDTH, 500);
  cap.set(CV_CAP_PROP_FRAME_HEIGHT, 600);

  // try to open video source
  cap.open(0);
    if (!cap.isOpened()) // check if it succeeded
  {
    std::cerr << "Could not open video" << std::endl;
    return -1;
  }

  // HSV section
  // create display window
  cv::namedWindow("HSV Result window", CV_WINDOW_AUTOSIZE);

  // create HSV controls window
  cv::namedWindow("HSV Controls", CV_WINDOW_AUTOSIZE);

  // HSV global values
  int iLowH = 0;
  int iHighH = 179;
  int iLowS = 0;
  int iHighS = 255;
  int iLowV = 0;
  int iHighV = 255;

  // Hue (0 - 179)
  cv::createTrackbar("LowH", "HSV Controls", &iLowH, 179);
  cv::createTrackbar("HighH", "HSV Controls", &iHighH, 179);
  // Saturation (0 - 255)
  cv::createTrackbar("LowS", "HSV Controls", &iLowS, 255);
  cv::createTrackbar("HighS", "HSV Controls", &iHighS, 255);
  // Value (0 - 255)
  cv::createTrackbar("LowV", "HSV Controls", &iLowV, 255);
  cv::createTrackbar("HighV", "HSV Controls", &iHighV, 255);

  // create display window
  cv::namedWindow("RGB Result window", CV_WINDOW_AUTOSIZE);

  // RGB section
  // create RGB controls window
  cv::namedWindow("RGB Controls", CV_WINDOW_AUTOSIZE);

  // RGB global values
  int iLowR = 0;
  int iHighR = 255;
  int iLowG = 0;
  int iHighG = 255;
  int iLowB = 0;
  int iHighB = 255;

  // Red (0 - 255)
  cv::createTrackbar("LowR", "RGB Controls", &iLowR, 255);
  cv::createTrackbar("HighR", "RGB Controls", &iHighR, 255);
  // Green (0 - 255)
  cv::createTrackbar("LowG", "RGB Controls", &iLowG, 255);
  cv::createTrackbar("HighG", "RGB Controls", &iHighG, 255);
  // Blue (0 - 255)
  cv::createTrackbar("LowB", "RGB Controls", &iLowB, 255);
  cv::createTrackbar("HighB", "RGB Controls", &iHighB, 255);

  for(;;)
  {
    cv::Mat frame;
    // grab frame
    cap >> frame;

    { // HSV try-out
      // convert to HSV
      cv::Mat imgHSV;
      cv::cvtColor(frame, imgHSV, cv::COLOR_BGR2HSV);

      // thresholded image
      cv::Mat imgThresholded;
      cv::inRange(
        imgHSV,
        cv::Scalar(iLowH, iLowS, iLowV),
        cv::Scalar(iHighH, iHighS, iHighV),
        imgThresholded);

      // show frame
      cv::imshow("HSV Result window", imgThresholded);
    }

    { // RGB try-out
      // thresholded image
      cv::Mat imgThresholded;
      cv::inRange(
        frame,
        cv::Scalar(iLowB, iLowG, iLowR),
        cv::Scalar(iHighB, iHighG, iHighR),
        imgThresholded);

      // show frame
      cv::imshow("RGB Result window", imgThresholded);
    }

    // give imshow some time to show the result
    // so have a 1 ms delay
    // stop when a key is pressed
    if (cv::waitKey(1) > -1)
    {
      break;
    }
  }

  return 0;
}
