"""Script that downloads linked data from Omeka S API and fixes namespace issues."""

from rdflib import Graph, URIRef
import requests

### Configuration
# Path to save file
EXPORT_PATH = "api-export.ttl"
# URI to Omeka S endpoint
BASE_URI = "https://muurschilderingendatabase.nl/"
# Defines the format of the output file
OUTPUT_FILE_FORMAT = "trig"
# Defines the graph identifier 
GRAPH_ID = "muurschildering-origineel"
### End of Configuration

graph = Graph(identifier=GRAPH_ID)

# retrieve items fron api endpoint
with open(EXPORT_PATH, "w", encoding="utf-8") as file:
    # Temporary subset to make testing faster
    for page in range(1,50):
        PAGE_URL = f"{BASE_URI}api/items?format=turtle&page={page}&per_page=100"
        data = requests.get(PAGE_URL)
        file.write(data.text)

    graph.parse(EXPORT_PATH)

    # retrieve namespaces from api-context endpoint
    namespace_response = requests.get(BASE_URI+"api-context")
    response_data = namespace_response.json()
    namespace_data = response_data["@context"]

    for key in namespace_data:
        ns = URIRef(namespace_data[key])
        print(f"binding namespace {ns} as {key}")
        graph.namespace_manager.bind(key, ns, override=True, replace=True)

    graph.serialize(format=OUTPUT_FILE_FORMAT, destination=f"api-export.{OUTPUT_FILE_FORMAT}")
