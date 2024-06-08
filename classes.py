

class FileShare:
    """
    A class used to share files using the Filestack API.

    Attributes:
        filepath (str): The path to the file to be shared.
        api_key (str): The API key for the Filestack API (default is FILESTACK_API_KEY).
    """

    def __init__(self, filepath: str, api_key: str = FILESTACK_API_KEY) -> None:
        """
        Initializes a FileShare instance.

        Args:
            filepath (str): The path to the file to be shared.
            api_key (str, optional): The API key for the Filestack API (default is FILESTACK_API_KEY).
        """
        self.filepath = filepath
        self.api_key = api_key

    def share(self) -> str:
        """
        Shares the file using the Filestack API and returns the URL of the shared file.

        Returns:
            str: The URL of the shared file.

        Raises:
            Exception: If an error occurs during file upload.
        """
        try:
            client = Client(self.api_key)
            pdf_filelink = client.upload(filepath=self.filepath)
            return pdf_filelink.url
        except Exception as e:
            raise Exception(f"An error occurred while sharing the file: {e}")
