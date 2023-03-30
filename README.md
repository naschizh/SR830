# SR830
SR830 GPIB Communication protocol

File SR830.py contains a class that represents SR830 Lock-in Amplifier.
Its manual one can find via the link https://www.thinksrs.com/downloads/pdfs/manuals/SR830m.pdf.

The class code was made with the same code words as in the manual of the device so that any user could easily navigate through it.
I used decorators in this code, because it garantees the simplicity and conciseness for the user.

Every time user tries to initialize communication with the device, it starts anew to avoid possible conflicts (as it was experienced in real-life application of the code).

