import xml.etree.ElementTree as ET
import pandas as pd

def leer_xml(infrastructure\Data\students_social_media_cleaned.csv):
    tree = ET.parse(infrastructure\Data\students_social_media_cleaned.csv)
    root = tree.getroot()
    
    rows = []
    for alumno in root.findall("alumno"):
        fila = {
            "student_id": alumno.findtext("student_id"),
            "age": int(alumno.findtext("age")),
            ...
        }
        rows.append(fila)
    
    df = pd.DataFrame(rows)
    return df
