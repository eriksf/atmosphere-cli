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
                    [--atmo-base-url <atmosphere-base-url>]
                    [--atmo-auth-token <atmosphere-auth-token>]
                    [--atmo-api-server-timeout <atmosphere-api-server-timeout>]

        Atmosphere CLI

        optional arguments:
          --version             show program's version number and exit
          -v, --verbose         Increase verbosity of output. Can be repeated.
          -q, --quiet           Suppress output except warnings and errors.
          --log-file LOG_FILE   Specify a file to log output. Disabled by default.
          -h, --help            Show help message and exit.
          --debug               Show tracebacks on errors.
          --atmo-base-url <atmosphere-base-url>
                                Base URL for the Atmosphere API (Env: ATMO_BASE_URL)
          --atmo-auth-token <atmosphere-auth-token>
                                Token used to authenticate with the Atmosphere API
                                (Env: ATMO_AUTH_TOKEN)
          --atmo-api-server-timeout <atmosphere-api-server-timeout>
                                Server timeout (in seconds) when accessing Atmosphere
                                API (Env: ATMO_API_SERVER_TIMEOUT)

        Commands:
          allocation source list  List allocation sources for a user.
          allocation source show  Show details for an allocation source.
          complete       print bash completion command
          help           print detailed help for another command
          identity list  List user identities managed by Atmosphere.
          identity show  Show details for a user identity.
          image list     List images for user.
          image search   Search images for user.
          image show     Show details for an image.
          image version show  Show details for an image version.
          instance actions  Show available actions for an instance.
          instance create  Create an instance.
          instance list  List instances for user.
          instance show  Show details for an instance.
          project create  Create a project.
          project list   List projects for a user.
          project show   Show details for a project.
          provider list  List cloud providers managed by Atmosphere.
          provider show  Show details for a cloud provider.
          size list      List sizes (instance configurations) for cloud provider.
          size show      Show details for a size (instance configuration).
          version        Show Atmosphere API version.
          volume create  Create a volume.
          volume list    List volumes for a user.
          volume show    Show details for a volume.
        """
