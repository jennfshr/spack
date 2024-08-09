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
    conflicts("%clang@:16")
    conflicts("%gcc@:9")
    
    # Example requires KokkosTools built with monolothic library interface
    conflicts("~single", when="+examples")
    

    variant("apex", default=False, description="Enable building Apex library")
    variant("caliper", default=False, description="Enable building Caliper library")
    variant("examples", default=False, description="Build examples")
    variant("tests", default=False, description="Build tests")
    variant("reuse-kokkos-compiler", default=False,
            description="Enable reuse of compiler and flags based on Kokkos settings")
    variant("mpi", default=False, description="Enable MPI support")
    variant("papi", default=False, description="Enable PAPI support")
    variant("single", default=False,
            description="Build Monolithic KokkosTools library with profilers")
    variant("variorum", default=False, description="Enable Variorum")
    variant("vtune", default=False,
            description="Enable profiling on VTune proprietary counters")
    variant("nvtx", default=False, description="Nvidia profiling")
    variant("roctx", default=False, description="Rocm profiling")
    depends_on("cmake@3.16:", type="build", when="kokkos-tools@develop")
    depends_on("intel-oneapi-vtune", when="+vtune", type=("build", "link", "run"))
    depends_on("caliper", when="+caliper", type=("build", "link", "run"))
    depends_on("kokkos@4:", when="+tests", type=("build", "link", "run"))
    depends_on("kokkos@4:", when="+examples", type=("build", "link", "run"))
    depends_on("kokkos@4:+cuda", when="+nvtx", type=("build", "link", "run"))
    depends_on("kokkos@4:+rocm", when="+roctx", type=("build", "link", "run"))
    depends_on("mpi", when="+mpi", type=("build", "link", "run"))
    depends_on("papi@6:", when="+papi", type=("build", "link", "run"))
    depends_on("variorum", when="+variorum", type=("build", "link", "run"))

    def setup_build_environment(self, env):
        # nvtx requires $Kokkos_ENABLE_CUDA to be set
        if "+nvtx" in self.spec:
            env.set("Kokkos_ENABLE_CUDA", "1")

        # roctx requires $Kokkos_ENABLE_HIP to be set
        if "+roctx" in self.spec:
            env.set("Kokkos_ENABLE_HIP", "1")

        # vtune requires VTUNE_HOME to be set
        if "+vtune" in self.spec:
            env.set("VTUNE_HOME", self.spec["vtune"].prefix)

    def cmake_args(self):
        spec = self.spec
        # Kokkos with relevant variants required for nvtx and roctx
        for con,var in ["nvtx", "+cuda"], ["roctx", "+rocm"]:
#        ns = f"^kokkos@4:{var}"
            if not spec.satisfies(f"^kokkos{var}"):
                conflicts(f"+{con}", msg=f"{con} requires ^kokkos{var}")

        cmake_args = [
            "-DKokkosTools_ENABLE_PAPI=%s" % ("ON" if "+papi" in spec else "OFF"),
            "-DKokkosTools_ENABLE_MPI=%s" % ("ON" if "+mpi" in spec else "OFF"),
            "-DKokkosTools_ENABLE_CALIPER=%s" % ("ON" if "+caliper" in spec else "OFF"),
            "-DKokkosTools_ENABLE_APEX=%s" % ("ON" if "+apex" in spec else "OFF"),
            "-DKokkosTools_ENABLE_EXAMPLES=%s" % ("ON" if "+examples" in spec else "OFF"),
            "-DKokkosTools_ENABLE_TESTS=%s" % ("ON" if "+tests" in spec else "OFF"),
            "-DKokkosTools_ENABLE_SINGLE=%s" % ("ON" if "+single" in spec else "OFF")
        ]

        if "+reuse-kokkos-compiler" in spec:
            cmake_args.append("-DKokkosTools_REUSE_KOKKOS_COMPILER=%s" % "ON")
        else:
            cmake_args.append("-DKokkosTools_REUSE_KOKKOS_COMPILER=%s" % "OFF")

        if "+tests" or "+caliper" or "+examples" or "+nvtx" or "+roctx" or "+vtune" in spec:
            try:
                cmake_args.append("-DKokkos_ROOT=%s" % spec["kokkos"].prefix)
            except:
                print("Kokkos_ROOT not defined due to kokkos not being in spec")

        if (
            spec.satisfies("+nvtx")
            and "^kokkos+cuda" in spec
            and not "^kokkos%clang+cuda" in spec
            or "^kokkos%cce+cuda"
        ):
            try:
                cmake_args.append("-DCMAKE_CXX_COMPILER=%s" %
                                   spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            except:
                print("kokkos-nvcc-wrapper not in spec")
        elif (
            "+nvtx" in spec
            and "^kokkos+cuda"
            and "^kokkos%clang+cuda"
        ):
            try:
                cmake_args.append("-DCMAKE_CXX_COMPILER=%s" % "{0}/bin/clang++".format(spec["clang"].prefix))
            except:
                print("clang not in spec")
        elif "+nvtx" in spec and "^kokkos%cce+cuda":
            try:
                cmake_args.append("-DCMAKE_CXX_COMPILER=%s" % "{0}/bin/CC".format(spec["cce"].prefix))
            except:
                print("cce not in spec")
        elif "+roctx" in spec and "^kokkos+rocm":
            try:
                cmake_args.append("-DCMAKE_CXX_COMPILER=%s" % spec["hip"].hipcc)
            except:
                print("hip not in spec")

        print("Debugging Cmake Args: %s", cmake_args)
        return cmake_args
