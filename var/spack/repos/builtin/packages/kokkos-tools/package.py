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
    variant("trilinos", default=False, description="Use Kokkos from Trilinos")
    variant("vtune", default=False, description="Enable profiling on VTune proprietary counters")

    variant('serial', default=True, description="enable Serial backend (default)")
    variant('cuda', default=False, description="enable Cuda backend")
    variant('openmp', default=False, description="enable OpenMP backend")
    variant('hip', default=False, description="enable HIP backend")

    depends_on('kokkos+serial', when='~trilinos+serial')
    depends_on('kokkos+cuda_lambda', when='~trilinos+cuda')
    #depends_on('kokkos+cuda', when='~trilinos+cuda')
    depends_on('kokkos+openmp', when='~trilinos+openmp')
    depends_on('kokkos+rocm', when='~trilinos+openmp')

    depends_on('cmake@3.16:', type='build')
    depends_on('kokkos@3.1.00:', when='~trilinos')
    depends_on('trilinos+kokkos@develop', when='+trilinos')
    depends_on('trilinos+openmp', when='+trilinos+openmp')
    conflicts('~serial', when='+trilinos')
    conflicts('+cuda', when='+trilinos')
    depends_on('intel-oneapi-vtune', when='+vtune')
    depends_on('caliper', when='+caliper')
    depends_on("kokkos", when="+testing")
    depends_on('mpi', when='+mpi')
    depends_on('papi@6:', when='+papi')
    depends_on('variorum')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DKokkos_ROOT=%s' % (spec['kokkos'].prefix if '~trilinos' in spec
                                  else spec['trilinos'].prefix),
            '-DARBORX_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
            '-DKokkosTools_ENABLE_APEX=%s' % ('ON' if '+apex' in spec else 'OFF'),
            '-DKokkosTools_ENABLE_CALIPER=%s' % ('ON' if '+caliper' in spec else 'OFF'),
            '-DKokkosTools_ENABLE_EXAMPLES=%s' % ('ON' if '+examples' in spec else 'OFF'),
            '-DKokkosTools_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
            '-DKokkosTools_ENABLE_PAPI=%s' % ('ON' if '+papi' in spec else 'OFF'),
            '-DKokkosTools_ENABLE_SINGLE=%s' % ('ON' if '+single' in spec else 'OFF'),
            '-DKokkosTools_ENABLE_TESTS=%s' % ('ON' if '+tests' in spec else 'OFF')
        ]
        if '+cuda' in spec:
            args.append('-DCMAKE_CXX_COMPILER=%s' % spec["kokkos"].kokkos_cxx)
        return args
