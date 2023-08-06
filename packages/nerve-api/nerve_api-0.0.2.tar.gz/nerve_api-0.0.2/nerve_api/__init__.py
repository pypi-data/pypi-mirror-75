"""
This module provides examples to provision, deploy, undeploy, delete, start and stop workloads.

Quickstart example::

    >>> import nerve_api
    >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
    >>> nerve_api.workload_list(conn)
    [{'_id': ...
    >>> nerve_api.node_list(conn)
    [{'_id': ...
    >>> nerve_api.create_docker_workload(conn, 'TestDocker.json')
    <Response [200]>
    >>> nerve_api.deploy_workload(conn, 'PrometheusAPItest217', 'prom','v1.0', ['012345678901'], 'Demo Deployment')
    <Response [200]>

Detailed function descriptions are provided as Sphinx API docs in each function.

"""

import argparse
import json
from http import HTTPStatus
from json import loads
from threading import Thread
from time import sleep
from urllib.parse import urljoin

import requests
from requests import get, put, post
from requests_toolbelt import (MultipartEncoder)


class RelativeSession(requests.Session):
    """Session that automatically uses the hostname, so we don't have to pass it for each function.

    .. see also:: https://stackoverflow.com/a/28337825
    """

    def __init__(self, base_url):
        super(RelativeSession, self).__init__()
        self.__base_url = base_url

    def request(self, method, url, **kwargs):
        url = urljoin(self.__base_url, url)
        return super(RelativeSession, self).request(method, url, **kwargs)


def search(name_element, name, lis):
    """Allows to specify a field name and its value as filter for a list

    This can be used to eg to retrieve versions of workloads with a specified name

    Parameters
    ----------
    name_element : str
        Name of the element inside the list that we are searching for.
    name : str
        This is the value of `name_element` that we are searching for.
    lis : list
        List to be searched

    Returns
    ----------
    list
        A list of elements where `name_element` matches `name`

    Example
    -------
    >>> workload_id = nerve_api.workload_id(conn, 'Prometheus')
    >>> p = nerve_api.workload_versions(conn, workload_id)
    >>> t = p['versions']
    >>> w = nerve_api.search('name', 'prom', t).

    """
    return [element for element in lis if element[name_element] == name]


def node_list(conn):
    """Get a list of nodes.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.

    Returns
    -------
    list[dict]
        A list of nodes in form of a list of dictionaries.

    """
    try:
        return conn.get('/nerve/nodes/list').json()
    except AttributeError:
        print('ERROR: No connection with the mgmt system')


def label_list(conn):
    """Get a list of labels.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    Returns
    -------
    list
        A list, where the first element of the list specifies the length of the list,
        and the second element is a list of dictionaries of all labels.

    """
    try:
        return conn.get('/nerve/labels/list').json()
    except AttributeError:
        print('ERROR: No connection with the mgmt system')


def get_label_id(conn, label_key, label_value):
    """Get the label id of a specified label.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    label_key : str
        The name of the key of the label
    label_value : str
        The value to the key of the label

    Returns
    -------
    str
        Label id of the specified key value pair

    """
    try:
        list_label = search('value', label_value, search('key', label_key, label_list(conn)['data']))
        return list_label[0]['_id']
    except TypeError:
        pass
    except IndexError:
        print('ERROR: Combination with that key:value pair for label doesnt exist')


def change_input_to_label_ids(conn, list_label):
    """Converts a list of labels in the form of a key value pair to their respective ids

    It will return the list of label_ids in form of ['labelid1','labelid2'].

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    list_label : list of label strings
        A list of key value paired labels like ['keylabel1:valuelabel','keylabel2:valuelabel']

    Returns
    -------
    list
    	List of label ids.

    """
    q = []
    for i in list_label:
        p = get_label_id(conn, i.split(':')[0], i.split(':')[1])
        q.append(p)
    return q


def workload_list(conn):
    """Get a list of workloads.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.

    Returns
    -------
    list
        List of workloads in form of list of dictionaries.

    """
    try:
        return conn.get('/nerve/workload/list').json()['data']
    except AttributeError:
        print('ERROR: No connection with the mgmt system')


def workload_versions(conn, workload_id):
    """Get all versions of a given workload.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload_id : str
        Value of workload Id

    Returns
    -------
    dict
        Versions of specific workload in form of dictionary.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> workload_id = nerve_api.workload_id(conn, 'Name of Workload')
        >>> nerve_api.workload_versions(conn, workload_id)
        {'_id': ...}

    """
    try:
        return conn.get('/nerve/workload/' + workload_id).json()
    except TypeError:
        print('ERROR: Workload with this ID doesnt exist')
    except AttributeError:
        pass


def get_workload_ids_on_node(conn, serial_number):
    """ Get the ids of all workloads on a specified node.

    Parameters
    ----------
    serial_number : str
        Serial number of node

    Returns
    -------
    list[dict]
        List of dictionaries which contains all deployed workloads on the node.
    """

    response = conn.get('/nerve/workload/node/%s/devices' % serial_number).json()
    try:
        if response[0]['message']:
            print('ERROR: ' + response[0]['message'])
    except (KeyError, AttributeError, IndexError):
        pass
    return response


def workload_id(conn, workload_name):
    """Get the ID of a workload.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload_name : str
        Name of workload

    Returns
    -------
    workload_id : str
        The id of the workload.

    """
    try:
        q = workload_list(conn)
        p = search('name', workload_name, q)
        return p[0]['_id']
    except IndexError:
        print('ERROR: Workload with this name doesnt exist')
    except TypeError:
        pass


def version_id(conn, version_name, release_name, workload_id):
    """ Get the version id of a specified workload

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    version_name : str
        Name of version
    release_name : str
        Name of release of upper version
    workload_id : str
        Workload id as returned by `nerve_api.workload_id`

    Returns
    -------
    str
        Version Id

    """
    try:
        p = workload_versions(conn, workload_id)
        t = p['versions']
        w = search('name', version_name, t)
        w = search('releaseName', release_name, w)
        return w[0]['_id']
    except IndexError:
        print('ERROR: There is no version or release like that on this workload')
    except TypeError:
        print('ERROR: Wrong ID of workload')


def get_workload_id_on_node(conn, workload, serial):
    """Get the id of a workload which is deployed on the node (node view).

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload : str
        Name of workload
    serial : str
        Serial number of the Node.

    Returns
    -------
    str
        Workload id as stored on the node (different than id on the management system)

    """
    try:
        p = get_workload_ids_on_node(conn, serial)
        q = search('device_name', workload, p)
        return q[0]['id']
    except IndexError:
        print('ERROR: There is no workload with this name on node')
    except KeyError:
        pass


def deploy_workload(conn, workload, version, release_name, nodes, deploy_name, dry_run=False, retry=3):
    """Deploy a workload to a set of Nodes.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload : str
        Name of workload
    version : str
        Version of the workload
    release_name:
        Release name of the version
    nodes : str in ['SerialNumber1,SerialNumber2']
        List of serial numbers
    deploy_name : str
        Name of deployment, only used to identify a particular deployment.
        Keep in mind if the deploy name is already used, deployment wont be possible.

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of current node, workload and status of deployment.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.deploy_workload(conn, 'Example Workload', 'Example Version', 'Example release', ['012345678901'], 'NAME')
        <Response [200]>

    """
    wid = workload_id(conn, workload)
    data = {
        "deployName": deploy_name,
        "dryRun": dry_run,
        "nodes": nodes,
        "retryTimes": retry,
        "versionId": version_id(conn, version, release_name, wid),
        "workloadId": wid,
    }
    return conn.post('/bom/nerve/workload/deploy', json=data)


def add_remote_screen_to_workload(conn, workload_name, workload_version, workload_release, name, port_number, password,
                                  connection):
    """Add remote screen to workload

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload_name : str
        Name of workload
    workload_version : str
        Version of the workload
    workload_release:
        Release name of the version
    name:
        Name for remote screen on workload
    port_number:
        Port on the node
    password:
        Password for the remote screen
    connection:
        Specify the type of connection either VNC, SSH or RDP.


    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the version section with the new remote screen connection.

    """
    try:
        workloadid = workload_id(conn, workload_name)
        versionid = version_id(conn, workload_version, workload_release, workloadid)
        data = {
            "connection": {
                "connection": connection,
                "acknowledgment": "No",
                "numberOfConnections": 1,
                "port": port_number,
                "autoretry": 1,
                "swapRedBlue": False,
                "readOnly": False,
                "type": "SCREEN",
                "securityMode": "",
                "ignoreServerCertificate": False,
                "name": name,
                "password": password,
                "username": None,
                "privateKey": None
            }
        }
        return conn.post('/nerve/remoteConnections/' + versionid, json=data)
    except TypeError:
        pass


def add_remote_tunnel_to_workload(conn, workload_name, workload_version, workload_release, name, port, local_port):
    """Add remote tunnel to workload

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload_name : str
        Name of workload
    workload_version : str
        Version of the workload
    workload_release:
        Release name of the version
    name:
        Name for remote screen on workload
    port:
        Port on the node
    local_port:
        Port on the PC

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the version section with the new remote tunnel connection.

    """
    try:
        workloadid = workload_id(conn, workload_name)
        versionid = version_id(conn, workload_version, workload_release, workloadid)
        data = {
            "connection": {
                "type": "TUNNEL",
                "acknowledgment": "No",
                "name": name,
                "port": port,
                "localPort": local_port
            }
        }
        return conn.post('/nerve/remoteConnections/' + versionid, json=data)
    except TypeError:
        pass


def delete_workload(conn, workload):
    """Delete a Workload from the Management System.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload : str
        Name of workload.

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the current deleted workload.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.delete_workload('Example Workload')
        <Response [200]>


    """
    try:
        return conn.delete('/nerve/workload/' + workload_id(conn, workload))
    except TypeError:
        print('ERROR: Workload with that name doesnt exist')


def undeploy_workload(conn, node, workload):
    """Undeploy a workload from a node.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    node : str
        The serial number of the node.
    workload : str
        The name of the Workload.

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of current node, workload and status of undeployment.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.undeploy_workload('012345678901', Example Workload')
        <Response [200]>



    """
    dev_id = get_workload_id_on_node(conn, workload, node)
    payload = {
        "command": "UNDEPLOY",
        "forceStop": False,
        "serialNumber": node,
        "timeout": 0,
        "sessionToken": "dummy",
        "deviceId": dev_id,
    }
    return conn.post('/nerve/workload/controller', json=payload)


def start_workload(conn, node, workload, timeout=0):
    """Start a Workload on a node.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    node : str
        The serial number of the node.
    workload : str
        The name of the Workload.
    timeout : int, optional
        Time to wait until response.

    Returns
    -------
    str
        Status code for starting the current workload.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.start_workload('012345678901', Example Workload')
        <Response [200]>

    """
    dev_id = get_workload_id_on_node(conn, workload, node)
    payload = {
        "command": "START",
        "forceStop": False,
        "serialNumber": node,
        "timeout": timeout,
        "sessionToken": "dummy",
        "deviceId": dev_id,
    }
    return conn.post('/nerve/workload/controller', json=payload)


def stop_workload(conn, node, workload, force_stop=False, timeout=0):
    """Stop a workload on a node.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    node : str
        The serial number of the node.
    workload : str
        The name of the Workload.

    Returns
    -------
    str
        Status code for stopping the current workload.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.stop_workload('012345678901', Example Workload')
        <Response [200]>


    """
    dev_id = get_workload_id_on_node(conn, workload, node)
    payload = {
        "command": "STOP",
        "forceStop": force_stop,
        "serialNumber": node,
        "timeout": timeout,
        "sessionToken": "dummy",
        "deviceId": dev_id,
    }
    return conn.post('/nerve/workload/controller', json=payload)


def restart_workload(conn, node, workload):
    """Restart a workload.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    node : str
        The serial number of the node.
    workload : str
        The name of the Workload.

    Returns
    -------
    str
        Status code for restarting the current workload.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.restart_workload(conn, '012345678901', 'Example Workload')
        <Response [200]>


    """
    dev_id = get_workload_id_on_node(conn, workload, node)
    payload = {
        "command": "RESTART",
        "forceStop": False,
        "serialNumber": node,
        "timeout": 0,
        "sessionToken": "dummy",
        "deviceId": dev_id,
    }
    return conn.post('/nerve/workload/controller', json=payload)


def create_docker_workload(conn, data_file, tar_file=None, list_label=None):
    """Create a Docker workload.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    data_file : .json file
        Datafile that goes in as body
    tar_file : path, optional
        Instead of pulling the Docker image from a registry, use the image located at `tar_file`.
    list_label:
        List of labels that needs to be specified, if user wants to add it in form of list ['labelkey1:labelvalue1','labelkey2:labelvalue2'].

    Warning
    -------
    The tuple of version name and version release in the json file needs to be unique

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the new docker workload.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.create_docker_workload(conn, 'TestDocker.json')
        <Response [200]>
        >>> nerve_api.create_docker_workload(conn, 'TestTarDocker.json', tar_file='remoteview_light.tar',list_label=['keylabel1:value','keylabel2:value'])
        <Response [200]>

    """
    try:
        with open(data_file) as stream:
            dic = json.load(stream)
        if list_label:
            dic['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
        files = []
        if tar_file:
            tar_file = open(tar_file, 'rb')
            postData = {'data': json.dumps(dic),
                        'file': (tar_file.name, tar_file, 'application/octet-stream')
                        }
            e = MultipartEncoder(fields=postData)
            return conn.post('/nerve/workload', data=e, headers={'Content-Type': e.content_type})
        else:
            return conn.post('/nerve/workload', data={'data': json.dumps(dic)}, files=files)
    except FileNotFoundError:
        print('ERROR: Wrong file name')


def create_codesys_workload(conn, data_file, zip_file, list_label=None):
    """Create a CODESYS workload.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    data_file : .json file
        Datafile that goes in as body
    zip_file : .zip file
        Codesys .zip file
    list_label:
        List of labels that needs to be specified, if user wants to add it in form of list ['labelkey1:labelvalue1','labelkey2:labelvalue2'].

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the new codesys workload.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.create_codesys_workload(conn, 'TestCodesys.json', 'CodesysApp.zip', list_label=['keylabel1:value','keylabel2:value'])
        <Response [200]>


    """
    try:
        with open(data_file) as stream:
            dic = json.load(stream)
        if list_label:
            dic['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
        zip_file = open(zip_file, 'rb')
        postData = {'data': json.dumps(dic),
                    'file': (zip_file.name, zip_file, 'application/octet-stream')
                    }
        e = MultipartEncoder(fields=postData)
        return conn.post('/nerve/workload', data=e, headers={'Content-Type': e.content_type})
    except FileNotFoundError:
        print('ERROR: Wrong file name')


def create_vm_workload(conn, data_file, raw_file_name, xml_file_name, list_label=None):
    """Create VM workload.

    Parameters
    ----------
    data_file : json
        DESCRIPTION.
    raw_file_name : raw file
        DESCRIPTION.
    xml_file_name : xml file

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the new vm workload.

    Example
    -------
        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.create_vm_workload(conn, 'TestVM.json', 'alpine.raw', 'alpine.xml', list_label=['keylabel1:value','keylabel2:value'])
        <Response [200]>


    """
    try:
        with open(data_file) as stream:
            dic = json.load(stream)
        if list_label:
            dic['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
        raw_file = open(raw_file_name, 'rb')
        xml_file = open(xml_file_name, 'rb')

        postData = {'data': json.dumps(dic),
                    'file1': (raw_file.name, raw_file, 'application/octet-stream'),
                    'file2': (xml_file.name, xml_file, 'plain/text')
                    }
        e = MultipartEncoder(fields=postData)
        return conn.post('/nerve/workload', data=e, headers={'Content-Type': e.content_type})
    except FileNotFoundError:
        print('ERROR: Wrong file name')


def create_new_version_to_existing_docker_workload(conn, workload, data_file, tar_file=None, list_label=None):
    """Create additional version of docker workload.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload:
        Name of workload on management system.
    data_file : .json file
        Datafile that goes in as body (same one for creating docker workload), for this function it only takes version part.
    tar_file : path, optional
        Instead of pulling the Docker image from a registry, use the image located at `tar_file`.
    list_label : list, optional
        List of labels that needs to be specified, if user wants to add it in form of list ['labelkey1:labelvalue1','labelkey2:labelvalue2'].

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the new version of the current docker workload.
    """
    try:
        with open(data_file) as stream:
            dic = json.load(stream)
        workloadId = workload_id(conn, workload)
        data_final = workload_versions(conn, workloadId)
        files = []
        t = data_final['versions']
        files_value = t[0]['files']
        data_final['versions'] = dic['versions']
        if list_label:
            data_final['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
        if tar_file:
            files_value[0]['originalName'] = tar_file
            data_final['versions'][0]['files'] = files_value
            tar_file = open(tar_file, 'rb')
            postData = {'data': json.dumps(data_final),
                        'file': (tar_file.name, tar_file, 'application/octet-stream')
                        }
            e = MultipartEncoder(fields=postData)
            return conn.patch('/nerve/workload', data=e, headers={'Content-Type': e.content_type})
        else:
            return conn.patch('/nerve/workload', data={'data': json.dumps(data_final)}, files=files)
    except FileNotFoundError:
        print('ERROR: Wrong file name')
    except TypeError:
        pass


def use_files_of_any_workload(conn, workload, version, release, data_file, list_label=None):
    """ Create a new version while using files from a previously created version.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload:
        Name of workload on management system.
    version:
        Name of version.
    release:
        Name of release.
    data_file : .json file
        Datafile that goes in as body, for this function it only takes version part.
        For each workload, its own json needs to be sent, like for creating workload. (Docker.json, Codesys.json and VM.json)
    list_label:
        List of labels that needs to be specified, if user wants to add it in form of list ['labelkey1:labelvalue1','labelkey2:labelvalue2'].

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the new version of the current workload.
    """
    try:
        with open(data_file) as stream:
            dic = json.load(stream)
        files = None
        workloadId = workload_id(conn, workload)
        data_final = workload_versions(conn, workloadId)
        t = data_final['versions']
        w = search('name', version, t)
        w = search('releaseName', release, w)
        files_value = w[0]['files']
        data_final['versions'] = dic['versions']
        if list_label:
            data_final['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
        data_final['versions'][0]['files'] = files_value
        return conn.patch('/nerve/workload', data={'data': json.dumps(data_final)}, files=files)
    except FileNotFoundError:
        print('ERROR: Wrong file name')
    except TypeError:
        pass
    except IndexError:
        print('ERROR: Check version and release name')


def create_new_version_to_existing_codesys_workload(conn, workload, data_file, zip_file, list_label=None):
    """Create a new version of CODESYS workload.

    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload:
        Name of workload on management system.
    data_file : .json file
        Datafile that goes in as body ( same one for creating codesys workload), for this function it only takes version part.
    zip_file : .zip file
        Codesys .zip file
    list_label:
        List of labels that needs to be specified, if user wants to add it in form of list ['labelkey1:labelvalue1','labelkey2:labelvalue2'].

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the new version of the current codesys workload.

    Warning
    -------
    The tuple of version name and version release in the json file needs to be unique


    """
    try:
        with open(data_file) as stream:
            dic = json.load(stream)
        workloadId = workload_id(conn, workload)
        data_final = workload_versions(conn, workloadId)
        t = data_final['versions']
        files_value = t[0]['files']
        data_final['versions'] = dic['versions']
        if list_label:
            data_final['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
        files_value[0]['originalName'] = zip_file
        data_final['versions'][0]['files'] = files_value
        zip_file = open(zip_file, 'rb')
        postData = {'data': json.dumps(data_final),
                    'file': (zip_file.name, zip_file, 'application/octet-stream')
                    }
        e = MultipartEncoder(fields=postData)
        return conn.patch('/nerve/workload', data=e, headers={'Content-Type': e.content_type})
    except FileNotFoundError:
        print('ERROR: Wrong file name')
    except TypeError:
        pass

      
def create_docker_workload_multi(conn, dic, tar_file=None, list_label=None):
    """Create a Docker workload.

    Example::

        >>> conn = nerve_api.get_connection(url='...', user='...', password='...')
        >>> nerve_api.create_docker_workload(conn, 'TestDocker.json')
        <Response [200]>
        >>> nerve_api.create_docker_workload(conn, 'TestTarDocker.json', tar_file='remoteview_light.tar',list_label=['keylabel1:value','keylabel2:value'])
        <Response [200]>

    Parameters
    ----------

    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    data_file : .json file
        Datafile that goes in as body
    tar_file : path, optional
        Instead of pulling the Docker image from a registry, use the image located at `tar_file`.
    """
    if list_label:
        dic['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
    files = []
    if tar_file:
        files = [('files', open(tar_file, 'rb'))]

    return conn.post('/nerve/workload', data={'data': json.dumps(dic)}, files=files)


def create_new_version_to_existing_vm_workload(conn, workload, data_file, raw_file, xml_file, list_label=None):
    """Create new version of VM workload.
    Parameters
    ----------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.
    workload:
        Name of workload on management system.
    data_file : json
        Datafile that goes in as body (same one for creating vm workload), for this function it only takes version part.
    raw_file: raw file
        Raw image file of the VM
    xml_file: xml file
        xml file specifying the VM
    list_label: list
        List of labels that needs to be specified, if user wants to add it in form of list ['labelkey1:labelvalue1','labelkey2:labelvalue2'].

    Returns
    -------
    list[dict]
        List of dictionary containing the parameters of the new version of the current vm workload.

    Warning
    -------
    The tuple of version name and version release in the json file needs to be unique


    """
    try:
        with open(data_file) as stream:
            dic = json.load(stream)
        workloadId = workload_id(conn, workload)
        data_final = workload_versions(conn, workloadId)
        t = data_final['versions']
        files_value = t[0]['files']
        data_final['versions'] = dic['versions']
        if list_label:
            data_final['versions'][0]['selectors'] = change_input_to_label_ids(conn, list_label)
        files_value[0]['originalName'] = raw_file
        files_value[1]['originalName'] = xml_file
        data_final['versions'][0]['files'] = files_value
        raw_file = open(raw_file, 'rb')
        xml_file = open(xml_file, 'rb')
        postData = {'data': json.dumps(data_final),
                    'file1': (raw_file.name, raw_file, 'application/octet-stream'),
                    'file2': (xml_file.name, xml_file, 'plain/text')
                    }
        e = MultipartEncoder(fields=postData)
        return conn.patch('/nerve/workload', data=e, headers={'Content-Type': e.content_type})
    except FileNotFoundError:
        print('ERROR: Wrong file name')
    except TypeError:
        pass


def apply_gateway_config(conn, config):
    """
    Applies the configuration string in the parameter config to the gateway on the Management System and restarts the gateway

    Parameters
    ----------
    config : str
        The configuration string of the gateway on the Management System in JSON format
    """
    check_response(conn.put('/dp/api/config', json={'config': loads(config)}))
    check_response(conn.get('/dp/api/restart/gw'))


def get_connection(url, user, password):
    """Get a connection object to the Management System.

    Returns
    -------
    conn : RelativeSession
        A connection as retrieved by `get_connection()`.

    """
    try:
        conn = RelativeSession(url)
        resp = conn.post('/auth/login', json={
            'identity': user,
            'secret': password,
        })
        if resp.status_code != HTTPStatus.OK:
            raise RuntimeError('Error: Could not authenticate to Management System')

        # set the session id as cookie (it's delivered as header, not as set-cookie)
        session_id = resp.headers['sessionid']
        conn.cookies['sessionid'] = session_id
        conn.headers['sessionid'] = session_id  # also add as header - both is necessary
        return conn
    except ConnectionError:
        print('ERROR: Bad URL of mgmt system')
    except RuntimeError:
        print('ERROR: Bad username or password')
    except:
        print('ERROR: Bad URL of mgmt system')


def check_response(response):
    """
    Checks if the response has an HTTP status code of 2XX and throws a RuntimeError otherwise

    Parameters
    ----------
    response : Response
        A Response object of a preceding HTTP request

    Returns
    -------
    Response
        The Response object of the argument if the response was successful
    """
    if response.ok:
        return response
    else:
        raise RuntimeError(f'{response.status_code} {response.reason} @ {response.url}')


class NodeAuthorizationCookiesMaintainer(Thread):
    def __init__(self, node, period=10):
        """
        Creates a NodeAuthorizationCookiesMaintainer object

        Parameters
        ----------
        node : Node
            The node for which the authorization cookies are updated
        period : int
            The period in seconds after which new authorization cookies are generated

        Returns
        -------
        NodeAuthorizationCookiesMaintainer
            The NodeAuthorizationCookiesMaintainer object that was constructed
        """
        super().__init__()
        self.node = node
        self.period = period

    def run(self):
        """
        Updates the authorization cookies of the node every self.period seconds
        """
        while True:
            self.node.authorization_cookies = check_response(
                self.node.request(post, 'api/auth/login', json=self.node.credentials)).cookies
            sleep(self.period)


class Node:
    def __init__(self, ip, port, username, password):
        """
        Creates a Node object

        Parameters
        ----------
        ip : str
            The IP address of the node
        port : int
            The port of the Local UI on the node
        username : str
            The username of the user in the Local UI
        password : str
            The password of the user in the Local UI

        Returns
        -------
        Node
            The Node object that was constructed
        """
        self.base_url = f'http://{ip}:{port}'
        self.credentials = {'username': username, 'password': password}
        self.authorization_cookies = None
        NodeAuthorizationCookiesMaintainer(self).start()
        while self.authorization_cookies is None:
            sleep(1)

    def request(self, method, url, *arg, **kwargs):
        """
        Makes a request to the local UI

        Parameters
        ----------
        method : func
            The HTTP request function for the HTTP method that should be executed
        url : str
            The part of the URL after self.base_url
        kwargs : dict
            keyword arguments that should be passed to the HTTP method

        Returns
        -------
        Response
            The Response object of the corresponding HTTP request
        """
        if 'cookies' not in kwargs:
            kwargs['cookies'] = self.authorization_cookies
        else:
            kwargs['cookies']['authorization'] = self.authorization_cookies['authorization']
        return method(urljoin(self.base_url, url), *arg, **kwargs)

    def apply_gateway_config(self, config):
        """
        Applies the configuration string in the parameter config to the gateway on the node and restarts the gateway

        Parameters
        ----------
        config : str
            The configuration string of the gateway on the node in JSON format
        """
        self.upload_gateway_config(config)
        self.restart_gateway()

    def upload_gateway_config(self, config):
        """
        Upload the configuration string in the variable config to the gateway configuration on the node

        Parameters
        ----------
        config : str
            The configuration string of the gateway on the node in JSON format

        Returns
        -------
        Response
            The Response object of the corresponding HTTP request if the request was successful
        """
        return check_response(self.request(put, 'dp/api/config', json={'config': loads(config)}))

    def restart_gateway(self):
        """
        Restart the gateway of the node

        Returns
        -------
        Response
            The Response object of the corresponding HTTP request if the request was successful
        """
        return check_response(self.request(get, 'dp/api/restart/gw'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nerve API examples')
    parser.add_argument('url', help="URL of the Nerve Management System")
    parser.add_argument('-u', '--user', metavar='USER', help="User for the Nerve Management System")
    parser.add_argument('-p', '--password', metavar='PWD', help="Password for the Nerve Management System")
    args = parser.parse_args()

    # Get a connection object (actually a requests.Session object)
    conn = get_connection(args.url, args.user, args.password)

    # get list of nodes, ...
    node_list(conn)
