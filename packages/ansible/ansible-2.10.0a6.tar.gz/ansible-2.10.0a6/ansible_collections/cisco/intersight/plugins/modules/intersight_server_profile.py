#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: intersight_server_profile
short_description: Server Profile configuration for Cisco Intersight
description:
  - Server Profile configuration for Cisco Intersight.
  - Used to configure Server Profiles with assigned servers and server policies.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    choices: [present, absent]
    default: present
  organization:
    description:
      - The name of the Organization this resource is assigned to.
      - Profiles and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    default: default
  name:
    description:
      - The name assigned to the Server Profile.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    required: true
  target_platform:
    description:
      - The platform for which the server profile is applicable.
      - Can either be a server that is operating in Standalone mode or which is attached to a Fabric Interconnect (FIAttached) managed by Intersight.
    choices: [Standalone, FIAttached]
    default: Standalone
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
  descrption:
    description:
      - The user-defined description of the Server Profile.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
  assigned_server:
    description:
      - Managed Obect ID (MOID) of assigned server.
      - Option can be omitted if user wishes to assign server later.
  imc_access_policy:
    description:
      - Name of IMC Access Policy to associate with this profile.
  local_user_policy:
    description:
      - Name of Local User Policy to associate with this profile.
author:
  - David Soper (@dsoper2)
version_added: '2.10'
'''

EXAMPLES = r'''
- name: Configure Server Profile
  intersight_server_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: SP-Server1
    target_platform: FIAttached
    tags:
      - Key: Site
        Value: SJC02
    description: Profile for Server1
    assigned_server: 5e3b517d6176752d319a9999
    imc_access_policy: sjc02-d23-access
    local_user_policy: guest-admin

- name: Delete Server Profile
  intersight_server_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: SP-Server1
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "AssignedServer": {
            "Moid": "5e3b517d6176752d319a0881",
            "ObjectType": "compute.Blade",
        },
        "Name": "SP-IMM-6454-D23-1-1",
        "ObjectType": "server.Profile",
        "Tags": [
            {
                "Key": "Site",
                "Value": "SJC02"
            }
        ],
        "TargetPlatform": "FIAttached",
        "Type": "instance"
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec, compare_values


def post_profile_to_policy(intersight, moid, resource_path, policy_name):
    options = {
        'http_method': 'get',
        'resource_path': resource_path,
        'query_params': {
            '$filter': "Name eq '" + policy_name + "'",
        },
    }
    response = intersight.call_api(**options)
    if response.get('Results'):
        # get expected policy moid from 1st list element
        expected_policy_moid = response['Results'][0]['Moid']
        actual_policy_moid = ''
        # check any current profiles and delete if needed
        options = {
            'http_method': 'get',
            'resource_path': resource_path,
            'query_params': {
                '$filter': "Profiles/any(t: t/Moid eq '" + moid + "')",
            },
        }
        response = intersight.call_api(**options)
        if response.get('Results'):
            # get actual moid from 1st list element
            actual_policy_moid = response['Results'][0]['Moid']
            if actual_policy_moid != expected_policy_moid:
                if not intersight.module.check_mode:
                    # delete the actual policy
                    options = {
                        'http_method': 'delete',
                        'resource_path': resource_path + '/' + actual_policy_moid + '/Profiles',
                        'moid': moid,
                    }
                    intersight.call_api(**options)
                actual_policy_moid = ''
        if not actual_policy_moid:
            if not intersight.module.check_mode:
                # post profile to the expected policy
                options = {
                    'http_method': 'post',
                    'resource_path': resource_path + '/' + expected_policy_moid + '/Profiles',
                    'body': [
                        {
                            'ObjectType': 'server.Profile',
                            'Moid': moid,
                        }
                    ]
                }
                intersight.call_api(**options)
            intersight.result['changed'] = True


def main():
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        target_platform=dict(type='str', choices=['Standalone', 'FIAttached'], default='Standalone'),
        tags=dict(type='list', default=[]),
        description=dict(type='str', aliases=['descr'], default=''),
        assigned_server=dict(type='str', default=''),
        imc_access_policy=dict(type='str'),
        local_user_policy=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # get assigned server information
    intersight.get_resource(
        resource_path='/compute/PhysicalSummaries',
        query_params={
            '$filter': "Moid eq '" + intersight.module.params['assigned_server'] + "'",
        }
    )
    source_object_type = None
    if intersight.result['api_response'].get('SourceObjectType'):
        source_object_type = intersight.result['api_response']['SourceObjectType']

    # get the current state of the resource
    intersight.result['api_response'] = {}
    intersight.get_resource(
        resource_path='/server/Profiles',
        query_params={
            '$filter': "Name eq '" + intersight.module.params['name'] + "'",
            '$expand': 'Organization',
        }
    )

    # create api_body for comparison with actual state
    intersight.api_body = {
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
        'AssignedServer': {
            'Moid': intersight.module.params['assigned_server'],
            'ObjectType': source_object_type,
        },
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
    }
    if intersight.module.params['target_platform'] == 'FIAttached':
        intersight.api_body['TargetPlatform'] = intersight.module.params['target_platform']

    moid = None
    resource_values_match = False
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        moid = intersight.result['api_response']['Moid']
        if module.params['state'] == 'present':
            resource_values_match = compare_values(intersight.api_body, intersight.result['api_response'])
        else:  # state == 'absent'
            intersight.delete_resource(
                moid=moid,
                resource_path='/server/Profiles',
            )
            moid = None

    if module.params['state'] == 'present' and not resource_values_match:
        # remove read-only Organization key
        intersight.api_body.pop('Organization')
        if not moid:
            # GET Organization Moid
            intersight.get_resource(
                resource_path='/organization/Organizations',
                query_params={
                    '$filter': "Name eq '" + intersight.module.params['organization'] + "'",
                    '$select': 'Moid',
                },
            )
            organization_moid = None
            if intersight.result['api_response'].get('Moid'):
                # resource exists and moid was returned
                organization_moid = intersight.result['api_response']['Moid']
            # Organization must be set, but can't be changed after initial POST
            intersight.api_body['Organization'] = {
                'Moid': organization_moid,
            }
        intersight.configure_resource(
            moid=moid,
            resource_path='/server/Profiles',
            body=intersight.api_body,
            query_params={
                '$filter': "Name eq '" + intersight.module.params['name'] + "'",
            }
        )
        if intersight.result['api_response'].get('Moid'):
            # resource exists and moid was returned
            moid = intersight.result['api_response']['Moid']

    if moid and intersight.module.params['imc_access_policy']:
        post_profile_to_policy(intersight, moid, resource_path='/access/Policies', policy_name=intersight.module.params['imc_access_policy'])

    if moid and intersight.module.params['local_user_policy']:
        post_profile_to_policy(intersight, moid, resource_path='/iam/EndPointUserPolicies', policy_name=intersight.module.params['local_user_policy'])

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
