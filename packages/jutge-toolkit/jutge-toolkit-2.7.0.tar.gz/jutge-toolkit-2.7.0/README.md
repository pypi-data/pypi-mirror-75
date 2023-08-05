# Toolkit to make problems for Jutge.org

![Logo](documentation/jutge-toolkit.png)


## Documentation

The `jutge-toolkit` toolkit provides command line tools to
make all necessary files for problems in
[Jutge.org](https://jutge.org/).


## Installation

1. Install the toolkit with `pip3 install jutge-toolkit`.
2. Install `jutge-vinga` with `jutge-install-vinga` (requires root access).

**Note:** In order to use the toolkit, you need to have its external dependencies
installed: Docker, LaTeX and various compilers.


## Upgrade

You can upgrade to the latest version with `pip3 install --upgrade jutge-toolkit`.


## Uninstall

If you want to uninstall the package, use `pip3 uninstall jutge-toolkit`.



## Usage

There are four commands:

- `jutge-make-problem`: Makes all the necessary files to generate a common problem.

- `jutge-make-quiz`: Makes all the necessary files to generate a quiz problem.

- `jutge-compilers`: Outputs information on the supported compilers.

- `jutge-available-compilers`: Outputs information on the available compilers.

For full details, please refer to the [common problem documentation](documentation/problems.md)
and to the [quiz problem documentation](documentation/quizzes.md).


## Credits

- [Jordi Petit](https://github.com/jordi-petit)
- [Cristina Raluca](https://github.com/ralucado)
- [Jordi Reig](https://github.com/jordireig)


## License

Apache License 2.0
