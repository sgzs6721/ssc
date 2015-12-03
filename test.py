import codecs
index = 0
obj = codecs.open("test.txt", 'r', "utf_8_sig")
print obj.read(10)