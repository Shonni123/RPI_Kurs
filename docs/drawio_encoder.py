import zlib, base64, urllib.parse

def make_drawio_file(graph_model_xml, diagram_id="module-diagram", diagram_name="Модульная диаграмма"):
    url_encoded = urllib.parse.quote(graph_model_xml.strip(), safe='~()*!\'')
    compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
    compressed = compressor.compress(url_encoded.encode('utf-8')) + compressor.flush()
    b64_payload = base64.b64encode(compressed).decode('utf-8')
    
    file_content = f'''<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="24.7.17">
  <diagram id="{diagram_id}" name="{diagram_name}">{b64_payload}</diagram>
</mxfile>'''
    return file_content
