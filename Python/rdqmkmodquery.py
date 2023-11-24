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

import json

from argparse import ArgumentParser

from rdqm.kmod import RdqmKmodData

parser = ArgumentParser()
location_group = parser.add_argument_group('instance_location')
location_group.add_argument("--instance_file", help='A local instance document')
location_group.add_argument("--instance_url", help='the URL of an instance document (the public one will be used by default)')
location_group = parser.add_argument_group('schema_location')
location_group.add_argument("--schema_file", help='A local schema')
location_group.add_argument("--schema_url", help='the URL of a local copy of the schema (the one referenced in the instance document will be used by default)')
parser.add_argument("kernel", help='A full RHEL kernel version')
parser.add_argument("-m", "--mq", help='A full MQ V.R.M.F')
args = parser.parse_args()

data = RdqmKmodData()

if args.schema_url:
    data.loadSchemaURL(args.schema_url)
elif args.schema_file:
    data.loadSchemaFile(args.schema_file)

if args.instance_url:
    data.loadInstanceURL(args.instance_url)
elif args.instance_file:
    data.loadInstanceFile(args.instance_file)
else:
    data.loadInstanceURL("http://ibm.biz/mqRdqmKmodJson")

result = data.query(args.kernel, args.mq)
if result:
    print(json.dumps(result, indent=4))
    