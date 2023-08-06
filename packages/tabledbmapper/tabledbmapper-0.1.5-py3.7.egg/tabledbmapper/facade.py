from tabledbmapper.engine import ConnHandle, ExecuteEngine, TemplateEngine
from tabledbmapper.logger import DefaultLogger, Logger
from tabledbmapper.manager.manager import Manager
from tabledbmapper.manager.mvc.dao import DAO
from tabledbmapper.manager.mvc.service import Service
from tabledbmapper.manager.session.decorators.sql_session import sqlsession
from tabledbmapper.manager.session.pool import SessionPool
from tabledbmapper.manager.session.sql_session import SQLSession
from tabledbmapper.manager.session.sql_session_factory import SQLSessionFactory, SQLSessionFactoryBuild

from tabledbmapper.sql_builder import builder
from tabledbmapper.manager.xml_config import parse_config_from_string, parse_config_from_file


def render_sql_template(template: str, parameter):
    """
    Build SQL string
    :param template: Init template
    :param parameter: Parameter
    :return: render result and parameter
    """
    builder(template, parameter)


def get_config_from_string(xml_string):
    """
    Parsing XML configuration string
    :param xml_string: XML configuration string
    :return: Profile information dictionary
    """
    return parse_config_from_string(xml_string)


def get_config_from_file(file_path):
    """
    Parsing XML configuration file
    :param file_path: Profile path
    :return: Profile information dictionary
    """
    return parse_config_from_file(file_path)
