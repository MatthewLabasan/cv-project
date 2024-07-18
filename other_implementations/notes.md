# Project Notes

## Conda / Pip notes
- Don't need the yaml file unless wanting to run from conda environment through development/dist
- VS code can run through the conda interpreter without the env so we will just develop with the thought of pip as we will on the actual computer

## Open CV
- Cross-plateform (C++, Python, Java) library that is optimized for real-time computer vision development and applications
- Focuses on image processing, video capture, analysis

## Tesseract and PyTesseract
- Open-source text recognition (OCR: optical character recognition) engine.
- Tesseract is just one of many open source engines built off of a trained dataset.
    - OCR is a process that consists of:
        - Preprocessing of the Image
        - Text Localization
        - Character Segmentation
        - Character Recognition
        - Post Processing
- Supports wide variert of languages. PyTesseract is a Python wrapper for Tesseract.
### Source: https://nanonets.com/blog/ocr-with-tesseract/

## Models of OCR Use
### Tesseract
- Having a difficult time detecting KNOTS and the direction within the circular part of the GUI
- Also does not detect all the numbers consistenently
- Nicer output strings
### Easy-OCR
- Better detection, funky output strings
- Is not detecting the numbers in the direction compasss circle
## Keras-OCR
- Slow, a bit harder to use.

## Screen Recording
- Utilize Pillow for screen image grab, screeninfo for screen resolution information, numpy for manipulation, and opencv

## Programs Put Together
- As we screen record (most likely one image per second depending on program updates, need to ask Kai), pass the information into python_ocr and print it to a file.
- Need to make python_ocr accept a param
- One second should be long enough for the ocr to run through without too many image modifications. May need to figure out how to optimize.

### Python Version 3.3 or later