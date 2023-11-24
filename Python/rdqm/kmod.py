#
# Copyright 2023 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict

import io
import json
from jsonschema import validate, ValidationError
import urllib.request
import logging

class RdqmKmodData:
    instance = None
    schema = None

    # Swap the following lines to enable debug logging.
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logging.basicConfig(format='%(levelname)s: %(message)s')


    @classmethod
    def validate_instance_data(self):
        if self.instance:
            # Validate the file if possible
            if self.schema is None:
                # We have not been told about a schema, so try and load one from the instance document.
                if "$schema" in self.instance:
                    schema_in_instance_document = self.instance["$schema"]
                    self.loadSchemaURL(schema_in_instance_document)
            if self.schema is not None:
                logging.debug("About to attempt schema validation")
                try:
                    validate(instance=self.instance, schema=self.schema)
                    logging.debug("Validation successful")
                except ValidationError as ve:
                    logging.error("Validation of instance data failed with the message %s", ve.message)
                    self.instance = None


    @classmethod
    def loadInstanceFile(self, instanceFile):
        try:
            instance_json_data = open(instanceFile)
            try:
                self.instance = json.load(instance_json_data)
                self.validate_instance_data()
                try:
                    instance_json_data.close()
                except IOError:
                    logging.warning("Failed to close file %s", instanceFile)
            except json.decoder.JSONDecodeError:
                logging.error("Failed to load instance from %s", instanceFile)
        except OSError:
            logging.error("Could not open file %s", instanceFile)

    @classmethod
    def loadInstanceURL(self, instanceURL):
        try:
            response = urllib.request.urlopen(instanceURL)
            try:
                self.instance = json.loads(response.read())
                self.validate_instance_data()
            except json.decoder.JSONDecodeError:
                logging.error("Failed to load instance from %s", instanceURL)
        except urllib.error.URLError:
            logging.error("urllib.request.urlopen(%s) returned urllib.error.URLError", instanceURL)
        except urllib.error.HTTPError:
            logging.error("urllib.request.urlopen(%s) returned urllib.error.HTTPError", instanceURL)

    @classmethod
    def loadSchemaFile(self, schemaFile):
        try:
            schema_json_data = open(schemaFile)
            try:
                self.schema = json.load(schema_json_data)
                try:
                    schema_json_data.close()
                except IOError:
                    logging.warning("Failed to close schema file %s", schemaFile)
            except json.decoder.JSONDecodeError:
                logging.warning("Failed to load schema from %s", schemaFile)
        except OSError:
            logging.warning("Could not open schema file %s", schemaFile)

    @classmethod
    def loadSchemaURL(self, schemaURL):
        try:
            response = urllib.request.urlopen(schemaURL)
            try:
                self.schema = json.loads(response.read())
            except json.decoder.JSONDecodeError:
                logging.warning("Failed to load schema from %s", schemaURL)
        except urllib.error.URLError:
            logging.warning("urllib.request.urlopen(%s) returned urllib.error.URLError", schemaURL)
        except urllib.error.HTTPError:
            logging.warning("urllib.request.urlopen(%s) returned urllib.error.HTTPError", schemaURL)

    @classmethod
    def is_vrmf_in_range(self, mqVRMF, minVRMF, testedVRMF):
        response = False

        mq_components = mqVRMF.split(".")
        mq_V = int(mq_components[0])
        mq_R = int(mq_components[1])
        mq_M = int(mq_components[2])
        mq_F = int(mq_components[3])

        min_components = minVRMF.split(".")
        min_V = int(min_components[0])
        min_R = int(min_components[1])
        min_M = int(min_components[2])
        min_F = int(min_components[3])

        tested_components = testedVRMF.split(".")
        tested_V = int(tested_components[0])
        tested_R = int(tested_components[1])
        tested_M = int(tested_components[2])
        tested_F = int(tested_components[3])

        if mq_V == min_V and mq_V == tested_V:
            if mq_R == min_R and mq_R == tested_R:
                if mq_M >= min_M and mq_M <= tested_M:
                    if mq_F >= min_F and mq_F <= tested_F:
                        response = True

        return response
    
    @classmethod
    def matching_key(self, kernelVersion, mqVRMF):
        response = ""

        if "kernelLevels" in self.instance:
            kernel_levels = self.instance["kernelLevels"]
            if kernelVersion in kernel_levels:
                kernel_level = kernel_levels[kernelVersion]
                if "compatibleMqVRMs" in kernel_level:
                    compatible_entries = kernel_level["compatibleMqVRMs"]
                    for k,v in compatible_entries.items():
                        if "minVrmf" in v:
                            minVRMF = v["minVrmf"]
                            if "testedVrmf" in v:
                                testedVRMF = v["testedVrmf"]
                        if self.is_vrmf_in_range(mqVRMF, minVRMF, testedVRMF):
                            response = k

        return response
        
    def query(self, kernelVersion, mqVRMF=None):
        result = {}
        if not self.instance:
            logging.debug("Attempting to load instance data from public URL")
            self.instance = self.loadInstanceURL("http://ibm.biz/mqRdqmKmodJson")
        if self.instance:
            result["kernelVersion"] = kernelVersion
            if "kernelLevels" in self.instance:
                if kernelVersion in self.instance["kernelLevels"]:
                    kernelVersionData = self.instance["kernelLevels"][kernelVersion]
                    if "status" in kernelVersionData:
                        kernelStatus = kernelVersionData["status"]
                        result["status"] = kernelStatus
                    if mqVRMF:
                        matching_key = self.matching_key(kernelVersion, mqVRMF)
                        if matching_key:
                            matching_entry = kernelVersionData["compatibleMqVRMs"][matching_key]
                            result["minVrmf"] = matching_entry["minVrmf"]
                            result["testedVrmf"] = matching_entry["testedVrmf"]
                            result["drbdKmod"] = matching_entry["drbdKmod"]
                        else:
                            if kernelStatus == "Under test":
                                result["note"] = "Current state of testing suggests MQ VRMF is not compatible with RHEL kernel."
                            else:
                                result["note"] = "MQ VRMF is not compatible with RHEL kernel"
                    else:
                        if kernelStatus == "Incompatible":
                            # No point looking for compatibleMqVRMs
                            result["note"] = "kernel version is incompatible with all tested MQ VRMs"
                        else:
                            if "compatibleMqVRMs" in kernelVersionData:
                                compatible_MQ_VRMs = kernelVersionData["compatibleMqVRMs"]
                                result["compatibleMqVRMs"] = compatible_MQ_VRMs
                        if "comments" in kernelVersionData:
                            if kernelVersionData["comments"] != "":
                                result["comments"] = kernelVersionData["comments"]
                else:
                    result["note"] = "kernelVersion has not yet been tested"
            else:
                result["note"] = "Missing kernelLevels dictionary"

        return result
    