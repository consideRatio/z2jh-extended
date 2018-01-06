# anongid: 1000
# anonuid: 1000
# export_path: /export/pool0/homes
# link_dirname: /data
# link_basename: homes
# mount_path: /mnt/homes
# mount_options: soft,timeo=100,nosuid
# nfs_client_subnet: 10.0.0.0/8
# nfs_server_host: nfsserver
# zfs_dataset: pool0/homes

RUN apt update

# - name: call ansible-playbook from cron
#     cron:
#     name: "ansible-run"
#     minute: "*/20"
#     hour: "*"
#     job: "cd /var/lib/ansible && git pull origin master && ansible-playbook -c local -i localhost, /var/lib/ansible/ansible/playbook.yml >> /var/log/ansible.log"

# - name: install zfsutils-linux
#     apt:
#     name: zfsutils-linux
#     state: installed
#     become: true
RUN apt install -y zfsutils-linux

# - name: check if pool has been created
#     shell: zpool status pool0
#     register: pool0_exists
#     ignore_errors: True
#     become: true
RUN echo 'No need to check if the pool is created afaik'

# - name: create pool0
#     shell: zpool create -f pool0 /dev/sdb
#     when: pool0_exists|failed
#     become: true
RUN zpool create -f pool0 /dev/sdb

# - name: install nfs server packages
#     apt:
#     name: nfs-kernel-server
#     state: installed
#     become: true
RUN apt-get install -y nfs-kernel-server

# - name: add mount path to /etc/exports
#     lineinfile:
#     path: /etc/exports
#     line: "{{ export_path }} {{ nfs_client_subnet }}(rw,sync,no_subtree_check,all_squash,anonuid={{ anonuid }},anongid={{ anongid }})"
#     register: exports_written
#     become: true
# export_path: /export/pool0/homes
# nfs_client_subnet: 10.0.0.0/8
# anonuid: 1000
# anongid: 1000
RUN echo "/export 10.0.0.0/8(rw,sync,no_subtree_check,all_squash,anonuid=1000,anongid=1000)" >> /etc/exports

- name: create zfs filesystem
    zfs:
    name: "{{ zfs_dataset }}"
    state: present
    become: true
# zfs_dataset: pool0/homes

- name: gather zfs facts
    zfs_facts:
    dataset: "{{ zfs_dataset }}"
    type: filesystem
    become: true
# zfs_dataset: pool0/homes

- name: check if zfs dataset is mounted
    fail:
    msg: "{{ zfs_dataset }} not mounted"
    with_items: "{{ ansible_zfs_datasets }}"
    when: item.name == zfs_dataset and item.mounted != "yes"
    become: true
# zfs_dataset: pool0/homes

- name: create mount path directory
    file:
    path: "{{ export_path }}"
    state: directory
    recurse: yes
    become: true
# export_path: /export/pool0/homes

- name: bind mount ZFS on to exported path
    mount:
    name: "{{ export_path}}"
    src: "/{{zfs_dataset}}"
    fstype: none
    opts: rw,bind
    state: mounted
    become: true
# export_path: /export/pool0/homes
# zfs_dataset: pool0/homes

- name: set permissions on exported path
    file:
    path: "{{ export_path }}"
    state: directory
    recurse: no
    owner: "{{ anongid }}"
    group: "{{ anongid }}"
    mode: 0755
    become: true
    RUN chmod /export
# export_path: /export/pool0/homes
# anongid: 1000
# anonuid: 1000

- name: export filesystem
    command: /usr/sbin/exportfs -a
    when: exports_written.changed
    become: true
RUN /usr/sbin/exportfs -a


