import os
root_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
mets_schema_file = os.path.join(root_dir, 'earkresources/schemas/mets_1_11.xsd')
premis_schema_file = os.path.join(root_dir, 'earkresources/schemas/premis-v2-2.xsd')