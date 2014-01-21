# coding=utf-8

"""
Collect stats from the NSD

#### Dependencies

    * subprocess
    * collections.defaultdict or kitchen

"""

import subprocess
import diamond.collector

from diamond.collector import str_to_bool


class NsdCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(NsdCollector, self).get_default_config_help()
        config_help.update({
            'bin':          'Path to nsd-control binary',
            'use_sudo':     'Use sudo?',
            'sudo_cmd':     'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NsdCollector, self).get_default_config()
        config.update({
            'path':         'nsd',
            'bin':          '/usr/sbin/nsd-control',
            'use_sudo':     False,
            'sudo_cmd':     '/usr/bin/sudo',
        })
        return config

    def get_nsd_control_output(self):
        try:
            command = [self.config['bin'] + ' stats']

            if str_to_bool(self.config['use_sudo']):
                command.insert(0, self.config['sudo_cmd'])

            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    shell=True).communicate()[0]
        except OSError:
            self.log.exception("Unable to run %s", command)
            return ""

    def collect(self):
        stats_output = self.get_nsd_control_output()

        for line in stats_output.splitlines():
            stat_name, stat_value = line.split('=')

            self.publish(stat_name, stat_value)
