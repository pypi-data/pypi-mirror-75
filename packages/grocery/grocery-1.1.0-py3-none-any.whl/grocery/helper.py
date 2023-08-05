import random
import tarfile
import hashlib
import string
import socket
import fcntl
import struct
from typing import List
from pathlib import Path

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.header import Header


def randstr(str_type: str = None, length: int = 8):
    """
    Generate a random alphabet string or special characters or mixed characters.
    str_type: "alphabet" and "spec_char" are accepted. "str_type=None" indicate all alphabets and special characters.
    length: the length of random string.
    Return: the random string.
    """
    if str_type == "alphabet":
        char_group = string.ascii_letters
    elif str_type == "spec_char":
        char_group = string.punctuation
    else:
        char_group = string.ascii_letters + string.punctuation
    return ''.join(random.choices(char_group, k=length))


def send_email(
        smtp_svr: str, smtp_svr_port: int, account: str, account_pwd: str, to: list,
        subject: str = '', content: str = '', attachments: List[Path] = None
):
    msg = MIMEMultipart()
    msg['From'] = account
    msg['To'] = ",".join(to)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    for fp in attachments or list():
        with open(fp, 'rb') as f:
            # 设置附件的MIME和文件名:
            if fp.name.endswith('zip'):
                mime = MIMEBase('application', 'x-zip-compressed', filename=fp.name)
                mime.add_header('Content-Disposition', 'attachment', filename=fp.name)
            elif fp.name.endswith('html'):
                mime = MIMEBase('text', 'html', filename=fp.name)
                mime.add_header('Content-Disposition', 'attachment', filename=fp.name)
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
    try:
        smtpObj = smtplib.SMTP_SSL(smtp_svr, smtp_svr_port)
        smtpObj.login(account, account_pwd)
        smtpObj.sendmail(account, to, msg.as_string())
    except smtplib.SMTPException as e:
        raise Exception('Fail to send email!')


def tar_files(archive_fp: Path, files: List[Path]):
    with tarfile.open(archive_fp, mode='w:gz') as archive:
        for f in files:
            archive.add(f, recursive=True, arcname=f.name)


def md5(s: (str, bytes)):
    m = hashlib.md5()
    m.update(isinstance(s, bytes) and s or s.encode())
    return m.hexdigest()


def get_file_md5(fp: str):
    """
    获取文件md5值
    :param fp: 文件路径名
    :return: 文件md5值
    """
    with open(fp, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()


def get_ip_address(ifname: (str, bytes)):
    """
    Get the IP address of current system
    note: this method tested on Linux ONLY
    :param ifname: interface name(you cae check all interfaces using 'ifconfig' command in console.)
    :return: the IP address of specified interface
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifname = isinstance(ifname, bytes) and ifname or ifname.encode()
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

