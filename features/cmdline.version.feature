Feature: Get the version of the Atmosphere server

  As a user
  I want to determine the version of the Atmosphere service

  Scenario: Show the atmosphere version
    Given a new working directory
    When I run "atmo version"
    Then it should pass
    And the command output should contain:
        """
        Atmosphere zesty-zapdos @b80381 [Built: 2017-07-25T13:26:59-04:00]
        """
