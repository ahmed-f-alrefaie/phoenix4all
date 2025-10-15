import ftplib

def list_ftp_files(ftp_server: str, usr: str= "", password: str="") -> list:
    """List files in a given directory on an FTP server."""
    with ftplib.FTP(host=ftp_server) as ftp:
        ftp.login()  # Anonymous login
        files = ftp.nlst()
    return files