#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from nsd import NsdCollector

################################################################################


class TestNsdCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NsdCollector', {})

        self.collector = NsdCollector(config, None)

    def test_import(self):
        self.assertTrue(NsdCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_wtih_real_data(self, publish_mock):
        fixture_data = self.getFixture('nsd_stats').getvalue()
        collector_mock = patch.object(NsdCollector,
                                      'get_nsd_control_output',
                                      Mock(return_value=fixture_data))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'server0.queries': 62942,
            'num.queries': 62942,
            'time.boot': 8505.772053,
            'time.elapsed': 8413.193979,
            'size.db.disk': 589824,
            'size.db.mem': 309488,
            'size.xfrd.mem': 21294248,
            'size.config.disk': 3016,
            'size.config.mem': 19600,
            'num.type.A': 45892,
            'num.type.NS': 342,
            'num.type.MD': 0,
            'num.type.MF': 0,
            'num.type.CNAME': 4,
            'num.type.SOA': 3516,
            'num.type.MB': 0,
            'num.type.MG': 0,
            'num.type.MR': 0,
            'num.type.NULL': 0,
            'num.type.WKS': 0,
            'num.type.PTR': 2409,
            'num.type.HINFO': 0,
            'num.type.MINFO': 0,
            'num.type.MX': 1034,
            'num.type.TXT': 308,
            'num.type.RP': 0,
            'num.type.AFSDB': 0,
            'num.type.X25': 0,
            'num.type.ISDN': 0,
            'num.type.RT': 0,
            'num.type.NSAP': 0,
            'num.type.SIG': 0,
            'num.type.KEY': 0,
            'num.type.PX': 0,
            'num.type.AAAA': 8996,
            'num.type.LOC': 0,
            'num.type.NXT': 0,
            'num.type.SRV': 263,
            'num.type.NAPTR': 0,
            'num.type.KX': 0,
            'num.type.CERT': 0,
            'num.type.TYPE38': 4,
            'num.type.DNAME': 0,
            'num.type.OPT': 0,
            'num.type.APL': 0,
            'num.type.DS': 2,
            'num.type.SSHFP': 0,
            'num.type.IPSECKEY': 0,
            'num.type.RRSIG': 0,
            'num.type.NSEC': 0,
            'num.type.DNSKEY': 0,
            'num.type.DHCID': 0,
            'num.type.NSEC3': 0,
            'num.type.NSEC3PARAM': 0,
            'num.type.TLSA': 0,
            'num.type.SPF': 67,
            'num.type.NID': 0,
            'num.type.L32': 0,
            'num.type.L64': 0,
            'num.type.LP': 0,
            'num.type.TYPE251': 6,
            'num.type.TYPE252': 14,
            'num.type.TYPE255': 85,
            'num.opcode.QUERY': 62942,
            'num.class.IN': 62934,
            'num.class.CH': 8,
            'num.rcode.NOERROR': 55761,
            'num.rcode.FORMERR': 0,
            'num.rcode.SERVFAIL': 5232,
            'num.rcode.NXDOMAIN': 1927,
            'num.rcode.NOTIMP': 0,
            'num.rcode.REFUSED': 1,
            'num.rcode.YXDOMAIN': 0,
            'num.edns': 46223,
            'num.ednserr': 0,
            'num.udp': 62921,
            'num.udp6': 0,
            'num.tcp': 21,
            'num.tcp6': 0,
            'num.answer_wo_aa': 7,
            'num.rxerr': 0,
            'num.txerr': 0,
            'num.raxfr': 6,
            'num.truncated': 0,
            'num.dropped': 0,
            'zone.master': 0,
            'zone.slave': 97,            
            }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        collector_mock = patch.object(NsdCollector,
                                      'get_nsd_control_output',
                                      Mock(return_value=''))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        self.assertPublishedMany(publish_mock, {})


################################################################################
if __name__ == "__main__":
    unittest.main()
