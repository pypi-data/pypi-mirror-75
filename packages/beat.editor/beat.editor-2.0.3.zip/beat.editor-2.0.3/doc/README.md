# beat.editor

A local editor for BEAT objects, including a graphical toolchain editor. It aims
to compliment `beat.cmdline` to enable a productive and smooth workflow for
developing objects for the BEAT platform as well as replace the current
toolchain editor in `beat.web`.

## Installation
#### System Requirements
- Up-to-date version of [conda](https://conda.io/miniconda.html)
- Idiap conda channel configured: ::

    $ conda config --env --add channels https://www.idiap.ch/software/beat/conda

To install, just run `conda install beat.editor`.


### Use

To start the main beat.editor application:

    $ beat editor start

This will show the main application Window which will allow to browse the prefix
configured or selected by the user.

For more information about the options that can be used with the application:

    $ beat editor --help


### Development
> See `contribute`
