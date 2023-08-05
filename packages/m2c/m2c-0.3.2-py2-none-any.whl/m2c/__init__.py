import os
import sys
import conf
import helper

if sys.argv[-1] == '-v3' or sys.argv[-1] == '-v4':
    conf.M2C_VERSION = sys.argv[-1].strip('-')
    sys.argv = sys.argv[:-1]
else:
    conf.M2C_VERSION = helper.m2c_cliversion()

print 'm2c_version:', helper.m2c_version()
print 'm2c_cliversion:', conf.M2C_VERSION

if os.path.exists('.env'):
    for line in open('.env'):
        items = line.split('=')
        if len(items) < 2:  # hander '=' in value(query string)
            continue
        print 'load env:', items[0], '='.join(items[1:])
        os.environ[items[0].strip()] = '='.join(items[1:]).strip()
