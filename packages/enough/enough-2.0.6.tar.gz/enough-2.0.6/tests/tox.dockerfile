RUN pip install python-openstackclient python-heatclient # this is not necessary to run tests but to cleanup leftovers when tests fail
RUN pip install tox
RUN git init
COPY requirements-dev.txt tox.ini setup.cfg setup.py README.md /opt/
RUN tox --notest
COPY . /opt
COPY tests/clouds.yml /opt/inventory/group_vars/all/clouds.yml
COPY tests/domain.yml /opt/inventory/group_vars/all/domain.yml
RUN cd /opt && git add . && git config user.email "you@example.com" && git config user.name "Your Name" && git commit -a -m 'for tests'
