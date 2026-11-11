# XML create: https://docs.python.org/3/library/xml.etree.elementtree.html#building-xml-documents
# https://gpx.studio/app#10.8/52.1726/4.4756
#
from Application.location import Location
import xml.etree.ElementTree as ET


def create_xml(data: list[Location], route_name: str) -> ET.ElementTree:
    root = ET.Element("gpx")
    metadata = ET.SubElement(root, "metadata")
    ET.SubElement(metadata, "name").text = route_name
    author = ET.SubElement(metadata, "author")
    ET.SubElement(author, "name").text = "Arion"

    trk = ET.SubElement(root, "trk")
    ET.SubElement(trk, "name").text = route_name
    segment = ET.SubElement(trk, "trkseg")
    for location in data:
        trkpt = ET.SubElement(segment, "trkpt", lat=f"{location.latitude:.5f}", lon=f"{location.longitude:.5f}")

    # 1. Format the tree with indentation before writing
    ET.indent(root, space="    ", level=0)
    return ET.ElementTree(root)


def export_gpx(data: list[Location], gpx_file_name: str) -> None:
    # if os.path.exists(gpx_file_name):
    #     return False, f"File {gpx_file_name} already exists"
    tree = create_xml(data, "Route 11nov2026")
    tree.write(r"C:\Users\erikk\PycharmProjects\GPS\Application\GPX\filename.xml", encoding="utf-8",
    xml_declaration=True)


if __name__ == "__main__":
    export_gpx([], "")
