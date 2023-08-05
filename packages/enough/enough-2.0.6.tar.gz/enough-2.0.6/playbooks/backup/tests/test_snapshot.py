testinfra_hosts = ['ansible://bind-host']


def openstack(host, cmd):
    cmd = host.run(f"""
    . /usr/lib/backup/openrc.sh
    openstack {cmd}
    """)
    print(cmd.stderr)
    assert 0 == cmd.rc
    return cmd.stdout


def expected_snapshots(host, count):
    assert count == openstack(
        host, "volume snapshot list -f value -c Name | grep -c pet-volume").strip()


def test_snapshots(host):
    with host.sudo():
        cmd = host.run("/etc/cron.daily/snapshot")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc

        expected_snapshots(host, '1')
        cmd = host.run("/etc/cron.daily/snapshot 0")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc

        assert openstack(host, "snapshot list -f value -c Name") == ""
