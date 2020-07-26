FROM    centos:7.2
MAINTAINER      Fisher "fisher@sudops.com"


RUN     /bin/echo 'root:123456' |chpasswd
RUN     useradd work
RUN     /bin/echo 'work:123456' |chpasswd
RUN     /bin/echo -e "LANG=\"en_US.UTF-8\"" >/etc/default/local
EXPOSE  22
EXPOSE  80
CMD     /usr/sbin/sshd -D
