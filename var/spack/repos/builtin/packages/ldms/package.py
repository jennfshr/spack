# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import spack.build_environment
from spack.package import *
from spack.util.environment import is_system_path

class Ldms(AutotoolsPackage):

    """LDMS Lightweight Distributed Metric Service is 
    a scalable monitoring system designed to run on HPC systems.
    """
    homepage = "http://github.com/OVIS-LDMS/ovis.git"
    url = "https://github.com/ovis-hpc/ovis/releases/download/v4.4.3/ovis-ldms-4.4.3.tar.gz"
    maintainers("vlkale", "jennfshr")
    license("GPLv2 or BSD")
    version("4.4.3", sha256="f34c1ac153e8d00ca3401458dd62f5bc76928cca98a02c627906014ede77031b")
    version("4.4.2", sha256="5d0a5fd1184beadbcba8cfb3070ac1e6efd6cc4795aed65873887b75bfc250b5")
    version("4.3.11", sha256="ef24aae04c08b32a414340e2975a98bd468eb85fdfa76640ba94f73a8945c14a")

    
    depends_on("pkg-config")
    variant("rpath", default=True, description="enable rpathing")
    variant("ovis_event", default=True, description="enable ovis_event module")
    variant("mmalloc", default=True, description="enable mmalloc module")
    variant("ovis_ctrl", default=True, description="enable ovis_ctrl module")
    variant("ovis_auth", default=True, description="enable ovis_auth module")
    variant("zap", default=True, description="enable zap module")
    
    # RDMA 
    variant("rdma", default=True, description="enable rdma module")
    depends_on("rdma-core", when="+rdma")
    variant("nola", default=True, description="enable nola module")
    variant("fabric", default=False, description="enable fabric module")
    depends_on("libfabric", when="+fabric")
    variant("ugni", default=False, description="enable ugni module")
    variant("rdc", default=False, description="include components that depend on AMD rdc tooling for GPUS")
    depends_on("rdc", when="+rdc")
    variant("sock", default=True, description="enable sock module")
    variant("ssl", default=False, description="enable ssl module")
    variant("zaptest", default=False, description="enable zaptest module")
    variant("ovis_event_test", default=False, description="enable ovis_event_test module")
    variant("ovis_ev_test", default=False, description="enable ovis_ev_test module")
    variant("etc", default=False, description="enable etc module")
    variant("scripts", default=True, description="enable scripts module")
    variant("slurmtest", default=False, description="enable slurmtest module")
    variant("developer", default=False, description="enable developer module")
    variant("doc", default=False, description="enable doc module")
    variant("doc-html", default=False, description="enable doc-html module")
    variant("doc-latex", default=False, description="enable doc-latex module")
    variant("doc-man", default=True, description="enable doc-man module")
    variant("doc-graph", default=False, description="enable doc-graph module")
    variant("ldms-test", default=False, description="enable ldms-test module")
    variant("mmap", default=True, description="enable mmap module")
    variant("perf", default=True, description="enable perf module")
    variant("yaml", default=True, description="enable yaml module")
    depends_on("libyaml", when="+yaml")
    variant("store", default=True, description="enable store module")
    variant("flatfile", default=True, description="enable flatfile module")
    variant("csv", default=True, description="enable csv module")
    variant("rabbitkw", default=False, description="enable rabbitkw module")
    variant("rabbitv3", default=False, description="enable rabbitv3 module")
#    variant("amqp", default=False, description="enable amqp module")
    depends_on("rabbitmq", when="+rabbitkw")
    depends_on("rabbitmq", when="+rabbitv3")
#    depends_on("amqp", when="+rabbitkw")
#    depends_on("amqp", when="+rabbitv3")
    variant("tutorial-store", default=False, description="enable tutorial-store module")
    variant("timescale-store", default=False, description="enable timescaledb store plugin")
    variant("gpcdlocal", default=False, description="enable gpcdlocal module (Required access to gpcd-support repository)")
    variant("store-avro-kafka", default=False, description="require store-avro-kafka[default=check]")
    depends_on("librdkafka", when="+store-avro-kafka")
    depends_on("py-avro", when="+store-avro-kafka")
    variant("sampler", default=True, description="enable sampler module")
    variant("kgnilnd", default=False, description="enable kgnilnd module")
    variant("lustre", default=True, description="enable lustre module")
    variant("jobid", default=False, description="enable jobid module")
    variant("clock", default=True, description="enable clock module")
    variant("synthetic", default=True, description="enable synthetic module")
    variant("varset", default=True, description="enable varset module")
    variant("lnet_stats", default=True, description="enable lnet_stats module")
    variant("meminfo", default=True, description="enable the meminfo module")
    variant("gpumetrics", default=False, description="enable gpumetrics module for Intel OneAPI")
    variant("coretemp", default=True, description="enable coretemp module")
    variant("filesingle", default=False, description="enable filesingle module")
    variant("msr_interlagos", default=False, description="enable msr_interlagos module")
    variant("array_example", default=False, description="enable array_example module")
    variant("hello_stream", default=True, description="enable hello_stream module")
    variant("blob_stream", default=True, description="enable blob_stream module")
    variant("perfevent", default=False, description="enable perfevent module")
    variant("mpi_sampler", default=False, description="enable mpi_sampler module")
    depends_on("mpi", when="+mpi_sampler")

    variant("mpi_noprofile", default=False, description="enable mpi_noprofile module")
    variant("procinterrupts", default=True, description="enable procinterrupts module")
    variant("procnet", default=True, description="enable procnet module")
    variant("procnetdev", default=True, description="enable procnetdev module")
    variant("procnfs", default=True, description="enable procnfs module")
    variant("dstat", default=True, description="enable dstat module")
    variant("procstat", default=True, description="enable procstat module")
    variant("llnl-edac", default=True, description="enable llnl-edac module")
    variant("fptrans", default=False, description="enable fptrans module")
    variant("tsampler", default=True, description="enable tsampler module")
    conflicts("^tsampler", msg="Cray Power Sampler will not build with --disable-tsampler")
    variant("cray_power_sampler", default=True, description="enable cray_power_sampler module")
    variant("loadavg", default=True, description="enable loadavg module")
    variant("vmstat", default=True, description="enable vmstat module")
    variant("procdiskstats", default=True, description="enable procdiskstats module")
    variant("cray_system_sampler", default=False, description="enable cray_system_sampler module")
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
    #depends_on("libibmad", when="+infiniband")
    depends_on("libibumad", when="+infiniband")
    variant("ibnet", default=False, description="require the ibnet plugin [default=check]") 
    variant("opa2", default=False, description="require the opa2 plugin [default=check]")
    variant("tx2mon", default=False, description="require components that depend upon tx2mon header)")

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
    #variant("cxi", default=False, description="support for cassini network interface")
    #depends_on("cxi", when="+cxi")
    variant("kafka", default=False, description="supply kafka path")
    ## unimplemented, not sure how to do this in Spack
    #--with-LDMSDPORT[=NNN]  self.specify LDMSD runtime default port [default=411]
    ## unimplemented, not sure how to do this in Spack
    #--with-libgenders[=path]
    depends_on("libtool", when="@OVIS-4")
    depends_on("bison", when="@OVIS-4")
    depends_on("flex", when="@OVIS-4")
    depends_on("automake", when="@OVIS-4")
    depends_on("autoconf", when="@OVIS-4")
    
    @run_before("autoreconf")
    def autogen(self):
        if self.specsatisfies("@OVIS-4"):
            sh = which("sh")
            sh("autogen.sh")

    def configure_args(self):
        options = []
        options.extend(self.enable_or_disable("shared"))
        options.extend(self.enable_or_disable("static"))
        if "+rdma" in self.spec:
            options.append("--with-libibverbs=%s" % self.spec["rdma-core"].prefix)
            options.append("--with-librdmacm=%s" % self.spec["rdma-core"].prefix)

        if "+ovis_auth" in self.spec:
            depends_on("openssl")
            options.append("--with-openssl=%s" % self.spec["openssl"].prefix)

        if "+fabric" in self.spec:
            options.append("--with-libfabric=%s" % self.spec["libfabric"].prefix)

        if "+ugni" in self.spec:
            depends_on("cray-ugni")
            depends_on("cray-rca")
        if "+rdc" in self.spec:
            options.append("--with-librdc_bootstrap-prefix=%s" % self.spec["rdc"].prefix)
        if "+slurmtest" in self.spec:
            conflict("^slurm", msg="Slurmtest requires Slurm")
        if "+yaml" in self.spec:
            options.append("--with-yaml=%s" % self.spec["libyaml"].prefix)

        if "+rabbitkw" or "+rabbitv3" in self.spec:
            options.append("--with-rabbitmq=%s" % self.spec["rabbitmq"].prefix)
            conflict("^amqp", msg="RabbitKW or Rabbitv3 require --with-amqp")
        #if "+amqp" in self.spec:
        #    options.append("--with-amqp=%s" % self.spec["amqp"].prefix)
        if "+timescale-store" in self.spec:
            depends_on("pq")
            options.append("--with-libpq-prefix=%s" % self.spec["pq"].prefix)
        if "+store-avro-kafka" in self.spec:
            options.append("--with-libavro-prefix=%s" % self.spec["py-avro"].prefix)
            options.append("--with-librdkafka-prefix=%s" % self.spec["librdkafka"].prefix)
            options.append("--with-serdes=%s" % self.spec["serdes"].prefix) ### This is not apparently a package in Spack yet
        if "+mpi_sampler" in self.spec:
            options.append("MPICXX=%s" % self.spec["mpi"].mpicxx)

        if "+atasmart" in self.spec:
            options.append("--with-atasmart=%s" % self.spec["libatasmart"].prefix)

        ## ovis-SOS isn't a supported package in Spack, and the sos package isn't what we want
        ## TODO: write an ovis-sos package in Spack
        ##if "+sosdb" in self.spec:
        ##    options.append("--with-sos=%s" % self.spec["ovis-sos"].prefix)
    
        if "+variorum" in self.spec:
            options.append("--with-libvariorum-prefix=%s" % self.spec["variorum"].prefix)
        if "+jansson" in self.spec:
            options.append("--with-libjansson-prefix=%s" % self.spec["jansson"].prefix)
        if "+influx" in self.spec:
            options.append("--with-curl=%s" % self.spec["curl"].prefix)
        if "+papi" in self.spec:
            options.append("--with-libpapi-prefix=%s" % self.spec["papi"].prefix)
            options.append("--with-libpfm4-prefix=%s" % self.spec["libpfm4"].prefix)
        if "+tx2mon" in self.spec:
            conflicts("target=x86:", msg="Only available for Aarch64")
            conflicts("target=ppc64:", msg="Only available for Aarch64")
            conflicts("target=ppc64le", msg="Only available for Aarch64")
            options.append("--with-tx2mon=%s" % self.spec["tx2mon"].prefix)
        if "+munge" in self.spec:
            options.append("--with-munge=%s" % self.spec["munge"].prefix)
        if "+readline" in self.spec:
            options.append("--with-readline=%s" % self.spec["readline"].prefix)
        if "+python" in self.spec:
            options.append("--with-python=%s" % self.spec["python"].prefix)
            options.append("--with-cython=%s" % self.spec["py-cython"].prefix)
    
        if "+libgenders" or "+csv_check" in self.spec:
            options.append("--with-boost=%s" % self.spec["boost"].prefix)
        if self.specsatisfies("@4.4.2:"):
            variant("slingshot", default=False, description="require the slinghost related plugins [default=check]")
            variant("slingshot_switch", default=False, description="require the slinghost on-switch plugins [default=check]")
            #depends_on("cxi", when="+slingshot")
            #if "+slingshot" in self.spec:
            #    options.append("--with-libcxi=%s" % self.spec["libcxi"].prefix)
        
        if "+zfs" in self.spec:
            options.append("--with-zfs=%s" % self.spec["zfs"].prefix)
    
        if self.specsatisfies("^pic"):
           options.append("--without-pic")
    
        if "aix-soname=aix" in self.spec:
           options.append("--with-aix-soname=aix")
        
    
        if "aix-soname=svr4" in self.spec:
           options.append("--with-aix-soname=svr4")
        
        if "aix-soname=both" in self.spec:
            options.append("--with-aix-soname=both")
        
        if "+geopm" in self.spec:
            options.append("--with-geopm=%s" % self.spec["geopm-service"].prefix)
        if "+daos" in self.spec:
            options.append("--with-daos=%s" % self.spec["daos"].prefix)
        if "+slurm" in self.spec:
            options.append("--with-slurm=%s" % self.spec["slurm"].prefix)
        #if "+dcgm" in self.spec:
        #    options.append("--with-dcgm=%s" % self.spec["dcgm"].prefix)
        #if "+cxi" in self.spec:
        #    options.append("--with-cxi-prefix=%s" % self.spec["cxi"].prefix)
        ## gpcdlocal isn't in spack
        #variant("+gpcdlocal", default=False, description="self.specify gpcdlocal path [default=in build tree]")
        if "+kafka" in self.spec:
            options.append("--with-kafka=%s" % self.spec["kafka"].prefix)
    



        return options


