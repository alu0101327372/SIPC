#include <iostream>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>

using namespace cv;
using namespace std;


int main(int argc, char* argv[])
{
	Mat frame;
	VideoCapture cap;
	cap.open(0);

	if (!cap.isOpened()) {
		printf("Error opening cam\n");
		return -1;
	}
	namedWindow("Frame");
	
	while(true) {

		cap>>frame;
		
		imshow("Frame",frame);

		int c = waitKey(40);

		if ((char)c =='q') break;
	}
	cap.release();
	destroyAllWindows();
}
