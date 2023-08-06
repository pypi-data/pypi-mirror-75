# -*- coding: utf-8 -*-
'''
diacamma.syndic tests package

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2018 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals

from lucterios.framework.test import add_user, LucteriosTest
from lucterios.CORE.views import get_wizard_step_list, Configuration
from lucterios.contacts.models import Individual


class ProTest(LucteriosTest):

    def setUp(self):
        LucteriosTest.setUp(self)
        Individual.objects.create(genre=1, firstname='Joe', lastname='Dalton', user=add_user('joe'))

    def test_status(self):
        self.calljson('/CORE/authentification', {'username': 'admin', 'password': 'admin'})
        self.assert_observer('core.auth', 'CORE', 'authentification')
        self.assert_json_equal('', '', 'OK')

        self.calljson('/CORE/statusMenu', {}, 'get')
        self.assert_observer('core.custom', 'CORE', 'statusMenu')
        self.assert_count_equal('', 16)

    def test_wizard(self):
        self.calljson('/CORE/authentification', {'username': 'admin', 'password': 'admin'})
        self.assert_observer('core.auth', 'CORE', 'authentification')
        self.assert_json_equal('', '', 'OK')

        steplist = get_wizard_step_list()
        self.assertEqual(15, len(steplist.split(';')), steplist)

    def test_situation(self):
        self.calljson('/CORE/authentification', {'username': 'joe', 'password': 'joe'})
        self.assert_observer('core.auth', 'CORE', 'authentification')
        self.assert_json_equal('', '', 'OK')

        self.calljson('/CORE/situationMenu', {}, 'get')
        self.assert_observer('core.custom', 'CORE', 'situationMenu')
        self.assert_count_equal('', 5)

    def test_config(self):
        self.factory.xfer = Configuration()
        self.calljson('/CORE/configuration', {}, False)
        self.assert_observer('core.custom', 'CORE', 'configuration')
        self.assert_count_equal('', 7 + 6 + 3)
        self.assert_action_equal('POST', self.json_comp["05@Adresses et Contacts_btn"]['action'],
                                 ("Modifier", 'images/edit.png', 'CORE', 'paramEdit', 0, 1, 1, {'params': ['contacts-mailtoconfig', 'contacts-createaccount', 'contacts-defaultgroup', 'contacts-size-page']}))
        self.assert_action_equal('POST', self.json_comp["60@Gestion documentaire_btn"]['action'],
                                 ("Modifier", 'images/edit.png', 'CORE', 'paramEdit', 0, 1, 1, {'params': ["documents-signature"]}))
