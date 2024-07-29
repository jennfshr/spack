# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import configparser
import spack.build_environment
from spack.package import *
from spack.util.environment import is_system_path

class Ldms(AutotoolsPackage):

    """LDMS is a low-overhead, low-latency framework for collecting, 
    transfering, and storing metric data on a large distributed computer system.
    https://ovis-hpc.readthedocs.io/en/latest/
    """
    homepage = "http://github.com/OVIS-LDMS/ovis.git"
    url = "https://github.com/ovis-hpc/ovis/releases/download/v4.4.3/ovis-ldms-4.4.3.tar.gz"
    maintainers("vlkale", "jennfshr")
    license("GPLv2 OR BSD")
    version("4.4.3", sha256="f34c1ac153e8d00ca3401458dd62f5bc76928cca98a02c627906014ede77031b")
    version("4.4.2", sha256="5d0a5fd1184beadbcba8cfb3070ac1e6efd6cc4795aed65873887b75bfc250b5")
    version("4.3.11", sha256="ef24aae04c08b32a414340e2975a98bd468eb85fdfa76640ba94f73a8945c14a")

    executables = [ 'ldmsd' ]
    provides = [ 'ldms', 'ovis' ]

    variant("array_example", default=False, description="enable array_example module")
    variant("aix-soname", default="aix", description="provide on AIX", values=("aix", "svr4", "both"), multi=False)
    #variant("amqp", default=False, description="enable amqp module")
    #depends_on("amqp", when="+rabbitkw")
    #depends_on("amqp", when="+rabbitv3")
    variant("clock", default=True, description="enable clock module")
    variant("coretemp", default=True, description="enable coretemp module")
    variant("csv", default=True, description="enable csv module")
    #variant("cxi", default=False, description="support for cassini network interface")
    #depends_on("cxi", when="+cxi")
    variant("developer", default=False, description="enable developer module")
    variant("doc", default=False, description="enable doc module")
    variant("doc-html", default=False, description="enable doc-html module")
    variant("doc-latex", default=False, description="enable doc-latex module")
    variant("doc-man", default=True, description="enable doc-man module")
    variant("doc-graph", default=False, description="enable doc-graph module")
    variant("etc", default=False, description="enable etc module")
    variant("fabric", default=False, description="enable fabric module")
    depends_on("libfabric", when="+fabric")
    variant("filesingle", default=False, description="enable filesingle module")
    variant("flatfile", default=True, description="enable flatfile module")
    variant("gpcdlocal", default=False, description="enable gpcdlocal module (Required access to gpcd-support repository)")
    variant("gpumetrics", default=False, description="enable gpumetrics module for Intel OneAPI")
    variant("jobid", default=False, description="enable jobid module")
    variant("kafka", default="check", description"Specify kafka path [default=check]", values=("check", "yes", "no", "PATH", multi=False)
    variant("kgnilnd", default=False, description="enable kgnilnd module")
    variant("ldms-test", default=False, description="enable ldms-test module")
    variant("lnet_stats", default=True, description="enable lnet_stats module")
    variant("lustre", default=True, description="enable lustre module")
    variant("meminfo", default=True, description="enable the meminfo module")
    variant("mmalloc", default=True, description="enable mmalloc module")
    variant("mmap", default=True, description="enable mmap module")
    variant("msr_interlagos", default=False, description="enable msr_interlagos module")
    variant("nola", default=True, description="enable nola module")
    variant("ovis_auth", default=True, description="enable ovis_auth module")
    variant("ovis_ctrl", default=True, description="enable ovis_ctrl module")
    variant("ovis_ev_test", default=False, description="enable ovis_ev_test module")
    variant("ovis_event", default=True, description="enable ovis_event module")
    variant("ovis_event_test", default=False, description="enable ovis_event_test module")
    variant("perf", default=True, description="enable perf module")
    depends_on("pkg-config")
    #variant("rabbitkw", default=False, description="enable rabbitkw module")
    #variant("rabbitv3", default=False, description="enable rabbitv3 module")
    #depends_on("rabbitmq", when="+rabbitkw")
    #depends_on("rabbitmq", when="+rabbitv3")
    variant("rdc", default=False, description="include components that depend on AMD rdc tooling for GPUS")
    depends_on("rdc", when="+rdc")
    variant("rdma", default=True, description="enable rdma module")
    depends_on("rdma-core", when="+rdma")
    variant("rpath", default=True, description="enable rpathing")
    variant("sampler", default=True, description="enable sampler module")
    variant("scripts", default=True, description="enable scripts module")
    variant("slurmtest", default=False, description="enable slurmtest module")
    variant("sock", default=True, description="enable sock module")
    variant("ssl", default=False, description="enable ssl module")
    variant("store", default=True, description="enable store module")
    variant("store-avro-kafka", default=False, description="require store-avro-kafka[default=check]")
    depends_on("librdkafka", when="+store-avro-kafka")
    depends_on("py-avro", when="+store-avro-kafka")
    variant("synthetic", default=True, description="enable synthetic module")
    variant("timescale-store", default=False, description="enable timescaledb store plugin")
    variant("tutorial-store", default=False, description="enable tutorial-store module")
    variant("ugni", default=False, description="enable ugni module")
    variant("yaml", default=True, description="enable yaml module")
    depends_on("libyaml", when="+yaml")
    variant("zap", default=True, description="enable zap module")
    variant("zaptest", default=False, description="enable zaptest module")
    variant("varset", default=True, description="enable varset module")
    variant("hello_stream", default=True, description="enable hello_stream module")
    variant("blob_stream", default=True, description="enable blob_stream module")
    variant("perfevent", default=False, description="enable perfevent module")
    variant("mpi_sampler", default=False, description="enable mpi_sampler module")
    depends_on("mpi", when="+mpi_sampler")
    variant("mpi_noprofile", default=False, description="enable mpi_noprofile module")
    depends_on("mpi", when="+mpi_noprofile")
    variant("procinterrupts", default=True, description="enable procinterrupts module")
    variant("procnet", default=True, description="enable procnet module")
    variant("procnetdev", default=True, description="enable procnetdev module")
    variant("procnfs", default=True, description="enable procnfs module")
    variant("dstat", default=True, description="enable dstat module")
    variant("procstat", default=True, description="enable procstat module")
    variant("llnl-edac", default=True, description="enable llnl-edac module")
    variant("fptrans", default=False, description="enable fptrans module")
    variant("tsampler", default=True, description="enable tsampler module")
    variant("cray_power_sampler", default=True, description="enable cray_power_sampler module")
    with when ("+cray_power_sampler"):
        conflicts("^tsampler", msg="Cray Power Sampler will not build with --disable-tsampler")
    
    variant("loadavg", default=True, description="enable loadavg module")
    variant("vmstat", default=True, description="enable vmstat module")
    variant("procdiskstats", default=True, description="enable procdiskstats module")
    variant("cray_system_sampler", default=False, description="enable cray_system_sampler module")

    ## TODO: understand the "spaceless names" limitation with cray sampling
    variant("spaceless_names", default=True, description="enable spaceless_names module")
    #variant("aries-mmr", default=False, description"enable aries-mmr module")
    #   >>>> Requires   variant("gpcd or --with-aries-libgpcd=libdir,incdir
    #variant("aries_linkstatus", default=False, decription="enable aries_linkstatus module")
    #   >>>> Requires gpcdr to be set up with status metrics
    variant("atasmart", default=False, description="enable atasmart module")
    depends_on("libatasmart", when="+atasmart")
    variant("generic_sampler", default=True, description="enable generic_sampler module")
    variant("switchx", default=False, description="enable switchx module")
    ## This is tricky, as the Spack package "sos" is actually Sandia-OpenSHMEM, and with this we have a naming conflict with the headers, as they both supply a include/sos/sos.h but they're distinct packages
    variant("sos", default=False, description="enable sos module")
    variant("darshan", default=False, description="enable darshan module", when="+sos")
    variant("kokkos", default=False, description="enable kokkos module", when="+sos")
    variant("proc-streams", default=False, description="enable proc-streams module", when="+sos")
    variant("jobinfo-sampler", default=True, description="enable jobinfo-sampler module")
    variant("ibm_occ", default=False, description="enable ibm_occ module")
    variant("appinfo", default=False, description="enable appinfo module")
    variant("app-sampler", default=True, description="enable app-sampler module")
    variant("store-app", default=False, description="enable the store-app module")
    variant("test_sampler", default=False, description="enable test_sampler module")
    variant("list_sampler", default=False, description="enable list_sampler module")
    variant("record_sampler", default=False, description="enable record_sampler module")
    variant("grptest", default=False, description="enable grptest module")
    variant("ipmireader", default=False, description="enable the ipmireader module")
    variant("tutorial-sampler", default=False, description="enable tutorial-sampler module")
    variant("variorum", default=False, description="require components that depend upon libvariorum (and libjansson) [default=check]")
    depends_on("variorum", when="+variorum")
    depends_on("jansson", when="+variorum")
    variant("influx", default=False, description="enable influx module")
    depends_on("curl", when="+influx")
    variant("papi", default=False, description="require components that depend upon libpapi (and libpfm4) [default=check]")
    depends_on("papi", when="+papi")
    depends_on("libpfm4", when="+papi")
    variant("infiniband", default=False, description="require components that depend upon libibmad and libibumad [default=check]")
    ## TODO: determine whether this is satisfied by "rdma-core" or other package
    #depends_on("libibmad", when="+infiniband")
    depends_on("libibumad", when="+infiniband")
    variant("ibnet", default=False, description="require the ibnet plugin [default=check]")
    variant("opa2", default=False, description="require the opa2 plugin [default=check]")
    depends_on("rdma-core", when="+opa2")
    variant("tx2mon", default=False, description="require components that depend upon tx2mon header)")
    ## TODO Figure out these cray-nvidia requirements
    variant("cray-nvidia", default=False, description="enable cray-nvidia module")
    variant("cray-nvidia-inc", default=False, description="enable cray-nvidia-inc module")
    variant("cray-hss-devel", default=False, description="enable cray-hss-devel module")
    variant("munge", default=False, description="enable munge module")
    depends_on("munge", when="+munge")
    variant("readline", default=True, description="enable readline module")
    variant("spank_subscriber", default=True, description="enable spank_subscriber module")
    variant("python", default=True, description="enable LDMS python API")
    depends_on("python@3.6:", when="+python")
    depends_on("py-cython", when="+python")
    variant("ldms-python", default=True, description="enable LDMS python API (deprecated)")
    variant("libgenders", default=False, description="enable libgenders module: requires C++,boost")
    depends_on("boost", when="+libgenders")
    ## gpcdlocal isn't in spack
    #variant("+gpcdlocal", default=False, description="specify gpcdlocal path [default=in build tree]")
    variant("genderssystemd", default=False, description="enable genderssystemd module")
    variant("csv_check", default=False, description="enable the csv_check module:   requires C++,boost")
    depends_on("boost", when="+csv_check")
    #variant("third-plugins=dir1,dir2  Enable the third-plugins extra build directories named.
    ## Slingshot Switch Samplers in v4.4.2+ ??
    variant("zfs", default=False, description="require the zfs related plugins [default=check]")
    depends_on("zfs", when="+zfs")
    variant("pic", default=True, description="try to use only PIC/non-PIC objects [default=use both]")
    #conflicts("^cxi", when="+slingshot", msg="Slingshot Sampler requires cxi")
    variant("geopm", default=False, description="build GEOPM telemetry sampler")
    depends_on("geopm-service", when="+geopm")
    variant("daos", default=False, description="build DAOS telemetry sampler")
    depends_on("daos", when="+daos")
    variant("slurm", default=False, description="support for Slurm jobid and additional information")
    depends_on("slurm", when="+slurm")
    variant("dcgm", default=False, description="support Nvidia DCGM telemetry sampler")
    #depends_on("dcgm", when="+dcgm")
    variant("kafka", default=False, description="supply kafka path")
    variant("shared", default=False, description="shared libs only")
    variant("static", default=False, description="static libs only")
    depends_on("libtool", when="@OVIS-4")
    depends_on("bison", when="@OVIS-4")
    depends_on("flex", when="@OVIS-4")
    depends_on("automake", when="@OVIS-4")
    depends_on("autoconf", when="@OVIS-4")
    with when("@4.4.2:"):
        variant("slingshot", default=False, description="require the slinghost related plugins [default=check]")
        variant("slingshot_switch", default=False, description="require the slinghost on-switch plugins [default=check]")
        #depends_on("cxi", when="+slingshot")

#    @run_before("autoreconf")
#    def autogen(self):
#        if self.spec.satisfies("@OVIS-4"):
#            sh = which("sh")
#            sh("autogen.sh")
#    cflags = []
    #@when("+rdma")
    #spec = self.spec
    #cflags = self.cflags
    #cflags.append("-I%s") % spec["rdma-core"].includes)

    #def setup_build_environment(self, spack_env):
    #    spack_env.set("CFLAGS", " ".join(self.cflags))


    def configure_args(self):
        spec = self.spec
        options = []
        options.extend(self.enable_or_disable("shared"))
        options.extend(self.enable_or_disable("static"))

        if "+amqp" in spec:
        #    options.append("--with-amqp=%s" % spec["amqp"].prefix)
            options.append("--enable-amqp")
        else:
            options.append("--disable-amqp")


        if "+appinfo" in spec:
            options.append("--enable-appinfo")
        else:
            options.append("--disable-appinfo")


        if "+app-sampler" in spec:
            options.append("--enable-app-sampler")
        else:
            options.append("--disable-app-sampler")


        if "+aries_linkstatus" in spec:
            options.append("--enable-aries_linkstatus")
        else:
            options.append("--disable-aries_linkstatus")


        if "+aries-mmr" in spec:
            options.append("--enable-aries-mmr")
        else:
            options.append("--disable-aries-mmr")


        if "+array_example" in spec:
            options.append("--enable-array_example")
        else:
            options.append("--disable-array_example")


        if "+atasmart" in spec:
            options.append("--with-atasmart=%s" % spec["libatasmart"].prefix)

            options.append("--enable-atasmart")
        else:
            options.append("--disable-atasmart")


        if "+blob_stream" in spec:
            options.append("--enable-blob_stream")
        else:
            options.append("--disable-blob_stream")


        if "+clock" in spec:
            options.append("--enable-clock")
        else:
            options.append("--disable-clock")


        if "+coretemp" in spec:
            options.append("--enable-coretemp")
        else:
            options.append("--disable-coretemp")


        if "+cray-hss-devel" in spec:
            options.append("--enable-cray-hss-devel")
        else:
            options.append("--disable-cray-hss-devel")


        if "+cray-nvidia" in spec:
            options.append("--enable-cray-nvidia")
        else:
            options.append("--disable-cray-nvidia")


        if "+cray-nvidia-inc" in spec:
            options.append("--enable-cray-nvidia-inc")
        else:
            options.append("--disable-cray-nvidia-inc")


        if "+cray_power_sampler" in spec:
            options.append("--enable-cray_power_sampler")
        else:
            options.append("--disable-cray_power_sampler")


        if "+cray_system_sampler" in spec:
            options.append("--enable-cray_system_sampler")
        else:
            options.append("--disable-cray_system_sampler")


        if "+csv" in spec:
            options.append("--enable-csv")
        else:
            options.append("--disable-csv")


        if "+csv_check" in spec:
            options.append("--enable-csv_check")
        else:
            options.append("--disable-csv_check")


        #if "+cxi" in spec:
        #    options.append("--with-libcxi-prefix=%s" % spec["cxi"].prefix)
        #else:
        #    options.append("--without-libcxi-prefix")

        if "+daos" in spec:
            options.append("--with-daos=%s" % spec["daos"].prefix)
        else:
            options.append("--without-daos")

        if "+darshan" in spec:
            options.append("--enable-darshan")
        else:
            options.append("--disable-darshan")

        #if "+dcgm" in spec:
        #    options.append("--with-dcgm=%s" % spec["dcgm"].prefix)
        #else:
        #    options.append("--without-dcgm")

        if "+developer" in spec:
            options.append("--enable-developer")
        else:
            options.append("--disable-developer")


        if "+doc" in spec:
            options.append("--enable-doc")
        else:
            options.append("--disable-doc")


        if "+doc-graph" in spec:
            options.append("--enable-doc-graph")
        else:
            options.append("--disable-doc-graph")


        if "+doc-html" in spec:
            options.append("--enable-doc-html")
        else:
            options.append("--disable-doc-html")


        if "+doc-latex" in spec:
            options.append("--enable-doc-latex")
        else:
            options.append("--disable-doc-latex")


        if "+doc-man" in spec:
            options.append("--enable-doc-man")
        else:
            options.append("--disable-doc-man")


        if "+dstat" in spec:
            options.append("--enable-dstat")
        else:
            options.append("--disable-dstat")


        if "+etc" in spec:
            options.append("--enable-etc")
        else:
            options.append("--disable-etc")


        if "+fabric" in spec:
            options.append("--enable-fabric")
            options.append("--with-libfabric=%s" % spec["libfabric"].prefix)
        else:
            options.append("--disable-fabric")


        if "+filesingle" in spec:
            options.append("--enable-filesingle")
        else:
            options.append("--disable-filesingle")


        if "+flatfile" in spec:
            options.append("--enable-flatfile")
        else:
            options.append("--disable-flatfile")


        if "+fptrans" in spec:
            options.append("--enable-fptrans")
        else:
            options.append("--disable-fptrans")


        if "+genderssystemd" in spec:
            options.append("--enable-genderssystemd")
        else:
            options.append("--disable-genderssystemd")


        if "+generic_sampler" in spec:
            options.append("--enable-generic_sampler")
        else:
            options.append("--disable-generic_sampler")

        if "+geopm" in spec:
            options.append("--with-geopm=%s" % spec["geopm-service"].prefix)

        if "+gpcdlocal" in spec:
            options.append("--enable-gpcdlocal")
        else:
            options.append("--disable-gpcdlocal")


        if "+gpumetrics" in spec:
            options.append("--enable-gpumetrics")
        else:
            options.append("--disable-gpumetrics")


        if "+grptest" in spec:
            options.append("--enable-grptest")
        else:
            options.append("--disable-grptest")


        if "+hello_stream" in spec:
            options.append("--enable-hello_stream")
        else:
            options.append("--disable-hello_stream")


        if "+ibm_occ" in spec:
            options.append("--enable-ibm_occ")
        else:
            options.append("--disable-ibm_occ")


        if "+influx" in spec:
            options.append("--enable-influx")
            options.append("--with-curl=%s" % spec["curl"].prefix)
        else:
            options.append("--disable-influx")

        if "+ipmireader" in spec:
            options.append("--enable-ipmireader")
        else:
            options.append("--disable-ipmireader")

        if "+jansson" in spec:
            options.append("--with-libjansson-prefix=%s" % spec["jansson"].prefix)
        else:
            options.append("--without-libjansson-prefix")

        if "+jobid" in spec:
            options.append("--enable-jobid")
        else:
            options.append("--disable-jobid")


        if "+jobinfo-sampler" in spec:
            options.append("--enable-jobinfo-sampler")
        else:
            options.append("--disable-jobinfo-sampler")

        if "+kafka" in spec:
            options.append("--with-kafka=%s" % spec["kafka"].prefix)




        if "+kgnilnd" in spec:
            options.append("--enable-kgnilnd")
        else:
            options.append("--disable-kgnilnd")


        if "+kokkos" in spec:
            options.append("--enable-kokkos")
        else:
            options.append("--disable-kokkos")


        if "+ldms-python" in spec:
            options.append("--enable-ldms-python")
        else:
            options.append("--disable-ldms-python")


        if "+ldms-test" in spec:
            options.append("--enable-ldms-test")
        else:
            options.append("--disable-ldms-test")


        if "+libgenders" in spec:
            options.append("--enable-libgenders")
            options.append("--with-boost=%s" % spec["boost"].prefix)
        else:
            options.append("--disable-libgenders")

        if "+list_sampler" in spec:
            options.append("--enable-list_sampler")
        else:
            options.append("--disable-list_sampler")


        if "+llnl-edac" in spec:
            options.append("--enable-llnl-edac")
        else:
            options.append("--disable-llnl-edac")


        if "+lnet_stats" in spec:
            options.append("--enable-lnet_stats")
        else:
            options.append("--disable-lnet_stats")


        if "+loadavg" in spec:
            options.append("--enable-loadavg")
        else:
            options.append("--disable-loadavg")


        if "+lustre" in spec:
            options.append("--enable-lustre")
        else:
            options.append("--disable-lustre")


        if "+meminfo" in spec:
            options.append("--enable-meminfo")
        else:
            options.append("--disable-meminfo")


        if "+mmalloc" in spec:
            options.append("--enable-mmalloc")
        else:
            options.append("--disable-mmalloc")


        if "+mmap" in spec:
            options.append("--enable-mmap")
        else:
            options.append("--disable-mmap")


        if "+mpi_noprofile" in spec:
            options.append("--enable-mpi_noprofile")
        else:
            options.append("--disable-mpi_noprofile")


        if "+mpi_sampler" in spec:
            options.append("MPICXX=%s" % spec["mpi"].mpicxx)
            options.append("--enable-mpi_sampler")
        else:
            options.append("--disable-mpi_sampler")


        if "+msr_interlagos" in spec:
            options.append("--enable-msr_interlagos")
        else:
            options.append("--disable-msr_interlagos")


        if "+munge" in spec:
            options.append("--enable-munge")
            options.append("--with-munge=%s" % spec["munge"].prefix)
        else:
            options.append("--disable-munge")
            options.append("--without-munge")

        if "+nola" in spec:
            options.append("--enable-nola")
        else:
            options.append("--disable-nola")

        if "+ovis_auth" in spec:
            options.append("--enable-ovis_auth")
            depends_on("openssl")
            options.append("--with-openssl=%s" % spec["openssl"].prefix)
        else:
            options.append("--disable-ovis_auth")


        if "+ovis_ctrl" in spec:
            options.append("--enable-ovis_ctrl")
        else:
            options.append("--disable-ovis_ctrl")


        if "+ovis_event" in spec:
            options.append("--enable-ovis_event")
        else:
            options.append("--disable-ovis_event")


        if "+ovis_event_test" in spec:
            options.append("--enable-ovis_event_test")
        else:
            options.append("--disable-ovis_event_test")


        if "+ovis_ev_test" in spec:
            options.append("--enable-ovis_ev_test")
        else:
            options.append("--disable-ovis_ev_test")

        if "+papi" in spec:
            options.append("--enable-papi")
            options.append("--with-libpapi-prefix=%s" % spec["papi"].prefix)
            options.append("--with-libpfm-prefix=%s" % spec["libpfm4"].prefix)
        else:
            options.append("--disable-papi")
            options.append("--without-libpapi-prefix")
            options.append("--without-libpfm-prefix")

        if "+perf" in spec:
            options.append("--enable-perf")
        else:
            options.append("--disable-perf")

        if "+perfevent" in spec:
            options.append("--enable-perfevent")
        else:
            options.append("--disable-perfevent")

        if "pic" in spec:
            ## TODO
            ## need to understand what PKGS means
            ##   --with-pic[=PKGS]       try to use only PIC/non-PIC objects [default=use
            options.append("--with-pic")
        else:
            options.append("--without-pic")

        if "+procdiskstats" in spec:
            options.append("--enable-procdiskstats")
        else:
            options.append("--disable-procdiskstats")

        if "+procinterrupts" in spec:
            options.append("--enable-procinterrupts")
        else:
            options.append("--disable-procinterrupts")

        if "+procnet" in spec:
            options.append("--enable-procnet")
        else:
            options.append("--disable-procnet")

        if "+procnetdev" in spec:
            options.append("--enable-procnetdev")
        else:
            options.append("--disable-procnetdev")

        if "+procnfs" in spec:
            options.append("--enable-procnfs")
        else:
            options.append("--disable-procnfs")

        if "+procstat" in spec:
            options.append("--enable-procstat")
        else:
            options.append("--disable-procstat")

        if "+proc-streams" in spec:
            options.append("--enable-proc-streams")
        else:
            options.append("--disable-proc-streams")

        if "+python" in spec:
            options.append("--enable-python")
            options.append("--with-python=%s" % spec["python"].prefix)
            options.append("--with-cython=%s" % spec["py-cython"].prefix)
        else:
            options.append("--disable-python")

        if "+rabbitkw" in spec:
            options.append("--enable-rabbitkw")
        else:
            options.append("--disable-rabbitkw")


        if "+rabbitv3" in spec:
            options.append("--enable-rabbitv3")
        else:
            options.append("--disable-rabbitv3")

        if "+rabbitkw" or "+rabbitv3" in spec:
            options.append("--with-rabbitmq=%s" % spec["rabbitmq"].prefix)
            conflict("^amqp", msg="RabbitKW or Rabbitv3 require --with-amqp")

        if "+rdc" in spec:
            options.append("--with-librdc_bootstrap-prefix=%s" % spec["rdc"].prefix)
            options.append("--enable-rdc")
        else:
            options.append("--without-librdc_bootrap")
            options.append("--disable-rdc")


        if "+rdma" in spec:
            options.append("--with-libibverbs=%s" % spec["rdma-core"].prefix)
            options.append("--with-librdmacm=%s" % spec["rdma-core"].prefix)
            options.append("--enable-rdma")
        else:
            options.append("--disable-rdma")


        if "+readline" in spec:
            options.append("--enable-readline")
            options.append("--with-readline=%s" % spec["readline"].prefix)
        else:
            options.append("--disable-readline")

        if "+record_sampler" in spec:
            options.append("--enable-record_sampler")
        else:
            options.append("--disable-record_sampler")


        if "+rpath" in spec:
            options.append("--enable-rpath")
        else:
            options.append("--disable-rpath")


        if "+sampler" in spec:
            options.append("--enable-sampler")
        else:
            options.append("--disable-sampler")


        if "+scripts" in spec:
            options.append("--enable-scripts")
        else:
            options.append("--disable-scripts")

        if "+slurm" in spec:
            options.append("--with-slurm=%s" % spec["slurm"].prefix)
        else:
            options.append("--without-slurm")

        if "+slurmtest" in spec:
            conflict("^slurm", msg="Slurmtest requires Slurm")
            options.append("--enable-slurmtest")
        else:
            options.append("--disable-slurmtest")


        if "+sock" in spec:
            options.append("--enable-sock")
        else:
            options.append("--disable-sock")

        ## ovis-SOS isn't a supported package in Spack, and the sos package isn't what we want
        ## TODO: write an ovis-sos package in Spack
        ##if "+sosdb" in spec:
        ##    options.append("--enable-sos")
        ##    options.append("--with-sos=%s" % spec["ovis-sos"].prefix)
        ##else:
        ##    options.append("--disable-sos")
        ##    options.append("--without-sos")

        if "+tx2mon" in spec:
            options.append("--enable-tx2mon")
            conflicts("target=x86:", msg="Only available for Aarch64")
            conflicts("target=ppc64:", msg="Only available for Aarch64")
            conflicts("target=ppc64le", msg="Only available for Aarch64")
            options.append("--with-tx2mon=%s" % spec["tx2mon"].prefix)
        else:
            options.append("--disable-tx2mon")
            options.append("--without-tx2mon")

        if "+variorum" in spec:
            options.append("--enable-variorum")
            options.append("--enable-sos")
            options.append("--with-libvariorum-prefix=%s" % spec.["variorum"].prefix)
            ## TODO NEED SOS SPACK PACKAGE
            ## options.append("--with-sos=%s" % spec.["sos"].prefix)
        else:
            options.append("--disable-variorum")
            options.append("--without-libvariorum-prefix")

            #if "+slingshot" in spec:
            #    options.append("--with-libcxi=%s" % spec["libcxi"].prefix)

        if "+spaceless_names" in spec:
            options.append("--enable-spaceless_names")
        else:
            options.append("--disable-spaceless_names")

        if "+spank_subscriber" in spec:
            options.append("--enable-spank_subscriber")
        else:
            options.append("--disable-spank_subscriber")

        if "+ssl" in spec:
            options.append("--enable-ssl")
        else:
            options.append("--disable-ssl")

        if "+store" in spec:
            options.append("--enable-store")
        else:
            options.append("--disable-store")

        if "+store-app" in spec:
            options.append("--enable-store-app")
        else:
            options.append("--disable-store-app")

        if "+store-avro-kafka" in spec:
            options.append("--enable-store-avro-kafka")
            options.append("--with-libavro-prefix=%s" % spec["py-avro"].prefix)
            options.append("--with-librdkafka-prefix=%s" % spec["librdkafka"].prefix)
            options.append("--with-serdes=%s" % spec["serdes"].prefix) ### This is not apparently a package in Spack yet
        else:
            options.append("--disable-store-avro-kafka")
            options.append("--without-libavro-prefix")
            options.append("--without-librdkafka-prefix")
            options.append("--without-serdes")

        if "+switchx" in spec:
            options.append("--enable-switchx")
        else:
            options.append("--disable-switchx")

        if "+synthetic" in spec:
            options.append("--enable-synthetic")
        else:
            options.append("--disable-synthetic")

        if "+test_sampler" in spec:
            options.append("--enable-test_sampler")
        else:
            options.append("--disable-test_sampler")

        if "+timescale-store" in spec:
            depends_on("pq")
            options.append("--with-libpq-prefix=%s" % spec["pq"].prefix)
            options.append("--enable-timescale-store")
        else:
            options.append("--disable-timescale-store")

        if "+tsampler" in spec:
            options.append("--enable-tsampler")
        else:
            options.append("--disable-tsampler")

        if "+tutorial-sampler" in spec:
            options.append("--enable-tutorial-sampler")
        else:
            options.append("--disable-tutorial-sampler")

        if "+tutorial-store" in spec:
            options.append("--enable-tutorial-store")
        else:
            options.append("--disable-tutorial-store")

        if "+ugni" in spec:
            depends_on("cray-ugni")
            depends_on("cray-rca")
            options.append("--enable-ugni")
        else:
            options.append("--disable-ugni")

        if "+varset" in spec:
            options.append("--enable-varset")
        else:
            options.append("--disable-varset")

        if "+vmstat" in spec:
            options.append("--enable-vmstat")
        else:
            options.append("--disable-vmstat")

        if "+yaml" in spec:
            options.append("--with-yaml=%s" % spec["libyaml"].prefix)
            options.append("--enable-yaml")
        else:
            options.append("--disable-yaml")

        if "+zap" in spec:
            options.append("--enable-zap")
        else:
            options.append("--disable-zap")

        if "+zaptest" in spec:
            options.append("--enable-zaptest")
        else:
            options.append("--disable-zaptest")

        if "+zfs" in spec:
            options.append("--with-zfs=%s" % spec["zfs"].prefix)

        ## unimplemented, not sure how to do this in Spack
        #--with-LDMSDPORT[=NNN]  self.specify LDMSD runtime default port [default=411]
        ## unimplemented, not sure how to do this in Spack
        #--with-libgenders[=path]

        return options

#    def setup_build_environment(self, spack_env):
#        spack_env.set("CFLAGS", " ".join(self.cflags))

#    def setup_run_environment(self, env):

    @run_after("install")
    def install_pkgconfig(self):
        mkdirp(self.prefix.lib.pkgconfig)

        with open(join_path(self.prefix.lib.pkgconfig, "ldms.pc"), "w") as f:
            f.write("prefix={0}\n".format(self.prefix))
            f.write("exec_prefix=${prefix}\n")
            f.write("libdir={0}\n".format(self.prefix.lib))
            f.write("includedir={0}\n".format(self.prefix.include))
            f.write("\n")
            f.write("Name: LDMS\n")
            f.write(
                "Description: LDMS is a Lightweight Distributed \n"
                "Metric Service.\n"
            )
            f.write("OVIS: {0}\n".format(self.spec.name))
            f.write("Version: {0}\n".format(self.spec.version))
            f.write("Cflags: -I${includedir}\n")
            f.write("Libs: -L${libdir} -llmdb\n")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("OVIS", self.prefix)
        env.set("OVIS_INC", self.prefix.inc)
        env.set("OVIS_LIB", self.prefix.lib)

## TODO https://spack.readthedocs.io/en/latest/packaging_guide.html#making-a-package-discoverable-with-spack-external-find
