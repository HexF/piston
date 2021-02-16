# name, version, aliases, dependencies, path
import sys, os

name = sys.argv[1].replace('./','')

file_content = []

file_content.append('name="%s"' % name)
file_content.append('aliases=()')
file_content.append('requires=()')
file_content.append('')

def wrapf(fname, content):
    if len(content.strip()) > 0:
        return ["%s(){" % fname] + ["\t" + l for l in content.split('\n')] + ["}"]
    return ["%s(){}" % fname]

with open('../lxc/util/versions') as f:
    version_code = ''.join(f.readlines()).split(
        "echo '%s'" % name)[1].strip().split('\n'
        )[0][53:-1] + " | grep -Po '\d+.\d+.\d+'"
    file_content += wrapf("version", version_code)


for fname in ['install','pre_uninstall','post_uninstall', 'path','compile']:
    file_content += wrapf(fname, "")



with open(name) as f:
    run_code = ''.join(f.readlines()).replace('#!/bin/bash', '').replace('cd /tmp/$1','')
    file_content += wrapf("run", run_code.strip())


with open(name + ".pld", 'w') as f:
    f.writelines('\n'.join(file_content))


os.rename(name, '../lxc/executors/' + name)