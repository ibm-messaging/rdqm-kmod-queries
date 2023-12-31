# rdqm-kmod-queries

In addition to the [IBM Support Document on RDQM kernel modules](https://www.ibm.com/support/pages/ibm-mq-replicated-data-queue-manager-kernel-modules) there is now a [JSON document](https://ibm.biz/mqRdqmKmodJson) and [associated schema](https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/messaging/mqadv/ibm-mq-rdqm-kmods.schema.v1-0.json) that provides the most recent information about the validated combinations of:
1. IBM MQ version
2. Red Hat Enterprise Linux (RHEL) Kernel version
3. DRBD kernel module version

You can find more information on this JSON document, and some other enhancements to the tools and information to help manage the RDQM (DRBD) kernel modules [here](https://community.ibm.com/community/user/integration/blogs/alex-chatt/2023/12/15/rdqm-kernel-module-administration-improvements).

This repository contains sample code showing how to query the JSON document. The initial code is [Python](Python/README.md).

## Contributing

If you are interested in contributing to this repository, please read the [document on contributing](CONTRIBUTING.md).

## Issue Tracking

There is no formal product support for the code in this repository. If you encounter an issue,
or wish to suggest an enhancement, please create an issue in this repository.