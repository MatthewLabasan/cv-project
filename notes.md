# Project Notes
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

## Conda / Pip notes
- Don't need the yaml file unless wanting to run from conda environment through development/dist
- VS code can run through the conda interpreter without the env so we will just develop with the thought of pip as we will on the actual computer

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