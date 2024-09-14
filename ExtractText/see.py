import easyocr

reader = easyocr.Reader(['en'])
#result = reader.readtext('71xbGE4AV3L.jpg',rotation_info=[90],ycenter_ths=1,link_threshold=0.1,text_threshold=0.5)
result = reader.readtext('71Xmkf5qsHL.jpg',rotation_info=[90,270],text_threshold=0.5,link_threshold=0.3,ycenter_ths=1,batch_size=3)
for i in result:
    print(i)