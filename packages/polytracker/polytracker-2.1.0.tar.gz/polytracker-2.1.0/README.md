# PolyTracker

<p align="center">
  <img src="logo/polytracker_name.png?raw=true" width="256" title="PolyTracker">
</p>
<br />

PolyTracker is a tool for the _Automated Lexical Annotation and Navigation of Parsers_, a backronym devised solely for the purpose of referring to it as _The ALAN Parsers Project_. It is a an LLVM pass that instruments the programs it compiles to track which bytes of an input file are operated on by which functions. It outputs a JSON file containing the function-to-input-bytes mapping. Unlike dynamic instrumentation alternatives like [Taintgrind](https://github.com/wmkhoo/taintgrind), PolyTracker imposes negligible performance overhead for almost all inputs, and is capable of tracking every byte of input at once. PolyTracker started as a fork of the LLVM DataFlowSanitizer and takes much inspiration from the [Angora Fuzzer.](https://github.com/AngoraFuzzer/Angora)

PolyTracker can be used in conjunction with [PolyFile](https://github.com/trailofbits/polyfile) to automatically determine the semantic purpose of the functions in a parser.

## Quickstart: Docker

The easiest way to run PolyTracker is via Docker. To build the Docker
container, simply run the following from the root of this repository:
```
docker build -t trailofbits/polytracker . 
```

This will create a Docker container with PolyTracker built, and the `CC` environment variable set to `polybuild`. Simply add the code to be instrumented to this container, and as long as its build process honors the `CC` environment variable, the resulting binary will be instrumented.

For a demo of PolyTracker running on the [MuPDF](https://mupdf.com/) parser run this command:
```
docker build -t trailofbits/polytracker-demo -f examples/pdf/Dockerfile-mupdf.demo .
```

`Mutool_track` will be build in `/polytracker/the_klondike/mupdf/build/debug`. Running `mutool_track` will output `polytracker.json` which contains the information provided by the taint analysis. Its reccomended to use this json with [PolyFile](https://www.github.com/trailofbits/PolyFile). 

For a demo of PolyTracker running on Poppler utils version 0.84.0 run this command: 

```
docker build -t trailofbits/polytracker-demo -f examples/pdf/Dockerfile-poppler.demo .
```

All the poppler utils will be located in `/polytracker/the_klondike/poppler-0.84.0/build/utils`. 

```
cd /polytracker/the_klondike/poppler-0.84.0/build/utils
POLYPATH=some_pdf.pdf ./pdfinfo_track some_pdf.pdf
```

## Quickstart: Instrumenting a simple C/C++ program 

First build the base docker image 
```
docker build -t trailofbits/polytracker .
``` 

Next, enter the docker image and mount your target as a volume 
```
docker run --rm -it -v /path/to/your/target:/workdir trailofbits/polytracker:latest /bin/bash
```

If you have a C target, you can instrument it by invoking the C compiler and passing the `--instrument-target` before your cflags 
```
${CC} --instrument-target -g -o my_target my_target.c 
```

Repeat the same steps above for a cxx file by invoking `${CXX}` instead of `${CC}`

## Dependencies and Prerequisites

PolyTracker has only been tested on x86\_64 Linux. (Notably, the [DataFlow Sanitizer](https://clang.llvm.org/docs/DataFlowSanitizer.html) that PolyTracker builds upon _does not_ work on macOS.)

PolyTracker depends on [gllvm](https://github.com/SRI-CSL/gllvm) to create whole program bitcode archives and to extract bitcode from targets. 

PolyTracker depends on python3.7+ 

The following tools and libraries are required to run PolyTracker:
* LLVM version 7 or 7.1; other later versions may work but have not been tested. The builds in the official Ubuntu Bionic repository appear to be broken; we suggest building LLVM from source or installing it from the official LLVM repositories

## Building PolyTracker from Source 

The following tools are required to build PolyTracker:
* [CMake](https://cmake.org)
* [Ninja](https://ninja-build.org) (`ninja-build` on Ubuntu)
* Python 3.7 and `pip`, for testing purposes (`apt-get -y install python3.7 python3-pip`)

First, make sure that the LLVM 7 binaries have priority in your `PATH`, _e.g._,
```
export PATH="/usr/lib/llvm-7/bin:${PATH}"
```
Next, from the root directory of this repository, run
```
mkdir build && cd build
cmake -G Ninja -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ .. && ninja install
```

This builds and installs two compilers: `polybuild` and
`polybuild++`. These are wrappers around `gclang` and `gclang++`,
respectively, and will add the PolyTracker instrumentation.

## Instrumenting a Program with PolyTracker

All that is required is to modify the program's build system to use `polybuild`/`polybuild++` instead of its default compiler. The easiest way to do this is to set the compiler environment variables to them:
```
export CC=`which polybuild`
export CXX=`which polybuild++`
```

For example, let's work through how to build MuPDF with PolyTracker instrumentation:

```
git clone --recursive git://git.ghostscript.com/mupdf.git
cd mupdf
git submodule update --init
make -j10 HAVE_X11=no HAVE_GLUT=no prefix=./bin install
``` 

Or if you would like to build the debug version, as we do in our Dockerfile:

```
make -j10 HAVE_X11=no HAVE_GLUT=no prefix=./bin debug
```

Then, find the build util you want to instrument, run gllvm's `get-bc` to extract the bitcode from the target, then instrument it with polybuild
```
get-bc -b target
${CC}/{CXX} --instrument-bitcode target.bc -o target_track --libs <any libs go here> 
```

If you aren't sure about what libraries you might need to link for a complex target, the enviornment variable `WLLVM_ARTIFACT_STORE` sets a directory that contains a mainfest that logs all build commands and artifacts used. You should be able to rebuild the target completely using information in the mantifest and the artifacts. 


## Environment Variables 

PolyTracker accepts configuration paramters in the form of environment variables to avoid recompiling target programs. The current environment variables PolyTracker supports is: 

```
POLYPATH: The path to the file to mark as tainted 

POLYTTL: This value is an initial "strength" value for taint nodes, when new nodes are formed, the average is taken. When the TTL value is 0, the node is considered clean. 

POLYSTART: Start offset to track 

POLYEND: End offset to track

POLYOUTPUT: Provides a a path/prefix to output polytracker information too

WLLVM_ARTIFACT_STORE: Provides a path to an exisiting directory to store artifact/manifest for all build targets
```

## Running an Instrumented Program

The PolyTracker instrumentation looks for the `POLYPATH` environment variable to specify which input file's bytes are meant to be tracked. (Note: PolyTracker can in fact track multiple input files—and really any file-like stream such as network sockets—however, we have thus far only exposed the capability to specify a single file. This will be improved in a future release.)

The instrumented software will write its output to `polytracker_process_sets.json` and 
`polytracker_forest.bin` in the current directory.

For example, with our instrumented version of MuPDF, run
```
POLYPATH=input.pdf POLYTTL=32 ./mutool_track info input.pdf
```
On program exit, those artifacts will be created in the current directory.
These are intended to be consumed by PolyProcess to produce a final `polytracker.json` file,
but can be consumed by other tools. The artifacts are documented [here.](docs/ARTIFACTS.md)

To create the final JSON, run `polyprocess` 
```
polyprocess --json path/to/polytracker_process_set.json --forest path/to/polytracker_forest.bin
```

By default this produces a polytracker.json file, which can then be given to PolyFile. 

## Creating custom ignore lists from pre-built libraries 

Attempting to build large software projects can be time consuming, especially older/unsupported ones.
It's even more time consuming to try and modify the build system such that it supports changes, like dfsan's/our instrumentation.

There is a script located in `polytracker/scripts` that you can run on any ELF library and it will output a list of functions to ignore.
We use this when we do not want to track information going through a specific library like libpng, or other sub components of a program. The `Dockerfile-listgen.demo` exists to build common open source libraries so we can create these lists. 
 
This script is a slightly tweaked version of what DataFlowSanitizer has, which focuses on ignoring system libraries. The original script can be found in `dfsan_rt`. 

## Current Status and Known Issues

Taints will not propagate through dynamically loaded libraries unless
those libraries were compiled from source using PolyTracker, _or_
there is specific support for the library calls implemented in
PolyTracker. There _is_ currently support for propagating taint
throught the majority of uninstrumented C standard library calls. 
To be clear, programs that use uninstrumented functions will still run normally,
however, operations performed by unsupported library calls will not
propagate taint. We are currently working on adding robust support for
C++ programs, but currently the best results will be from C programs.

Snapshotting is currently deprecated and not supported in the latest version. 

If there are issues with Docker please do a system prune and build with --no-cache for both PolyTracker 
and whatever demo you are trying to run. 

The worst case performance of PolyTracker is exercised when a single
byte in memory is simultaneously tainted by a large number of input
bytes from the source file. This is most common when instrumenting
compression and cryptographic algorithms that have large block
sizes. There are a number of mitigations for this behavior currently
being researched and developed.

## License and Acknowledgements

This research was developed by [Trail of
Bits](https://www.trailofbits.com/) with funding from the Defense
Advanced Research Projects Agency (DARPA) under the SafeDocs program
as a subcontractor to [Galois](https://galois.com). It is licensed
under the [Apache 2.0 lisense](LICENSE). © 2019, Trail of Bits.

## Maintainers
[Carson Harmon](https://github.com/notBD)<br />
[Evan Sultanik](https://github.com/ESultanik)<br />
[Brad Larsen](https://github.com/bradlarsen)<br />
<br />
`firstname.lastname@trailofbits.com`
