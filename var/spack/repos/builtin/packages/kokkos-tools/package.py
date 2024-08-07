# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class KokkosTools(CMakePackage):
    """Kokkos Profiling and Debugging Tools"""

    homepage = "https://github.com/kokkos/kokkos-tools/"
    git = "https://github.com/kokkos/kokkos-tools.git"

    license("Apache-2.0 WITH LLVM-exception")
    maintainers("vkale", "jennfshr", "rbbgerber", "dalg24")
    version("develop", branch="develop")

    # C++17 standard support requires sufficiently new compilers
    conflicts('%clang@:16')
    conflicts('%gcc@:9')

    variant("apex", default=False, description="Enable APEX support")
    variant("caliper", default=False, description="Enable Caliper support")
    variant("examples", default=False, description="Enable examples")
    variant("mpi", default=False, description="Enable MPI support")
    variant("papi", default=False, description="Enable PAPI support")
    variant("reuse-compiler", default=False,
            description="Enable reuse of compiler and flags based on Kokkos settings")
    variant("single", default=False, description="Build Monolithic KokkosTools library with profilers")
    variant("testing", default=False, description="Enable Testing")
    variant("variorum", default=False, description="Enable Variorum")
    variant("vtune", default=False, description="Enable profiling on VTune proprietary counters")
    variant("nvtx", default=False, description="Nvidia profiling")
    variant("roctx", default=False, description="Rocm profiling")
    depends_on('cmake@3.16:', type='build', when="kokkos-tools@develop")
    depends_on('intel-oneapi-vtune', when='+vtune', type=("build", "link", "run"))
    depends_on('caliper', when='+caliper', type=("build", "link", "run"))
    depends_on("kokkos@4:", when="+testing", type=("build", "link", "run"))
    depends_on("kokkos@4:", when="+examples", type=("build", "link", "run"))
    depends_on("kokkos@4:+cuda", when="+nvtx", type=("build", "link", "run"))
    depends_on("kokkos@4:+rocm", when="+roctx", type=("build", "link", "run"))
    depends_on('mpi', when='+mpi', type=("build", "link", "run"))
    depends_on('papi@6:', when='+papi', type=("build", "link", "run"))
    depends_on('variorum', when='+variorum" type=("build", "link", "run"))

def build_env(self):
    if '+nvtx' in spec:
        setenv Kokkos_ENABLE_CUDA=1

    if '+rocm' in spec:
        setenv Kokkos_ENABLE_HIP=1

    #if '+vtune' in spec:
    #    setenv VTUNE_HOME spec['intel-oneapi-vtune'].prefix
    #    ## Maybe leave this out?

def cmake_args(self):
    spec = self.spec
    args = [
        '-DKokkosTools_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
        '-DKokkosTools_ENABLE_APEX=%s' % ('ON' if '+apex' in spec else 'OFF'),
        '-DKokkosTools_ENABLE_CALIPER=%s' % ('ON' if '+caliper' in spec else 'OFF'),
        '-DKokkosTools_ENABLE_EXAMPLES=%s' % ('ON' if '+examples' in spec else 'OFF'),
        '-DKokkosTools_ENABLE_PAPI=%s' % ('ON' if '+papi' in spec else 'OFF'),
        '-DKokkosTools_ENABLE_SINGLE=%s' % ('ON' if '+single' in spec else 'OFF'),
        '-DKokkosTools_ENABLE_TESTS=%s' % ('ON' if '+tests' in spec else 'OFF')
    ]

    if '+testing' or '+caliper' or '+examples' or '+nvtx' or '+roctx' or '+vtune' in spec:
        args.append('-DKokkos_ROOT=%s' % spec['kokkos'].prefix)

    if '+cuda' in spec:
        args.append('-DCMAKE_CXX_COMPILER=%s' % spec['kokkos'].kokkos_cxx)

    return args
