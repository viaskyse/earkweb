from celery import Task
import time, os
from config.config import root_dir
from celery import current_task
from taskresult import TaskResult
import tarfile
from workers.statusvalidation import StatusValidation
from earkcore.metadata.premis.PremisManipulate import Premis
from workflow.ip_state import IpState
import glob
from tasklogger import TaskLogger
import traceback

def init_task2(ip_work_dir, task_name, task_logfile_name):
    start_time = time.time()
    # create working directory
    if not os.path.exists(ip_work_dir):
        os.mkdir(ip_work_dir)
    metadata_dir = os.path.join(ip_work_dir, 'metadata')
    task_log_file = os.path.join(metadata_dir, "%s.log" % task_logfile_name)
    # create log directory
    if not os.path.exists(metadata_dir):
        os.mkdir(metadata_dir)
    # create PREMIS file or return handle to task
    if os.path.isfile(metadata_dir + '/PREMIS.xml'):
        with open(metadata_dir + '/PREMIS.xml', 'rw') as premis_file:
            package_premis_file = Premis(premis_file)
    elif not os.path.isfile(metadata_dir + '/PREMIS.xml'):
        # TODO: dependency to root directory must be removed! PREMIS_skeleton not necessary
        premis_skeleton_file = root_dir + '/earkresources/PREMIS_skeleton.xml'
        with open(premis_skeleton_file, 'r') as premis_file:
            package_premis_file = Premis(premis_file)
        package_premis_file.add_agent('eark-aip-creation')
    tl = TaskLogger(task_log_file)
    tl.addinfo(("%s task %s" % (task_name, current_task.request.id)))
    return tl, start_time, package_premis_file


def add_PREMIS_event(task, outcome, identifier_value,  linking_agent, package_premis_file,
                     tl, ip_work_dir):
    '''
    Add an event to the PREMIS file and update it afterwards.
    '''
    package_premis_file.add_event(task, outcome, identifier_value, linking_agent)
    path_premis = os.path.join(ip_work_dir, "metadata/PREMIS.xml")
    with open(path_premis, 'w') as output_file:
        output_file.write(package_premis_file.to_string())
    tl.addinfo('PREMIS file updated: %s (%s)' % (path_premis, outcome))

def finalize_task(uuid, tl, state_code, ip_state_xml, add_result_params={}):
    """
    Finalize logging task. Can be called several times to get an updated result object.
    @rtype:     TaskResult
    @return:    Task result (success/failure, processing log, error log)
    """
    if tl.path is not None and not tl.task_logfile.closed:
        tl.task_logfile.close()
    ip_state_xml.write_doc(ip_state_xml.get_doc_path())
    # TaskResult:           (uuid, state_code, success,          log,    err,    additional_result_params)
    task_result = TaskResult(uuid, state_code, len(tl.err) == 0, tl.log, tl.err, add_result_params)
    return task_result

class DefaultTask(Task, StatusValidation):

    expected_status = "status!=-9999"
    success_status = 0
    error_status = 0

    task_name = "DefaultTask"

    def run_task(self, uuid, path, tl, additional_params):
        """
        This method is overriden by the task method implementation
        @type tl: list[str]
        @param tl: Task log
        @return: Additional result parameters dictionary
        """
        tl.addinfo("Executing default task (to be overridden)")
        return {}

    def run(self, uuid, path, additional_params, *args, **kwargs):
        """
        Default task

        @type       uuid: str
        @param      uuid: Internal identifier

        @type       path: str
        @param      path: Path where the IP is stored

        @type       path: additional_params
        @param      path: Additional parameters dictionary (passed throuh from actual task implementation to celery result)

        @rtype:     TaskResult
        @return:    Task result (success/failure, processing log, error log, additional parameters)
        """
        add_result_params = {}
        # task name is name of instantiating class (concrete task implementation)
        self.task_name = str(self.__name__)
        # initialize task
        tl, start_time, package_premis_file = init_task2(path, self.task_name, "earkweb")
        tl.addinfo("Processing package %s" % uuid)
        self.update_state(state='PROGRESS', meta={'process_percent': 1})
        try:
            # get state, try reading current state from state.xml, otherwise set default to is error state,
            # which must then be set to success state explicitely.
            ip_state_doc_path = os.path.join(path, "state.xml")
            ip_state_xml = IpState.from_parameters(self.error_status, False)
            if os.path.exists(ip_state_doc_path):
                ip_state_xml = IpState.from_path(ip_state_doc_path)
            ip_state_xml.set_doc_path(ip_state_doc_path)

            # check state
            tl.err = self.valid_state(ip_state_xml.get_state(), self.expected_status)
            if len(tl.err) > 0:
                return finalize_task(uuid, tl, self.error_status, ip_state_xml)

            # executing actual task implementation; can return additional result parameters
            # in the dictionary returned. This dictionary is stored as part of the celery result
            # and is stored in the result backend (AsyncResult(task_id).result.add_res_parms).
            add_result_params = self.run_task(uuid, path, tl, additional_params)

            # set status to error status of the task if errors occurred during task execution.
            if len(tl.err) > 0:
                return finalize_task(uuid, tl, self.error_status, ip_state_xml)

            # finalize task
            ip_state_xml.set_state(self.success_status)
            ip_state_xml.write_doc(ip_state_doc_path)
            self.update_state(state='PROGRESS', meta={'process_percent': 100})
            add_PREMIS_event('SIPDeliveryValidation', 'SUCCESS', 'identifier', 'agent', package_premis_file, tl, path)
            print "Default task: set status to: %s" % self.success_status
            return finalize_task(uuid, tl, self.success_status, ip_state_xml, add_result_params)
        except Exception:
            traceback.print_exc()
            add_PREMIS_event('SIPDeliveryValidation', 'FAILURE', 'identifier', 'agent', package_premis_file, tl, path)
            return finalize_task(uuid, tl, self.error_status, ip_state_xml)