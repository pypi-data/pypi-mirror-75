import mimetypes
import uuid


def encode(name: str, filename: str, data: bytes, extra_data=()):
    boundary = uuid.uuid4().hex
    content_type = 'multipart/form-data; boundary={}'.format(boundary)
    boundary = boundary.encode()
    inner_content_type = (mimetypes.guess_type(
        filename)[0] or 'application/octet-stream').encode()
    name = name.encode()
    filename = filename.encode()
    boundary_token = b'--' + boundary + b'\r\n'
    return content_type, \
        b"".join(map(lambda key_val: boundary_token + encode_value(*key_val), extra_data)) \
        + b'--' + boundary + b'\r\n' \
        b'Content-Disposition: form-data; name="' + name + b'"; filename="' + filename + b'"\r\n' \
        b'Content-Type: ' + inner_content_type + b'\r\n' \
        b'\r\n' \
        + data \
        + b'\r\n--' + boundary + b'--\r\n'


def encode_value(key, value):
    return b'Content-Disposition: form-data; name="' + key.encode() + b'"\r\n' \
        b'\r\n' \
        + str(value).encode() + b'\r\n'
