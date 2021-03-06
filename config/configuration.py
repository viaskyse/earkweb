import os
import string
import ConfigParser

import logging
logger = logging.getLogger(__name__)

root_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
earkweb_version = '0.9.4'
earkweb_version_date = "02.12.2016"

config = ConfigParser.RawConfigParser()
config.read(os.path.join(root_dir, 'config/settings.cfg'))

# earkweb django server
django_service_ip = config.get('server', 'django_service_ip')
django_service_port = config.getint('server', 'django_service_port')

redis_ip = config.get('server', 'redis_ip')
redis_port = config.getint('server', 'redis_port')

# rabbitmq server
rabbitmq_ip = config.get('server', 'rabbitmq_ip')
rabbitmq_port = config.getint('server', 'rabbitmq_port')
rabbitmq_user = config.get('server', 'rabbitmq_user')
rabbitmq_password = config.get('server', 'rabbitmq_password')

# mysql server
mysql_server_ip = config.get('server', 'mysql_server_ip')
mysql_port = config.getint('server', 'mysql_port')
mysql_user = config.get('server', 'mysql_user')
mysql_password = config.get('server', 'mysql_password')
mysql_earkweb_db = config.get('server', 'mysql_earkweb_db')
mysql_celerybackend_db = config.get('server', 'mysql_celerybackend_db')

logger.info("mysql_server_ip: %s" % mysql_server_ip)

# access solr server
access_solr_server_ip = config.get('server', 'access_solr_server_ip')
access_solr_port = config.getint('server', 'access_solr_port')
access_solr_core = config.get('server', 'access_solr_core')

# storage solr server
storage_solr_server_ip = config.get('server', 'storage_solr_server_ip')
storage_solr_port = config.getint('server', 'storage_solr_port')
storage_solr_core = config.get('server', 'storage_solr_core')

# lily content access
lily_content_access_ip = config.get('server', 'lily_content_access_ip')
lily_content_access_port = config.getint('server', 'lily_content_access_port')
lily_content_access_core = config.get('server', 'lily_content_access_core')

# hdfs upload service
hdfs_upload_service_ip = config.get('server', 'hdfs_upload_service_ip')
hdfs_upload_service_port = config.getint('server', 'hdfs_upload_service_port')
hdfs_upload_service_endpoint_path = config.get('server', 'hdfs_upload_service_endpoint_path')
hdfs_upload_service_resource_path = config.get('server', 'hdfs_upload_service_resource_path')

# peripleo
peripleo_server_ip = config.get('server', 'peripleo_server_ip')
peripleo_port = config.getint('server', 'peripleo_port')
peripleo_path = config.get('server', 'peripleo_path')

# flower
flower_server = config.get('server', 'flower_server')
flower_port = config.getint('server', 'flower_port')
flower_path = config.get('server', 'flower_path')

# siard target db and util
siard_dbptk = config.get('server', 'siard_dbptk')
siard_db_type = config.get('server','siard_db_type')
siard_db_host = config.get('server', 'siard_db_host')
siard_db_user = config.get('server', 'siard_db_user')
siard_db_passwd = config.get('server', 'siard_db_passwd')

dip_download_base_url = config.get('access', 'dip_download_base_url')
dip_download_path = config.get('access', 'dip_download_path')

mets_schema_file = os.path.join(root_dir, config.get('schemas', 'mets_schema_file'))
premis_schema_file = os.path.join(root_dir, config.get('schemas', 'premis_schema_file'))

# size limit for direct file display
config_max_filesize_viewer = config.getint('limits', 'config_max_filesize_viewer')

config_path_reception = config.get('paths', 'config_path_reception')
config_path_work = config.get('paths', 'config_path_work')
config_path_storage = config.get('paths', 'config_path_storage')
config_path_access = config.get('paths', 'config_path_access')

# EAD metadata file pattern
metadata_file_pattern_ead =  config.get('metadata', 'metadata_file_pattern_ead')

# location of METS Template
template_METS_path = root_dir + '/lib/metadata/mets/template_METS.xml'

# maximum number of submissions by web client
max_submissions_web_client = 50

server_repo_record_content_query = "http://%s:%d/repository/table/%s/record/{0}/field/n$content/data?ns.n=org.eu.eark" % (lily_content_access_ip, lily_content_access_port, lily_content_access_core)

server_hdfs_aip_query = "http://%s:%d/hsink/fileresource/retrieve_newest?file={0}" % (hdfs_upload_service_ip, hdfs_upload_service_port)

commands = {
    'summain':
        ["/usr/bin/summain", "-c", "SHA256", "-c", "MD5", "--exclude=Ino,Dev,Uid,Username,Gid,Group,Nlink,Mode",
         "--output", string.Template("$manifest_file"), string.Template("$package_dir")],
    'untar':
        ["tar", "-xf", string.Template("$tar_file"), "-C", string.Template("$target_dir")],
    'pdftohtml':
        ["pdftohtml", "-c", "-s", "-noframes", string.Template("$pdf_file"), string.Template("$html_file")],
    'pdftopdfa':
        ['gs', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dUseCIEColor', '-sProcessColorModel=DeviceCMYK', '-sDEVICE=pdfwrite',
         '-sPDFACompatibilityPolicy=1', string.Template('$output_file'), string.Template('$input_file')],
    'totiff':
        ['convert', string.Template('$input_file'), string.Template('$output_file')],
    'blank':
        [string.Template('$command')]
}

# Test settings

test_rest_endpoint_hdfs_upload = "http://%s" % hdfs_upload_service_ip

# NLP settings
stanford_jar = config.get('nlp', 'stanford_jar_path')
stanford_ner_models = config.get('nlp', 'stanford_models_path')
text_category_models = config.get('nlp', 'category_models_path')
config_path_nlp = config.get('nlp', 'config_path_nlp')
nlp_storage_path = config.get('nlp', 'tar_path')

# Solr fields
# {'name': '', 'type': '', 'stored': ''}
# {'name': '', 'type': '', 'stored': '', 'indexed': 'true'}
solr_field_list = [{'name': 'packagetype', 'type': 'string', 'stored': 'true'},
                   {'name': 'package', 'type': 'string', 'stored': 'true'},
                   {'name': 'path', 'type': 'string', 'stored': 'true'},
                   {'name': 'size', 'type': 'long', 'stored': 'true'},
                   {'name': 'confidential', 'type': 'boolean', 'stored': 'true'},
                   {'name': 'textCategory', 'type': 'text_general', 'stored': 'true'},
                   {'name': 'content', 'type': 'text_general', 'stored': 'true', 'indexed': 'true'},
                   {'name': 'contentType', 'type': 'strings', 'stored': 'true'},
                   {'name': 'content_type', 'type': 'strings', 'stored': 'true', 'indexed': 'true'}]
solr_copy_fields = [{'source': 'content_type', 'dest': 'contentType'}]

# Solr config
# {'type':'', 'path': '', 'class': '', 'field_name':'', 'field_value': ''}
solr_config_changes = [{'type': 'update-requesthandler', 'path': '/update/extract', 'class': 'solr.extraction.ExtractingRequestHandler',
                        'fields': {'fmap.content': 'content', 'lowernames': 'true', 'fmap.meta': 'ignored'}}]
