from constants import DROIDCAM_IP_ADDRESS, DROIDCAM_PORT_NUMBER


def get_droidcam_url():
    """
    Get the URL for the DroidCam server based on environment variables.

    Requires 'DROIDCAM_IP_ADDRESS' and 'DROIDCAM_PORT_NUMBER' environment variables to be set.

    Returns:
    str: The URL for the DroidCam server.
    """
    if not DROIDCAM_IP_ADDRESS or not DROIDCAM_PORT_NUMBER:
        return None

    # Construct the URL for the DroidCam server
    url = f'http://{DROIDCAM_IP_ADDRESS}:{DROIDCAM_PORT_NUMBER}/video'

    return url
