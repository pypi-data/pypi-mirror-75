#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re

from neutron_lib.api.definitions import portbindings
from neutron_lib import constants as const
import six

# TODO(lucasagomes): Remove OVN_SG_NAME_EXT_ID_KEY in the Rocky release
OVN_SG_NAME_EXT_ID_KEY = 'neutron:security_group_name'
OVN_SG_EXT_ID_KEY = 'neutron:security_group_id'
OVN_SG_RULE_EXT_ID_KEY = 'neutron:security_group_rule_id'
OVN_ML2_MECH_DRIVER_NAME = 'ovn'
OVN_NETWORK_NAME_EXT_ID_KEY = 'neutron:network_name'
OVN_NETWORK_MTU_EXT_ID_KEY = 'neutron:mtu'
OVN_PORT_NAME_EXT_ID_KEY = 'neutron:port_name'
OVN_PORT_FIP_EXT_ID_KEY = 'neutron:port_fip'
OVN_ROUTER_NAME_EXT_ID_KEY = 'neutron:router_name'
OVN_ROUTER_IS_EXT_GW = 'neutron:is_ext_gw'
OVN_GW_PORT_EXT_ID_KEY = 'neutron:gw_port_id'
OVN_SUBNET_EXT_ID_KEY = 'neutron:subnet_id'
OVN_SUBNET_EXT_IDS_KEY = 'neutron:subnet_ids'
OVN_PHYSNET_EXT_ID_KEY = 'neutron:provnet-physical-network'
OVN_NETTYPE_EXT_ID_KEY = 'neutron:provnet-network-type'
OVN_SEGID_EXT_ID_KEY = 'neutron:provnet-segmentation-id'
OVN_PROJID_EXT_ID_KEY = 'neutron:project_id'
OVN_DEVID_EXT_ID_KEY = 'neutron:device_id'
OVN_CIDRS_EXT_ID_KEY = 'neutron:cidrs'
OVN_FIP_EXT_ID_KEY = 'neutron:fip_id'
OVN_FIP_PORT_EXT_ID_KEY = 'neutron:fip_port_id'
OVN_FIP_EXT_MAC_KEY = 'neutron:fip_external_mac'
OVN_REV_NUM_EXT_ID_KEY = 'neutron:revision_number'
OVN_QOS_POLICY_EXT_ID_KEY = 'neutron:qos_policy_id'
OVN_SG_IDS_EXT_ID_KEY = 'neutron:security_group_ids'
OVN_DEVICE_OWNER_EXT_ID_KEY = 'neutron:device_owner'
OVN_LIVENESS_CHECK_EXT_ID_KEY = 'neutron:liveness_check_at'
OVN_PORT_BINDING_PROFILE = portbindings.PROFILE
OVN_PORT_BINDING_PROFILE_PARAMS = [{'parent_name': six.string_types,
                                    'tag': six.integer_types},
                                   {'vtep-physical-switch': six.string_types,
                                    'vtep-logical-switch': six.string_types}]
MIGRATING_ATTR = 'migrating_to'
OVN_ROUTER_PORT_OPTION_KEYS = ['router-port', 'nat-addresses']
OVN_GATEWAY_CHASSIS_KEY = 'redirect-chassis'
OVN_CHASSIS_REDIRECT = 'chassisredirect'
OVN_GATEWAY_NAT_ADDRESSES_KEY = 'nat-addresses'
OVN_DROP_PORT_GROUP_NAME = 'neutron_pg_drop'

OVN_PROVNET_PORT_NAME_PREFIX = 'provnet-'

# Agent extension constants
OVN_AGENT_DESC_KEY = 'neutron:description'
OVN_AGENT_METADATA_SB_CFG_KEY = 'neutron:ovn-metadata-sb-cfg'
OVN_AGENT_METADATA_DESC_KEY = 'neutron:description-metadata'
OVN_AGENT_METADATA_ID_KEY = 'neutron:ovn-metadata-id'
OVN_CONTROLLER_AGENT = 'OVN Controller agent'
OVN_CONTROLLER_GW_AGENT = 'OVN Controller Gateway agent'
OVN_METADATA_AGENT = 'OVN Metadata agent'

# OVN ACLs have priorities.  The highest priority ACL that matches is the one
# that takes effect.  Our choice of priority numbers is arbitrary, but it
# leaves room above and below the ACLs we create.  We only need two priorities.
# The first is for all the things we allow.  The second is for dropping traffic
# by default.
ACL_PRIORITY_ALLOW = 1002
ACL_PRIORITY_DROP = 1001

ACL_ACTION_DROP = 'drop'
ACL_ACTION_ALLOW_RELATED = 'allow-related'
ACL_ACTION_ALLOW = 'allow'

# When a OVN L3 gateway is created, it needs to be bound to a chassis. In
# case a chassis is not found OVN_GATEWAY_INVALID_CHASSIS will be set in
# the options column of the Logical Router. This value is used to detect
# unhosted router gateways to schedule.
OVN_GATEWAY_INVALID_CHASSIS = 'neutron-ovn-invalid-chassis'

SUPPORTED_DHCP_OPTS = {
    4: ['netmask', 'router', 'dns-server', 'log-server',
        'lpr-server', 'swap-server', 'ip-forward-enable',
        'policy-filter', 'default-ttl', 'mtu', 'router-discovery',
        'router-solicitation', 'arp-timeout', 'ethernet-encap',
        'tcp-ttl', 'tcp-keepalive', 'nis-server', 'ntp-server',
        'tftp-server'],
    6: ['server-id', 'dns-server', 'domain-search']}
DHCPV6_STATELESS_OPT = 'dhcpv6_stateless'

# When setting global DHCP options, these options will be ignored
# as they are required for basic network functions and will be
# set by Neutron.
GLOBAL_DHCP_OPTS_BLACKLIST = {
    4: ['server_id', 'lease_time', 'mtu', 'router', 'server_mac',
        'dns_server', 'classless_static_route'],
    6: ['dhcpv6_stateless', 'dns_server', 'server_id']}

CHASSIS_DATAPATH_NETDEV = 'netdev'
CHASSIS_IFACE_DPDKVHOSTUSER = 'dpdkvhostuser'

OVN_IPV6_ADDRESS_MODES = {
    const.IPV6_SLAAC: const.IPV6_SLAAC,
    const.DHCPV6_STATEFUL: const.DHCPV6_STATEFUL.replace('-', '_'),
    const.DHCPV6_STATELESS: const.DHCPV6_STATELESS.replace('-', '_')
}

DB_MAX_RETRIES = 60
DB_INITIAL_RETRY_INTERVAL = 0.5
DB_MAX_RETRY_INTERVAL = 1

TXN_COMMITTED = 'committed'
INITIAL_REV_NUM = -1

ACL_EXPECTED_COLUMNS_NBDB = (
    'external_ids', 'direction', 'log', 'priority',
    'name', 'action', 'severity', 'match')

# Resource types
TYPE_NETWORKS = 'networks'
TYPE_PORTS = 'ports'
TYPE_SECURITY_GROUP_RULES = 'security_group_rules'
TYPE_ROUTERS = 'routers'
TYPE_ROUTER_PORTS = 'router_ports'
TYPE_SECURITY_GROUPS = 'security_groups'
TYPE_FLOATINGIPS = 'floatingips'
TYPE_SUBNETS = 'subnets'

_TYPES_PRIORITY_ORDER = (
    TYPE_NETWORKS,
    TYPE_SECURITY_GROUPS,
    TYPE_SUBNETS,
    TYPE_ROUTERS,
    TYPE_PORTS,
    TYPE_ROUTER_PORTS,
    TYPE_FLOATINGIPS,
    TYPE_SECURITY_GROUP_RULES)

# The order in which the resources should be created or updated by the
# maintenance task: Root ones first and leafs at the end.
MAINTENANCE_CREATE_UPDATE_TYPE_ORDER = {
    t: n for n, t in enumerate(_TYPES_PRIORITY_ORDER, 1)}

# The order in which the resources should be deleted by the maintenance
# task: Leaf ones first and roots at the end.
MAINTENANCE_DELETE_TYPE_ORDER = {
    t: n for n, t in enumerate(reversed(_TYPES_PRIORITY_ORDER), 1)}

# The addresses field to set in the logical switch port which has a
# peer router port (connecting to the logical router).
DEFAULT_ADDR_FOR_LSP_WITH_PEER = 'router'

# FIP ACTIONS
FIP_ACTION_ASSOCIATE = 'fip_associate'
FIP_ACTION_DISASSOCIATE = 'fip_disassociate'

# Loadbalancer constants
LRP_PREFIX = "lrp-"
RE_PORT_FROM_GWC = re.compile(r'(%s)([\w-]+)_([\w-]+)' % LRP_PREFIX)
LB_VIP_PORT_PREFIX = "ovn-lb-vip-"
LB_EXT_IDS_LS_REFS_KEY = 'ls_refs'
LB_EXT_IDS_LR_REF_KEY = 'lr_ref'
LB_EXT_IDS_POOL_PREFIX = 'pool_'
LB_EXT_IDS_LISTENER_PREFIX = 'listener_'
LB_EXT_IDS_MEMBER_PREFIX = 'member_'
LB_EXT_IDS_VIP_KEY = 'neutron:vip'
LB_EXT_IDS_VIP_FIP_KEY = 'neutron:vip_fip'
LB_EXT_IDS_VIP_PORT_ID_KEY = 'neutron:vip_port_id'

# Maximum chassis count where a gateway port can be hosted
MAX_GW_CHASSIS = 5

UNKNOWN_ADDR = 'unknown'

# TODO(lucasagomes): Create constants for other LSP types
LSP_TYPE_LOCALNET = 'localnet'
LSP_TYPE_VIRTUAL = 'virtual'
LSP_OPTIONS_VIRTUAL_PARENTS_KEY = 'virtual-parents'
LSP_OPTIONS_VIRTUAL_IP_KEY = 'virtual-ip'
