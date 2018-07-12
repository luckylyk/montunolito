import sys
import os


def read_ressource_xml_file(filename):
    filename = os.path.join(RESSOURCES_PATH, filename)
    with open(filename, "r") as my_xml:
        return my_xml.read()

RESSOURCES_PATH = os.path.realpath(os.path.dirname(__file__))
RESSOURCES = {
    str(filename[:-4]) : read_ressource_xml_file(filename)
    for filename in os.listdir(RESSOURCES_PATH) if filename.endswith('.xml')}