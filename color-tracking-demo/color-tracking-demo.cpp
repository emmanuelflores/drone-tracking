// color-tracking-demo.cpp

#include <iostream>
#include <cstdlib>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

// clicked point class
class CClickedPoint
{
public:
  CClickedPoint();
  virtual ~CClickedPoint();

  cv::Point point_;
  bool bUpdated_;
};

CClickedPoint::CClickedPoint()
 : point_(0, 0)
 , bUpdated_(false)
{}

CClickedPoint::~CClickedPoint()
{}

// callback for mouse events on a window
void
mouseCallback(int event, int x, int y, int flags, void* pData)
{
  CClickedPoint* pClickedPoint = static_cast<CClickedPoint*>(pData);
  if (pClickedPoint != NULL)
  {
    if (event == cv::EVENT_LBUTTONDOWN)
    {
      pClickedPoint->point_.x = x;
      pClickedPoint->point_.y = y;
      pClickedPoint->bUpdated_ = true;
    }
  }
}

// init
bool
initVideoCapture(cv::VideoCapture& videoCapture)
{
  // set video capture properties for MacBook' iSight camera
  videoCapture.set(CV_CAP_PROP_FRAME_WIDTH, 500);
  videoCapture.set(CV_CAP_PROP_FRAME_HEIGHT, 600);

  // try to open the video source
  videoCapture.open(0);
  if (!videoCapture.isOpened())
  {
    std::cerr << "Could not open video capture device" << std::endl;
    return false;
  }
  return true;
}

bool
createWindow(const std::string& sWindowName, const CClickedPoint* pCallbackData)
{
  // create window
  cv::namedWindow(sWindowName, CV_WINDOW_AUTOSIZE);
  // bind mouse callback function
  cv::setMouseCallback(sWindowName, mouseCallback, (void*)pCallbackData);
  // should always succeed
  return true;
}

bool
addTrackbar(
  const std::string& sWindowName,
  const std::string& sTrackbarName,
  int* value,
  const int count = 255)
{
  cv::createTrackbar(sTrackbarName, sWindowName, value, count);
  return true;
}

// main entry point
int
main(int argc, char** argv)
{
  int iDebug = 0;
  if (argc == 2)
  {
    iDebug = std::atoi(argv[1]);
  }

  // create video capture object
  cv::VideoCapture videoCapture;
  const bool bVideoCaptureInitialized = initVideoCapture(videoCapture);

  // create windows
  // Input
  const std::string sInputWindow("Input");
  CClickedPoint InputWindowClickedPoint;
  createWindow(sInputWindow, &InputWindowClickedPoint);
  // HSV Result
  const std::string sResultWindow("Result");
  createWindow(sResultWindow, NULL);
  // Controls
  const std::string sControlsWindow("Controls");
  createWindow(sControlsWindow, NULL);
  const std::string sControlRangeH("Range H");
  const std::string sControlRangeS("Range S");
  const std::string sControlRangeV("Range V");
  int rangeH = 10;
  int rangeS = 10;
  int rangeV = 10;
  const int maxRangeH = 50;
  const int maxRangeS = 50;
  const int maxRangeV = 50;
  addTrackbar(sControlsWindow, sControlRangeH, &rangeH, maxRangeH);
  addTrackbar(sControlsWindow, sControlRangeS, &rangeS, maxRangeS);
  addTrackbar(sControlsWindow, sControlRangeV, &rangeV, maxRangeV);

  if (bVideoCaptureInitialized)
  {
    // HSV threshold values
    int iLowH = 0;
    int iHighH = 179;
    int iLowS = 0;
    int iHighS = 255;
    int iLowV = 0;
    int iHighV = 255;

    for(;;)
    {
      cv::Mat frame;
      // grab frame
      videoCapture >> frame;
      // flip to make it mirror-like
      // cv::flip(frame, frame, 1);

      // show it
      cv::imshow(sInputWindow, frame);

      // HSV try-out
      // convert to HSV
      cv::Mat imgHSV;
      cv::cvtColor(frame, imgHSV, cv::COLOR_BGR2HSV);

      // get clicked point color
      if (InputWindowClickedPoint.bUpdated_ == true)
      {
        const int x = InputWindowClickedPoint.point_.x;
        const int y = InputWindowClickedPoint.point_.y;
        InputWindowClickedPoint.bUpdated_ = false;
        const cv::Vec3b hsv = imgHSV.at<cv::Vec3b>(y, x);
        if (iDebug > 3)
        {
          std::cout << "h=" << static_cast<int>(hsv[0])
                    << " s=" << static_cast<int>(hsv[1])
                    << " v=" << static_cast<int>(hsv[2]) << std::endl;
        }

        // update range thresholds
        iLowH  = hsv[0] - rangeH;
        iHighH = hsv[0] + rangeH;
        iLowS  = hsv[1] - rangeS;
        iHighS = hsv[1] + rangeS;
        iLowV  = hsv[2] - rangeV;
        iHighV = hsv[2] + rangeV;
      }

      // threshold image
      cv::Mat imgThresholded;
      cv::inRange(
        imgHSV,
        cv::Scalar(iLowH, iLowS, iLowV),
        cv::Scalar(iHighH, iHighS, iHighV),
        imgThresholded);

      // combine thresholded on original image
      cv::Mat imgCombined;
      frame.copyTo(imgCombined, imgThresholded);

      // show result
      cv::imshow(sResultWindow, imgCombined);

      // give imshow some time to show the result
      // so have a 1 ms delay
      // stop when a key is pressed
      if (cv::waitKey(1) > -1)
      {
        break;
      }
    }
  }
  else
  {
    std::cerr << "Failed to initialize video capture device" << std::endl;
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
