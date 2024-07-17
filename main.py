# purpose of program: screen record data for future reference and automate data collection with optical character recognition

# write screen recorder

# for every frame read, push into tesseract and append to txt file
# write to video

# this assumes that it will take only a second to complete the tesseract. how can we prevent script from holding up (as it will probably take longer, alongside data sorting and identification)?
# try to ptimize tesseract by reducing image changes and reducing scan size (decrease size to gui only)

# possible solutions: 
    # place images into an array/stack or something, and process data after.
    # record data every 5 or so seconds instead