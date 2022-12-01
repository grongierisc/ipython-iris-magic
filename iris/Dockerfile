ARG IMAGE=intersystemsdc/iris-community:preview

FROM $IMAGE

USER root

# Update package and install sudo
RUN apt-get update && apt-get install -y \
	nano \
	python3-pip \
	python3-venv \
	sudo && \
	/bin/echo -e ${ISC_PACKAGE_MGRUSER}\\tALL=\(ALL\)\\tNOPASSWD: ALL >> /etc/sudoers && \
	sudo -u ${ISC_PACKAGE_MGRUSER} sudo echo enabled passwordless sudo-ing for ${ISC_PACKAGE_MGRUSER}

# Back to non-root user
USER ${ISC_PACKAGE_MGRUSER}

# create Python env
ENV PYTHON_PATH=/usr/irissys/bin/irispython
ENV SRC_PATH=/opt/irisapp
ENV IRISUSERNAME "SuperUser"
ENV IRISPASSWORD "SYS"
ENV IRISNAMESPACE "USER"
ENV PATH "/usr/irissys/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/irisowner/bin"

# Copy requirements.txt and install Python packages
COPY requirements.txt /tmp/requirements.txt

# Copy iris.script for use in entrypoint.sh
COPY iris.script /tmp/iris.script

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Requirement for embedded python
RUN pip3 install -r /tmp/requirements.txt

# install embbeded Python kernel
RUN mkdir /home/irisowner/.local/share/jupyter/kernels/irispython
COPY irispython/* /home/irisowner/.local/share/jupyter/kernels/irispython/

ENTRYPOINT [ "/tini", "--", "/entrypoint.sh" ]