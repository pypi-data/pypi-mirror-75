from qrcode import *


def cz_qrcode(text):
    qr = QRCode()
    qr.add_data(text)
    img = qr.make_image()
    img.show()