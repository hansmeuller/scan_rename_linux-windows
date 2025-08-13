import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pytesseract
from pdf2image import convert_from_path
import logging

# einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()

# Pfad
scans_folder = "ftp://fritz.box/PortableSSD/scans/_test"

# OCR
def extract_text_with_ocr(pdf_path):
    try:
        logger.info(f"Starte: {pdf_path}")
        # Konvertiere 
        pages = convert_from_path(pdf_path)
        text = ""
        for page in pages:
            # ocr auf jeder Seite anwenden
            text += pytesseract.image_to_string(page)
        logger.info(f"fertig: {pdf_path}")
        return text
    except Exception as e:
        logger.error(f"Fehler : {e}")
        return ""

# überwachung datei
class ScanHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".pdf"):
            logger.info(f"PDF erkannt: {event.src_path}")
            # ocr neu
            extracted_text = extract_text_with_ocr(event.src_path)
            # umbenennen
            logger.info(f"folgendes erkannt: {extracted_text[:100]}...")  

# Überwachung
def start_monitoring():
    event_handler = ScanHandler()
    observer = Observer()
    observer.schedule(event_handler, path=scans_folder, recursive=False)
    observer.start()
    logger.info(f"Überwache: {scans_folder}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#finally main
if __name__ == "__main__":
    start_monitoring()
