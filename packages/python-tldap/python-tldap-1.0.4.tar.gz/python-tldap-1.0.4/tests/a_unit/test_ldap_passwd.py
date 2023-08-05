#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2012-2014 Brian May
#
# This file is part of python-tldap.
#
# python-tldap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-tldap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-tldap  If not, see <http://www.gnu.org/licenses/>.

import unittest
import warnings

import tldap.ldap_passwd as lp

server = None


class PasswordTest(unittest.TestCase):

    def test_password_check_ldap_md5_crypt(self):
        self.assertTrue(lp.check_password(
            "test", "{MD5}CY9rzUYh03PK3k6DJie09g=="))

    def test_password_check_ldap_sha1(self):
        self.assertTrue(lp.check_password(
            "test", "{SHA}qUqP5cyxm6YcTAhz05Hph5gvu9M="))

    def test_password_check_ldap_salted_sha1(self):
        self.assertTrue(lp.check_password(
            "test", "{SSHA}sAloRnCFgBV+SjStZB0lIr8jCCq21to7"))

    def test_password_check_ldap_salted_md5(self):
        self.assertTrue(lp.check_password(
            "test", "{SMD5}xosLPIl3lM7lKx4xeEDPmdpjTig="))

    def test_password_check_md5_crypt(self):
        self.assertTrue(lp.check_password(
            "test", "{CRYPT}$1$U1TmLCl7$MZS59PDJxAE8j9fO/Zs4A0"))
        # some old passwords have crypt in lower case
        self.assertTrue(lp.check_password(
            "test", "{crypt}$1$U1TmLCl7$MZS59PDJxAE8j9fO/Zs4A0"))

    def test_password_check_des_crypt(self):
        self.assertTrue(lp.check_password(
            "test", "{CRYPT}PQl1.p7BcJRuM"))
        # some old passwords have crypt in lower case
        self.assertTrue(lp.check_password(
            "test", "{crypt}PQl1.p7BcJRuM"))

    def test_password_encode(self):
        encrypted = lp.encode_password("test")
        self.assertTrue(encrypted.startswith("{CRYPT}$6$"))
        self.assertTrue(lp.check_password("test", encrypted))
        self.assertFalse(lp.check_password("teddst", encrypted))
