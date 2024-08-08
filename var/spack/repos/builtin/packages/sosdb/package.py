# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib
import re

import spack.build_systems.autotools
from spack.package import *

class Sosdb(AutotoolsPackage, GNUMirrorPackage):
    """SOS (pronuounced "sôs") -- Scalable Object Store -- is a high-performance, indexed, object-oriented
     database designed to efficiently manage structured data on persistent media."""

    homepage = "https://github.com/ovis-hpc/sos"
    url = "https://github.com/ovis-hpc/sos/archive/refs/tags/OVIS-4.3.1.tar.gz"
    git = "https://github.com/ovis-hpc/sos.git"

    maintainers("jennfshr", "tomogc")
    
    license("GPLv2 OR BSD")
    version("DEC23", commit="83c8f8462f08cfb238be550b85bb23e4149d35de")
    version("SOS-6", branch="SOS-6")
    version("4.3.1", sha256="1224515749632485651eaf8ae64644ab443ec9cfe743ea7263e2a7e4676dd9b0")
    tags = ["ovis", "database"]
    variant("gssapi", default=False, description="Enable gssapi support")
    variant("jansson", default=False, description="libjansson support")
    variant("authdes", default=False, description="Enable authdes support")
    variant("ipv6", default=False, description="Enable ipv6 support")
    variant("debug", default=False, description="Enable debug support")
    variant("python", default=True, description="Enable python support")
    variant("symvers", default=True, description="Enable symbol versioning")
    variant("doc", default=False, description="Enable doc module")
    variant("doc-html", default=False, description="Enable doc-html module")
    variant("doc-latex", default=False, description="Enable doc-latex module")
    variant("doc-man", default=True, description="Enable doc-man module")
    variant("doc-graph", default=False, description="Enable doc-graph module")
    variant("libtool-lock", default=True, description="Enable locking; disabling may break parallel builds")
    variant("gettext", default=True, description="Use gettext")

    depends_on("autoconf@2.69")
    depends_on("automake")
    depends_on("libtool")
    depends_on("bison")
    depends_on("flex")
    depends_on("krb5", when="+gssapi")
    depends_on("readline")
    depends_on("python@3.9", when="+python")
    depends_on("py-cython@:0.29.36", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("libuuid@1.0.3")
    depends_on("jansson", when="+jansson")
    depends_on("gettext@0.19.8.1")

    executables = ["^dsosd$", "^dsosql$", "^sos-db$", "^sos-schema$", "^sos_cmd$", "^ods_dump$"]
    parallel = False

    def configure_args(self):
        spec = self.spec
        args = []
        # Check for GSS-API
        if "+gssapi" in spec:
            args.append("--enable-gssapi")
            args.append("--with-gssapi=%s" % spec["krb5"].prefix)
            # krbconf = which("krb5-config")
            # ovis-sos_cflags = krbconf("--cflags", "gssapi", output=str)
            # args.append(f"CFLAGS={ovis-sos_cflags}")
            # ovis-sos_libs = krbconf("--libs", "gssapi", output=str)
            # args.append(f"LIBS={ovis-sos_libs}")
        else:
            args.append("--disable-gssapi")
            args.append("--without-gssapi")

        # Authdes support
        if "+authdes" in spec:
            args.append("--enable-authdes")
            args.append("--with-uuid=%s" % spec["libuuid"].prefix)
        else:
            args.append("--disable-authdes")

        # IPV6 support
        if "+ipv6" in spec:
            args.append("--enable-ipv6")
        else:
            args.append("--disable-authdes")

        # Debug support
        if "+debug" in spec:
            args.append("--enable-debug")
        else:
            args.append("--disable-debug")

        # Jansson support
        if "+jansson" in spec:
            args.append("--with-jansson=%s" % spec["jansson"].prefix)
        else:
            args.append("--without-jansson")

        # Python3 support
        if "+python" in spec:
            args.append("--enable-python")
            args.append("--with-python_prefix=%s" % spec["python"].prefix)
            args.append("--with-python-sys-prefix=%s" % spec["python"].prefix)
            site_pkgs = os.path.join(spec["python"].prefix, "lib", "python%s" % spec["python"].version.up_to(2), "site_packages")
            args.append("--with-python_exec_prefix=%s" % site_pkgs)
            python = self.spec["python"].command
            args.append("PYTHON=%s" % python)
            args.append("PYTHON_PREFIX=%s" % spec["python"].prefix)
#            args.append("PYTHON_EXEC_PREFIX=%s" % site_pkgs)
        else:
            args.append("--disable-python")

        # Symvers support
        if "+symvers" in spec:
            args.append("--enable-symvers")
        else:
            args.append("--disable-symvers")

        # Doc support
        if "+doc" in spec:
            args.append("--enable-doc")
        else:
            args.append("--disable-doc")

        if "+doc-html" in spec:
            args.append("--enable-doc-html")
        else:
            args.append("--disable-doc-html")

        if "+doc-latex" in spec:
            args.append("--enable-doc-latex")
        else:
            args.append("--disable-doc-latex")

        if "+doc-man" in spec:
            args.append("--enable-doc-man")
        else:
            args.append("--disable-doc-man")

        if "+doc-graph" in spec:
            args.append("--enable-doc-graph")
        else:
            args.append("--disable-doc-graph")

        # Libtool locking support
        if "+libtool-lock" in spec:
            args.append("--enable-libtool-lock")
        else:
            args.append("--disable-libtool-lock")

        # gettext req't
        if "+gettext" in spec:
            args.append("CFLAGS=-I%s" % spec["gettext"].prefix.include)
            args.append("LDFLAGS=-L%s -lintl" % spec["gettext"].prefix.libs)
        return args


