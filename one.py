import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext('imag2.png')

for i in result:
    print(i)