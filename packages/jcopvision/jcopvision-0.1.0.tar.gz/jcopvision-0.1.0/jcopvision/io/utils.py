import cv2


def key_pressed(key):
    """
    Listens to keyboard event


    === Input ===
    key: char
        keyboard key to listen to


    === Return ===
    A boolean value indicating the key being pressed
    """
    return cv2.waitKey(1) == ord(key)


def create_sized_window(height, aspect_ratio, window_name="window", window_type=cv2.WINDOW_NORMAL):
    '''
    Create a window with specified height and aspect ratio


    === Input ===
    height: int
        desired window height

    aspect_ratio: float
        media aspect ratio

    window_name: str
        window name

    window_type: enum
        Qt backend flags. These are the available options
        - cv2.WINDOW_NORMAL
            enables window resizing
        - cv2.WINDOW_AUTOSIZE
            automatically adjusts to fit the displayed image
        - cv2.WINDOW_OPENGL
            window with opengl support
        - cv2.WINDOW_FULLSCREEN
            change the window to fullscreen
        - cv2.WINDOW_FREERATIO
            adjusts the image with no respect to its ratio
        - cv2.WINDOW_KEEPRATIO
            keeps the image ratio
        - cv2.WINDOW_GUI_EXPANDED
            new enhanced GUI
        - cv2.WINDOW_GUI_NORMAL
            old way to draw the window without statusbar and toolbar


    === Return ===
    Create a new window, but returning None
    '''
    cv2.namedWindow(window_name, window_type)
    cv2.resizeWindow(window_name, int(height * aspect_ratio), height)
