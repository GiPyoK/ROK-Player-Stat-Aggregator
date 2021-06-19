# ROK-Player-Stat-Aggregator

This program automates the process collecting in-game statistics of top 300 players in the kingdom.

## Description

This program goes through top 300 players and take screenshots of their statistics page. Then, OCR is performed on those screenshots and saves the data in a spread sheet. It saves hours of manual typing to just 30 minutes.

## Example Screenshots

The program takes two screenshots per player like the below images.

<p align="center">
  <img src="./images/example1.jpeg" alt="Player Stat Screenshot1" width="650">
</p>
<p align="center">
  <img src="./images/example2.jpeg" alt="Player Stat Screenshot2" width="650">
</p>

OCR is performed on above images, and useful data are exported in xlsx format.

<p align="center">
  <img src="./images/spreadsheet.jpeg" alt="Final Output" width="650">
</p>

## Dependencies

* PyAutoGUI - Controls the mouse to navigate through top 300 players' statistic pages
* OpenCV - Enhances image for better OCR accuracy
* PyTesseract - Converts image to string data
* OpenPyXL - Saves and formats the string data in xlsx format
