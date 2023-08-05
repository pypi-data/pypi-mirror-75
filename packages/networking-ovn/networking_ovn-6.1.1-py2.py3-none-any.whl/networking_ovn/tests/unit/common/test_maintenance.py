# Copyright 2017 Red Hat, Inc.
# All Rights Reserved.
#
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

import mock

from futurist import periodics
from neutron.tests.unit.plugins.ml2 import test_security_group as test_sg
from neutron_lib.db import api as db_api

from networking_ovn.common import config as ovn_config
from networking_ovn.common import constants
from networking_ovn.common import maintenance
from networking_ovn.common import utils
from networking_ovn.db import maintenance as db_maint
from networking_ovn.db import revision as db_rev
from networking_ovn import ovn_db_sync
from networking_ovn.tests.unit.db import base as db_base


@mock.patch.object(maintenance.DBInconsistenciesPeriodics,
                   'has_lock', mock.PropertyMock(return_value=True))
class TestDBInconsistenciesPeriodics(db_base.DBTestCase,
                                     test_sg.Ml2SecurityGroupsTestCase):

    def setUp(self):
        super(TestDBInconsistenciesPeriodics, self).setUp()
        self.net = self._make_network(
            self.fmt, name='net1', admin_state_up=True)['network']
        self.port = self._make_port(
            self.fmt, self.net['id'], name='port1')['port']
        self.fake_ovn_client = mock.Mock()
        self.periodic = maintenance.DBInconsistenciesPeriodics(
            self.fake_ovn_client)
        self.session = db_api.get_writer_session()

    @mock.patch.object(maintenance.DBInconsistenciesPeriodics,
                       '_fix_create_update')
    @mock.patch.object(db_maint, 'get_inconsistent_resources')
    def test_check_for_inconsistencies(self, mock_get_incon_res, mock_fix_net):
        fake_row = mock.Mock(resource_type=constants.TYPE_NETWORKS)
        mock_get_incon_res.return_value = [fake_row, ]
        self.periodic.check_for_inconsistencies()
        mock_fix_net.assert_called_once_with(fake_row)

    def _test_migrate_to_port_groups_helper(self, pg_supported, a_sets,
                                            migration_expected, never_again):
        self.fake_ovn_client._nb_idl.is_port_groups_supported.return_value = (
            pg_supported)
        self.fake_ovn_client._nb_idl.get_address_sets.return_value = a_sets
        with mock.patch.object(ovn_db_sync.OvnNbSynchronizer,
                               'migrate_to_port_groups') as mtpg:
            if never_again:
                self.assertRaises(periodics.NeverAgain,
                                  self.periodic.migrate_to_port_groups)
            else:
                self.periodic.migrate_to_port_groups()

            if migration_expected:
                mtpg.assert_called_once()
            else:
                mtpg.assert_not_called()

    def test_migrate_to_port_groups_port_groups_not_supported(self):
        self._test_migrate_to_port_groups_helper(pg_supported=False,
                                                 a_sets=None,
                                                 migration_expected=False,
                                                 never_again=True)

    def test_migrate_to_port_groups_not_needed(self):
        self._test_migrate_to_port_groups_helper(pg_supported=True,
                                                 a_sets=None,
                                                 migration_expected=False,
                                                 never_again=True)

    def test_migrate_to_port_groups(self):
        # Check normal migration path: if port groups are supported by the
        # schema and the migration has to be done, it will take place and
        # won't be attempted in the future.
        self._test_migrate_to_port_groups_helper(pg_supported=True,
                                                 a_sets=['as1', 'as2'],
                                                 migration_expected=True,
                                                 never_again=True)

    def test_migrate_to_port_groups_no_lock(self):
        with mock.patch.object(maintenance.DBInconsistenciesPeriodics,
                               'has_lock', mock.PropertyMock(
                                   return_value=False)):
            # Check that if this worker doesn't have the lock, it won't
            # perform the migration and it will try again later.
            self._test_migrate_to_port_groups_helper(pg_supported=True,
                                                     a_sets=['as1', 'as2'],
                                                     migration_expected=False,
                                                     never_again=False)

    def _test_fix_create_update_network(self, ovn_rev, neutron_rev):
        self.net['revision_number'] = neutron_rev

        # Create an entry to the revision_numbers table and assert the
        # initial revision_number for our test object is the expected
        db_rev.create_initial_revision(
            self.net['id'], constants.TYPE_NETWORKS, self.session,
            revision_number=ovn_rev)
        row = db_rev.get_revision_row(self.net['id'])
        self.assertEqual(ovn_rev, row.revision_number)

        if ovn_rev < 0:
            self.fake_ovn_client._nb_idl.get_lswitch.return_value = None
        else:
            fake_ls = mock.Mock(external_ids={
                constants.OVN_REV_NUM_EXT_ID_KEY: ovn_rev})
            self.fake_ovn_client._nb_idl.get_lswitch.return_value = fake_ls

        self.fake_ovn_client._plugin.get_network.return_value = self.net
        self.periodic._fix_create_update(row)

        # Since the revision number was < 0, make sure create_network()
        # is invoked with the latest version of the object in the neutron
        # database
        if ovn_rev < 0:
            self.fake_ovn_client.create_network.assert_called_once_with(
                self.net)
        # If the revision number is > 0 it means that the object already
        # exist and we just need to update to match the latest in the
        # neutron database so, update_network() should be called.
        else:
            self.fake_ovn_client.update_network.assert_called_once_with(
                self.net)

    def test_fix_network_create(self):
        self._test_fix_create_update_network(ovn_rev=-1, neutron_rev=2)

    def test_fix_network_update(self):
        self._test_fix_create_update_network(ovn_rev=5, neutron_rev=7)

    def _test_fix_create_update_port(self, ovn_rev, neutron_rev):
        self.port['revision_number'] = neutron_rev

        # Create an entry to the revision_numbers table and assert the
        # initial revision_number for our test object is the expected
        db_rev.create_initial_revision(
            self.port['id'], constants.TYPE_PORTS, self.session,
            revision_number=ovn_rev)
        row = db_rev.get_revision_row(self.port['id'])
        self.assertEqual(ovn_rev, row.revision_number)

        if ovn_rev < 0:
            self.fake_ovn_client._nb_idl.get_lswitch_port.return_value = None
        else:
            fake_lsp = mock.Mock(external_ids={
                constants.OVN_REV_NUM_EXT_ID_KEY: ovn_rev})
            self.fake_ovn_client._nb_idl.get_lswitch_port.return_value = (
                fake_lsp)

        self.fake_ovn_client._plugin.get_port.return_value = self.port
        self.periodic._fix_create_update(row)

        # Since the revision number was < 0, make sure create_port()
        # is invoked with the latest version of the object in the neutron
        # database
        if ovn_rev < 0:
            self.fake_ovn_client.create_port.assert_called_once_with(
                self.port)
        # If the revision number is > 0 it means that the object already
        # exist and we just need to update to match the latest in the
        # neutron database so, update_port() should be called.
        else:
            self.fake_ovn_client.update_port.assert_called_once_with(
                self.port)

    def test_fix_port_create(self):
        self._test_fix_create_update_port(ovn_rev=-1, neutron_rev=2)

    def test_fix_port_update(self):
        self._test_fix_create_update_port(ovn_rev=5, neutron_rev=7)

    @mock.patch.object(db_rev, 'bump_revision')
    def _test_fix_security_group_create(self, mock_bump, revision_number):
        sg_name = utils.ovn_addrset_name('fake_id', 'ip4')
        sg = self._make_security_group(self.fmt, sg_name, '')['security_group']

        db_rev.create_initial_revision(
            sg['id'], constants.TYPE_SECURITY_GROUPS, self.session,
            revision_number=revision_number)
        row = db_rev.get_revision_row(sg['id'])
        self.assertEqual(revision_number, row.revision_number)

        if revision_number < 0:
            self.fake_ovn_client._nb_idl.get_address_set.return_value = None
            self.fake_ovn_client._nb_idl.get_port_group.return_value = None
        else:
            self.fake_ovn_client._nb_idl.get_address_set.return_value = (
                mock.sentinel.AddressSet)

        self.fake_ovn_client._plugin.get_security_group.return_value = sg
        self.periodic._fix_create_update(row)

        if revision_number < 0:
            self.fake_ovn_client.create_security_group.assert_called_once_with(
                sg)
        else:
            # If the object already exist let's make sure we just bump
            # the revision number in the ovn_revision_numbers table
            self.assertFalse(self.fake_ovn_client.create_security_group.called)
            mock_bump.assert_called_once_with(
                sg, constants.TYPE_SECURITY_GROUPS)

    def test_fix_security_group_create_doesnt_exist(self):
        self._test_fix_security_group_create(revision_number=-1)

    def test_fix_security_group_create_version_mismatch(self):
        self._test_fix_security_group_create(revision_number=2)

    def test__create_lrouter_port(self):
        port = {'id': 'port-id',
                'device_id': 'router-id'}
        self.periodic._create_lrouter_port(port)
        l3_mock = self.periodic._ovn_client._l3_plugin
        l3_mock.add_router_interface.assert_called_once_with(
            mock.ANY, port['device_id'], {'port_id': port['id']},
            may_exist=True)

    @mock.patch.object(maintenance.LOG, 'debug')
    def test__log_maintenance_inconsistencies(self, mock_log):
        ovn_config.cfg.CONF.set_override('debug', True)

        # Create fake inconsistencies: 2 networks, 4 subnets and 8 ports
        incst = []
        incst += [mock.Mock(resource_type=constants.TYPE_NETWORKS)] * 2
        incst += [mock.Mock(resource_type=constants.TYPE_SUBNETS)] * 4
        incst += [mock.Mock(resource_type=constants.TYPE_PORTS)] * 8

        # Create fake inconsistencies for delete: 3 routers and 6 router ports
        incst_del = []
        incst_del += [mock.Mock(resource_type=constants.TYPE_ROUTERS)] * 3
        incst_del += [mock.Mock(resource_type=constants.TYPE_ROUTER_PORTS)] * 6

        self.periodic._log_maintenance_inconsistencies(incst, incst_del)

        # Assert LOG.debug was called twice
        self.assertEqual(2, len(mock_log.call_args_list))

        # Assert the log matches the number of inconsistencies
        fail_str_create_update = mock_log.call_args_list[0][0][1]['fail_str']
        self.assertIn('networks=2', fail_str_create_update)
        self.assertIn('subnets=4', fail_str_create_update)
        self.assertIn('ports=8', fail_str_create_update)

        fail_str_delete = mock_log.call_args_list[1][0][1]['fail_str']
        self.assertIn('routers=3', fail_str_delete)
        self.assertIn('router_ports=6', fail_str_delete)

    @mock.patch.object(maintenance.LOG, 'debug')
    def test__log_maintenance_inconsistencies_debug_disabled(self, mock_log):
        ovn_config.cfg.CONF.set_override('debug', False)

        incst = [mock.Mock(resource_type=constants.TYPE_NETWORKS)] * 2
        self.periodic._log_maintenance_inconsistencies(incst, [])
        self.assertFalse(mock_log.called)
