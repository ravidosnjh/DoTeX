Download DoTeX.zip by clicking the Code dropdown on Github and selecting Download ZIP.
Extract the downloaded zip to a trusted location.

To run DoTeX open the extracted folder, and double click the file DoTeX.vbs

Troubleshooting:
If double clicking DoTeX.vbs does not work:
1) Try double clicking DoTeX.bat
2) Open command prompt/powershell, and change directory to inside the extracted folder. Then run .\Python310\Python.exe DoTeX.py
3) Install Python and add it to environment path. Open command prompt/powershell and change directory to inside the extracted folder. Then run python DoTeX.py
4) Open Python IDLE and open DoTeX.py inside it and run it

Default file paths are:
TEX_DIRECTORY = "TeX_Documents"
PDF_DIRECTORY = "PDFs"
LOG_DIRECTORY = "Logs"
FILTERED_LOG_DIRECTORY = "Logs/Filtered_Logs"
PICTURES_PATH = "Pictures"

These can be changed in the application using the Settings button

Bib files should be saved to the DoTeX root folder where sample.bib is saved
Other files should be saved to their corresponding default file path, or the file path set through Settings
