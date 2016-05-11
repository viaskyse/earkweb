import os
import string
import ConfigParser

root_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(root_dir, 'config/settings.cfg'))

# earkweb django server
django_service_ip = config.get('server', 'django_service_ip')
django_service_port = config.getint('server', 'django_service_port')

# mysql server
mysql_server_ip = config.get('server', 'mysql_server_ip')

# access solr server
access_solr_server_ip = config.get('server', 'access_solr_server_ip')
access_solr_port = config.getint('server', 'access_solr_port')
access_solr_core = config.get('server', 'access_solr_core')

# storage solr server
local_solr_server_ip = config.get('server', 'storage_solr_server_ip')
local_solr_port = config.getint('server', 'storage_solr_port')
local_solr_core = config.get('server', 'storage_solr_core')

# lily content access
lily_content_access_ip = config.get('server', 'lily_content_access_ip')
lily_content_access_port = config.getint('server', 'lily_content_access_port')
lily_content_access_core = config.get('server', 'lily_content_access_core')

# hdfs upload service
hdfs_upload_service_ip = config.get('server', 'hdfs_upload_service_ip')
hdfs_upload_service_port = config.getint('server', 'hdfs_upload_service_port')

mets_schema_file = os.path.join(root_dir, config.get('schemas', 'mets_schema_file'))
premis_schema_file = os.path.join(root_dir, config.get('schemas', 'premis_schema_file'))

# size limit for direct file display
config_max_filesize_viewer = config.getint('limits', 'config_max_filesize_viewer')

config_path_reception = config.get('paths', 'config_path_reception')
config_path_ingest = config.get('paths', 'config_path_ingest')
config_path_work = config.get('paths', 'config_path_work')
config_path_storage = config.get('paths', 'config_path_storage')
config_path_access = config.get('paths', 'config_path_access')

# location of METS Template
template_METS_path = root_dir + '/lib/metadata/mets/template_METS.xml'

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