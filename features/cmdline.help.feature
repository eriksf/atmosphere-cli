Feature: Command-line options: Use atmo --help

  As a user
  I want to determine which options are available from atmo
  So that I can use them in feature files or command lines

  Scenario: Use atmo --help
    Given a new working directory
    When I run "atmo --help"
    Then it should pass
    And the command output should contain:
        """
        usage: atmo [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

        Atmosphere CLI

        optional arguments:
          --version            show program's version number and exit
          -v, --verbose        Increase verbosity of output. Can be repeated.
          -q, --quiet          Suppress output except warnings and errors.
          --log-file LOG_FILE  Specify a file to log output. Disabled by default.
          -h, --help           Show help message and exit.
          --debug              Show tracebacks on errors.

        Commands:
          complete       print bash completion command
          help           print detailed help for another command
          image list     List images for user.
          image show     Show details for an image.
          instance list  List instances for user.
        """
