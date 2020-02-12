FROM debian:stable

RUN apt-get update && apt-get install -y devscripts

RUN mkdir -p /tmp/setuptools-scm-git-archive && \
    cd /tmp/setuptools-scm-git-archive && \
    curl -O https://salsa.debian.org/python-team/modules/setuptools-scm-git-archive/-/archive/debian/1.1-1/setuptools-scm-git-archive-debian-1.1-1.tar.gz && \
    tar xf setuptools-scm-git-archive-debian-1.1-1.tar.gz && \
    cd setuptools-scm-git-archive-debian-1.1-1 && \
    apt-get update && ls && \
    mk-build-deps -t "apt-get -o Debug::pkgProblemResolver=yes --no-install-recommends -y" -ir debian/control && \
    dpkg-buildpackage -b -us -uc && \
    dpkg -i ../python3-setuptools-scm-git-archive*.deb

COPY control /tmp/control
RUN apt-get update && mk-build-deps -t "apt-get -o Debug::pkgProblemResolver=yes --no-install-recommends -y" -ir /tmp/control
