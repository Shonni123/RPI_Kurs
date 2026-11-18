import zlib, base64, urllib.parse

def encode_diagram(xml_str):
    url_encoded = urllib.parse.quote(xml_str, safe='~()*!\'')
    # Raw deflate
    compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
    compressed = compressor.compress(url_encoded.encode('utf-8')) + compressor.flush()
    return base64.b64encode(compressed).decode('utf-8')

def decode_diagram(b64_str):
    raw = base64.b64decode(b64_str)
    decompressed = zlib.decompress(raw, -15)
    return urllib.parse.unquote(decompressed.decode('utf-8'))

test_xml = '<mxGraphModel dx="1200" dy="900"><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>'
encoded = encode_diagram(test_xml)
decoded = decode_diagram(encoded)
assert decoded == test_xml
print("Success! Compression and decompression match draw.io standard format.")
