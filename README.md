# CaptureX: A Flexible Image Capture and Sharing App

## Overview
CaptureX is a Kivy application designed for capturing images using either an external webcam connected via IP or the computer's built-in camera. It provides functionalities for starting and stopping the camera feed, capturing images, and sharing captured images through shareable links. Built using the Kivy framework, the application offers a user-friendly interface that allows users to interact seamlessly with the camera feed and captured images.

## Features
- **Camera Feed**: Start and stop the camera feed to view live video streams.
- **Image Capture**: Capture images from the camera feed.
- **Image Sharing**: Generate shareable links for captured images and copy them to the clipboard.
- **Open Image Link**: Open the shareable image link in the default web browser.
- **Home Navigation**: Navigate back to the camera feed screen.

## Technologies Used
- **filestack-python**: A library for integrating with the Filestack file handling service.
- **Kivy**: An open-source Python framework for developing multitouch applications.
- **opencv-python**: A library for computer vision and image processing.
- **python-dotenv**: A library for managing environment variables in .env files.
- **webbrowser**: A module for displaying web-based documents.

## Setup
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Configure the necessary parameters such as `DROIDCAM_IP_ADDRESS`, `DROIDCAM_PORT_NUMBER`, and `FILESTACK_API_KEY` in `constants.py`.
5. Run the script using `python main.py`.
   - By default, the application uses an external webcam with an IP address (similar to DroidCam). Users can switch to using the computer's built-in camera by uncommenting the relative line in `main.py` to use `gui_cam.py`, which is integrated with the necessary KV file for the computer camera widget.

## Usage
1. Run the script using `python main.py`.
2. Use the `Start Camera` button to start the camera feed.
3. Use the `Capture` button to capture images from the camera feed.
4. Navigate to the `Image` screen to view captured images and share them.
5. Use the `Create Shareable Link` button to generate a shareable link for the captured image.
6. Use the `Copy Link` button to copy the shareable link to the clipboard.
7. Use the `Open Link` button to open the shareable image link in the default web browser.
8. Use the `Stop Camera` button to stop the camera feed when done.
9. Use the `Home` button to navigate back to the camera feed screen.

## Customization
Users can customize the appearance and behavior of the application by modifying the KV file `front_end.kv` located in the `data` directory.

## Shareable Links
The application uses [filestack](https://www.filestack.com/) cloud service to generate shareable links for captured images by default. However, users can choose any cloud service and adjust the `FileShare` class accordingly in the `classes.py` file to integrate with their preferred cloud storage solution.

## Contributing
Contributions are welcome! Here are some ways you can contribute to the project:
- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests with bug fixes or enhancements

## Author
- Emad &nbsp; E>
  
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the MIT License, which grants permission for free use, modification, distribution, and sublicense of the code, provided that the copyright notice (attributed to [emads22](https://github.com/emads22)) and permission notice are included in all copies or substantial portions of the software. This license is permissive and allows users to utilize the code for both commercial and non-commercial purposes.

Please see the [LICENSE](LICENSE) file for more details.