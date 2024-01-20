import time
import shutil
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from classes.xml_handlerStatus import XmlHandlerStatus  # Importiere die XmlHandler-Klasse aus der separaten Datei

class MyHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        # Laden der Konfiguration aus der JSON-Datei
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        self.function_rename_Status_activ = config.get("function_rename_Status_activ", False)
        self.function_drill_length = config.get("function_drill_length", False)
        self.function_change_material = config.get("function_change_material", False)
        self.neue_datei = None

    def on_created(self, event):
        if event.is_directory:
            return

        if event.event_type == 'created' and event.src_path.lower().endswith('.xml'):
            print(f"found new xml: {event.src_path}")
            self.neue_datei = event.src_path

            if self.function_rename_Status_activ:
                XmlHandlerStatus.change_special_parameter(self.neue_datei)

            if self.function_drill_length:
                XmlHandlerStatus.change_special_parameter(self.neue_datei)

            if  self.function_change_material:
                XmlHandlerStatus.change_special_parameter(self.neue_datei)



if __name__ == "__main__":
    # Laden Sie die Konfiguration aus der JSON-Datei
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    directory_to_watch = config["directory_to_watch"]
    directory_to_move = config["directory_to_move"]

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=False)

    print(f"Monitoring: {directory_to_watch}\n")
    observer.start()

    try:
        while True:
            time.sleep(1)
            if event_handler.neue_datei:
                ziel_dateipfad = os.path.join(directory_to_move, os.path.basename(event_handler.neue_datei))
                if os.path.exists(ziel_dateipfad):
                    os.remove(ziel_dateipfad)
                    print("file already exists - deleted")

                shutil.move(event_handler.neue_datei, directory_to_move)
                print(f"new xml-file moved to {directory_to_move}")
                print("wait...\n")

                event_handler.neue_datei = None
    except KeyboardInterrupt:
        observer.stop()

    observer.join()