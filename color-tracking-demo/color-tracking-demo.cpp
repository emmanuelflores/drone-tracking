// drone-tracking-demo.cpp

#include <iostream>
#include "opencv2/highgui/highgui.hpp"

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

  // create display window
  cv::namedWindow("Result window", CV_WINDOW_AUTOSIZE);

  for(;;)
  {
    cv::Mat frame;
    // grab frame
    cap >> frame;

    // show frame
    cv::imshow("Result window", frame);

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
