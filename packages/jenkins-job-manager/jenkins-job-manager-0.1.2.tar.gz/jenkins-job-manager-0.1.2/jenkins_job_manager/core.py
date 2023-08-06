from jenkins_job_manager.connect_config import JenkinsConnectConfig
from jenkins_job_manager.xml_change import (
    XmlChange,
    XmlChangeDefaultDict,
    CREATE,
    UPDATE,
    DELETE,
)

import itertools
import logging
import os
import re
import random
import string
import xml.dom.minidom
import xml.etree.ElementTree
from typing import Dict, Optional

import jenkins
import jenkins_jobs.modules.base
import jinja2
from jenkins_jobs.parser import YamlParser
from jenkins_jobs.registry import ModuleRegistry
from jenkins_jobs.xml_config import XmlJob, XmlJobGenerator, XmlViewGenerator


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("jjm")

