
import os

RESSOURCES_PATH = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), 'xml')


def read_ressource_xml_file(filename):
    filename = os.path.join(RESSOURCES_PATH, filename)
    with open(filename, "r") as my_xml:
        return my_xml.read()


RESSOURCES = {
    filename.strip(".xml") : read_ressource_xml_file(filename)
    for filename in os.listdir(RESSOURCES_PATH)
}



for k, v in RESSOURCES.items():
    print(k)
    print(v)
    print()
    print()
    print()