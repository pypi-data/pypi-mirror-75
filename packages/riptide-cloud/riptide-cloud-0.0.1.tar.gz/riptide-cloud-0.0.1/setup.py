#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'riptide-cloud',
        version = '0.0.1',
        description = 'Riptide Cloud API.',
        long_description = '# Riptide Cloud API\n\n## Installing\n\n`riptide-cloud` is available using pip.\n\n```.env\npip install riptide-cloud\n```\n\n## Introduction\n\nThe APIs provided as part of the `riptide-cloud` package can be used to read\nthe following information.\n\n - `entity` (like `site`, `equipments`, `points`, etc),\n - `alarms` (a.k.a. `alerts`),\n - `history` (past data about any entity),\n - `watch` (list of entities that you are interested in watching), etc.\n\nPlease note that the APIs can only be used to `read` information from the\nRiptide cloud. No `write`/`create` is allowed (except `watch` where you are\nallowed to `create` one-or-more watches to monitor points at the real-time).\n\nThe request and response payload are in `JSON` format. So the `content-type`\nin the header would be `application/json`.\n\n## RiptideCloudApp\n\nCreate a `JSON` file with the following contents:\n\n```json\n{\n  "auth": "Basic",\n  "username": "<username>",\n  "password": "<password>"\n}\n```\n\n`username` and `password` should be a valid username and password provided\nto you for accessing Riptide cloud.\n\nSay you save this file as `riptide.json` and the full path to this file is\n`/tmp/riptide.json`.\n\nCreate an instance of `RiptideCloudApp` with `config_file=/tmp/riptide.json`\n\n```python\nfrom riptide.cloud.app import RiptideCloudApp\n\nrca = RiptideCloudApp(config_file="/tmp/riptide.json")\n```\n\nNOTE: For all interactions with riptide cloud, you will use the\n`RiptideCloudApp` instance `rca`.\n\n\n## Entity\n\nEntity APIs can be invoked as follows:\n\n- `rca.entity.get_entity(uri=<uri>)`\n- `rca.entity.get_entity_tag(uri=<uri>, name=<tag-name>)`\n- `rca.entity.get_entity_tags(uri=<uri>)`\n- `rca.entity.entity_read_override(uri=<uri>)`\n- `rca.entity.entity_read_override_at(uri=<uri>, level=<priority-level>)`\n\n`<uri>` in the above API calls are called as `Riptide Entity URI`. Riptide\nuses `uri` (Uniform Resource Identifier) to represent `site`, `equipments`\nand `points` in the following way.\n\n```.env\n/<customer-name>/<site-name>[/<path-to-equipment>]/<equipment-name>/properties/<property-type>/<property-name>[/presentValue | priorityArray[/<priorityLevel>]]\n```\n\nThe following are some of the examples.\n\n```.env\n/McDonalds/San Bernardino/Weather/properties/AI/Temperature\n```\n\n- `customer-name` is `McDonalds`\n- `site-name` is `San Bernardino`\n- `equipment-name` is `Weather`\n- `property-type` is `AI`\n- `property-name` is `Temperature`\n\n---\n\n```.env\n/McDonalds/San Bernardino/HVAC/Outdoor Unit - 05/properties/AI/Target Condensing Temperature\n```\n\n- `customer-name` is `McDonalds`\n- `site-name` is `San Bernardino`\n- `path-to-equipment` is `HVAC`\n- `equipment-name` is `Outdoor Unit - 05`\n- `property-type` is `AI`\n- `property-name` is `Target Condensing Temperature`\n\n---\n\n```.env\n/McDonalds/San Bernardino/HVAC/Indoor Unit - 11/properties/AO/Set Temperature/priorityArray/10\n```\n\n- `customer-name` is `McDonalds`\n- `site-name` is `San Bernardino`\n- `path-to-equipment` is `HVAC`\n- `equipment-name` is `Indoor Unit - 11`\n- `property-type` is `AO`\n- `property-name` is `Set Temperature`\n- `priority-level` is `10`\n\nThe following are syntactically valid examples.\n\n- `/McDonalds/San Bernardino/HVAC/Indoor Unit - 11/properties/AO/Set Temperature/priorityArray/10`\n- `/McDonalds/San Bernardino/HVAC/Indoor Unit - 11/properties/AO/Set Temperature/priorityArray`\n- `/McDonalds/San Bernardino/HVAC/Indoor Unit - 11/properties/AO/Set Temperature/presentValue`\n- `/McDonalds/San Bernardino/HVAC/Indoor Unit - 11/properties/AO/Set Temperature`\n- `/McDonalds/San Bernardino/HVAC/Indoor Unit - 11`\n- `/McDonalds/San Bernardino/HVAC`\n- `/McDonalds/San Bernardino` *\n- `/McDonalds` *\n\n`* -> NOT RECOMMENDED`\n\nMost of the `entity` APIs takes the entity url as input. The output of these\n APIs varies based on the entity `url`.\n\nFor example:\n\n - `/priorityArray` would give the following output.\n\n```json\n{\'1\': None,\n \'10\': None,\n \'11\': None,\n \'12\': None,\n \'13\': None,\n \'14\': 73,\n \'15\': None,\n \'16\': None,\n \'2\': None,\n \'3\': None,\n \'4\': None,\n \'5\': None,\n \'6\': 73.5,\n \'7\': None,\n \'8\': None,\n \'9\': 75,\n \'relinquish\': None}\n```\n\n - `/presentValue` would give the following output.\n\n```json\n21.3\n```\n\n\n## Alarm\n\nAlarm APIs can be invoked as follows:\n\n- `rca.alarms.get_alarm(alarm_uuid=<alarm_uuid>)`\n- `rca.alarms.get_alarm_history(uuids, context, start, end)`\n\nTo get more help on these APIs, you could type the following in your Python\nterminal.\n\n```python\nhelp(rca.alarms.get_alarm)\nhelp(rca.alarms.get_alarm_history)\n```\n\n## History\n\nRiptide cloud offers the following flavors of historic data.\n\n- `Raw Historic Data` : The value of a point as recorded at the site at\nvarious instances of time.\n\n- `Interpolated Historic Data` : The value of a point as recorded at the site\nat various instances of time and also the estimated or interpolated values\nof the point for the missing periods by using re-sampling technique.\n\n- `Rolled-up Historic Data` : The value of point condensed for a time period\n(e.g. 1 day, 10 days, 1 week and so on).\n\n- `Digested Historic Data` : The value of a point summarized over a period of\nperiod of time (e.g. mean, sum, median and so on). This also allows user\nto apply a function on every value of a point like say add, subtract etc.\n\nHistory APIs can be invoked as follows:\n\n- `rca.history.get_history(identifiers=[uri1, uri2 ... ], start=<datetime>,\nstop=<datetime>)`\n\nFew important points to NOTE:\n- `identifiers` are entity property uri\'s. It must not be site or equipment\nuri\'s but only point uri\'s.\n- Maximum number of `identifiers` that are allowed per API call is 50.\n- `start` and `end` accepts only `datetime` objects; `start` should be\nlesser-than-or-equal-to `end` but must not exceed 31 days.\n\nTo get more help on the above API, you could type the following in your\nPython terminal.\n\n```python\nhelp(rca.history.get_history)\n```\n\n## Watch\n\nYou can create a watch and then interacts with that watch to obtain the\nlatest readings associated with a group of entity properties.\n\nWatch APIs can be invoked as follows:\n\n- `rca.watch.create_watch(identifiers=[uri1, uri2 ... ])`\n- `rca.watch.get_watches()`\n- `rca.watch.poll_watch(watch_id=<watch-id>)`\n- `rca.watch.poll_watch_changed(watch_id=<watch-id>)`\n- `rca.watch.delete_watch(watch_id=<watch-id>)`\n- `rca.watch.read_present_value(identifier=<entity-property-uri>)`\n\nTo get more help on the above API, you could type the following in your\nPython terminal.\n\n```python\nhelp(rca.watch.create_watch)\nhelp(rca.watch.get_watches)\nhelp(rca.watch.poll_watch)\nhelp(rca.watch.poll_watch_changed)\nhelp(rca.watch.delete_watch)\nhelp(rca.watch.read_present_value)\n```\n\n## Support\n\nFor any support, please reach out to `support@riptideio.com`\n\n\n# __END__\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development :: Libraries'
        ],
        keywords = 'riptide alarm entity watch history IoT cloud',

        author = 'Sangeeth Saravanaraj',
        author_email = 'sangeeth@riptideio.com',
        maintainer = 'Sangeeth Saravanaraj',
        maintainer_email = 'sangeeth@riptideio.com',

        license = 'MIT',

        url = '',
        project_urls = {},

        scripts = [],
        packages = [
            'riptide',
            'riptide.cloud'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['requests==2.24.0'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.6',
        obsoletes = [],
    )
