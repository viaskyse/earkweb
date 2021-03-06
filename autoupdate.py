import subprocess32
import time
import os
import ConfigParser
from earkcore.utils.configutils import set_default_config_if_not_exists


""" This script performs an update of EARKweb. This includes:
* db migrations
* updates to Solr schema
* updating existing/adding new Celery tasks
"""

# check for missing configuration options
default_config = [
    ("nlp", "tar_path", "/var/data/earkweb/nlp/tarfiles"),
    ("server", "peripleo_server_ip", "127.0.0.1"),
    ("server", "peripleo_port", 9000),
    ("server", "peripleo_path", "peripleo"),
    ("server", "siard_dbptk", "/usr/local/bin/dbptk-app-2.0.0-beta3.2.5.jar"),
    ("server", "siard_db_type", "mysql"),
    ("server", "siard_db_host", "localhost"),
    ("server", "siard_db_user", "root"),
    ("server", "siard_db_passwd", "password"),
    ("server", "flower_server", "127.0.0.1"),
    ("server", "flower_port", "5555"),
    ("server", "flower_path", "/"),
    ("access", "dip_download_base_url", "http://127.0.0.1:8000/static/earkweb/download"),
    ("access", "dip_download_path", "/opt/python_wsgi_apps/earkweb/static/download"),

]

from config.configuration import solr_field_list, solr_copy_fields, solr_config_changes, root_dir

set_default_config_if_not_exists(os.path.join(root_dir,'config/settings.cfg'), default_config)

# colour codes
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# # requirements.txt: install new requirements
# print '\033[95m' + '----------------\nNow updating from requirements.txt.\n----------------' + '\033[0m'
# req_update_args = ['pip', 'install', '-r', 'requirements.txt']
# update_process = subprocess32.Popen(req_update_args)
# update_out, update_err = update_process.communicate()
# if update_err is not None:
#     print WARNING + 'There have been errors when updating from requirements.txt:\n' + '\033[0m'
#     print update_err

# migrations - prepare
cwd = "/earkweb" if os.path.exists("/earkweb") else root_dir
print HEADER + '----------------\nNow preparing database migrations.\n----------------' + ENDC
migrations_update_args = ['python', 'manage.py', 'makemigrations', 'earkcore']
migrations_process = subprocess32.Popen(migrations_update_args, cwd=cwd)
migrations_out, migrations_err = migrations_process.communicate()
if migrations_err is not None:
    print WARNING + 'There have been errors when performing "earkcore" migrations:\n' + ENDC
    print migrations_err
migrations_update_args = ['python', 'manage.py', 'makemigrations']
migrations_process = subprocess32.Popen(migrations_update_args, cwd=cwd)
migrations_out, migrations_err = migrations_process.communicate()
if migrations_err is not None:
    print WARNING + 'There have been errors when performing migrations:\n' + ENDC
    print migrations_err

# migrations - apply
print HEADER + '----------------\nNow applying database migrations.\n----------------' + ENDC
migrations_update_args = ['python', 'manage.py', 'migrate']
migrations_process = subprocess32.Popen(migrations_update_args, cwd=cwd)
migrations_out, migrations_err = migrations_process.communicate()
if migrations_err is not None:
    print WARNING + 'There have been errors when performing migrations:\n' + ENDC
    print migrations_err

# scan for new/updated Celery tasks
print HEADER + '----------------\nNow scanning for new/updated Celery tasks.\n----------------' + ENDC
taskscan_args = ['python', 'workers/scantasks.py']
taskscan_process = subprocess32.Popen(taskscan_args, cwd=cwd)
taskscan_out, taskscan_err = taskscan_process.communicate()
if taskscan_err is not None:
    print WARNING + + 'There have been errors when updating Celery tasks:\n' + ENDC
    print taskscan_err

from config.configuration import storage_solr_server_ip
from config.configuration import storage_solr_port
from config.configuration import storage_solr_core

local_solr_core_uri = 'http://%s:%d/solr/%s' % (storage_solr_server_ip, storage_solr_port, storage_solr_core)

# Solr: create new fields
print HEADER + '----------------\nNow adding new Solr fields.\n----------------' + ENDC
for field in solr_field_list:
    print OKBLUE + '## Adding new field: %s ##' % field['name'] + ENDC
    # simple field with name, type, stored parameter
    solr_fields_args = ['curl', '-X', 'POST', '-H', '\'Content-type:application/json\'',
                        '--data-binary', '{"add-field": {"name": "%s", "type": "%s", "stored": "%s"}}' % (field['name'], field['type'], field['stored']),
                        '%s/schema' % local_solr_core_uri]
    try:
        # check if 'indexed' is set (additional to parameters above)
        if field['indexed']:
            solr_fields_args = ['curl', '-X', 'POST', '-H', '\'Content-type:application/json\'',
                                '--data-binary', '{"add-field": {"name": "%s", "type": "%s", "stored": "%s", "indexed": "%s"}}' % (field['name'], field['type'], field['stored'], field['indexed']), '%s/schema' % local_solr_core_uri]
    except KeyError:
        # expected behaviour if 'indexed' is not set
        pass

    solr_fields_process = subprocess32.Popen(solr_fields_args)
    solr_fields_out, solr_fields_err = solr_fields_process.communicate()
    if solr_fields_err is not None:
        print WARNING + 'There have been errors when updating Solr fields:\n' + ENDC
        print solr_fields_err

time.sleep(2.5)

for field in solr_copy_fields:
    print OKBLUE + '## Adding new copy-field: from %s to %s ##' % (field['source'], field['dest']) + ENDC
    solr_fields_args = ['curl', '-X', 'POST', '-H', '\'Content-type:application/json\'',
                        '--data-binary', '{"add-copy-field": {"source": "%s", "dest": "%s"}}' % (field['source'], field['dest']),
                        '%s/schema' % local_solr_core_uri]

    solr_fields_process = subprocess32.Popen(solr_fields_args)
    solr_fields_out, solr_fields_err = solr_fields_process.communicate()
    if solr_fields_err is not None:
        print WARNING + 'There have been errors when updating Solr fields:\n' + ENDC
        print solr_fields_err

print HEADER + '----------------\nNow editing the Solr config.\n----------------' + ENDC
for change in solr_config_changes:
    print OKBLUE + '## Editing class: %s ##' % change['class'] + ENDC
    solr_config_args = ['curl', '%s/config' % local_solr_core_uri, '-H', '\'Content-type:application/json\'',
                        '-d', '{"%s":{"name":"%s", "class":"%s", "defaults": %s}}' %
                        (change['type'], change['path'], change['class'], change['fields'])]
    solr_change_process = subprocess32.Popen(solr_config_args)
    solr_change_out, solr_change_err = solr_change_process.communicate()
    if solr_change_err is not None:
        print WARNING + 'There have been errors when updating the Solr config file:\n' + ENDC
        print solr_change_err
