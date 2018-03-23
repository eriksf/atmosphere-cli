Feature: Get information about sizes (instance configurations)

  As a user
  I want to find out about the sizes (instance configurations) offered by Atmoshere

  Scenario: Show all the available sizes (instance configurations)
    Given a new working directory
    When I run "atmo size list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+-----------------------+-------+-------------------+-----+--------+------+--------+------------+
        | uuid                                 | name                  | alias | provider          | cpu | memory | disk | active | start_date |
        +--------------------------------------+-----------------------+-------+-------------------+-----+--------+------+--------+------------+
        | 5fb893dd-f1c0-45bd-8f6f-cfb721bcf303 | manila-service-flavor | 100   | Cloudlab - ErikOS |   1 |    256 |    0 | True   | 2017-09-18 |
        | c9fdefca-0a5a-40c2-b706-2b55a6c92ab8 | m1.tiny               | 1     | Cloudlab - ErikOS |   1 |    512 |    1 | True   | 2017-09-18 |
        | d2c5df07-1a01-4074-b3d2-87acaa9ac355 | m1.small              | 2     | Cloudlab - ErikOS |   1 |   2048 |   20 | True   | 2017-09-18 |
        | 2fac806b-5000-4489-9252-e0e4b1f00f5e | m1.medium             | 3     | Cloudlab - ErikOS |   2 |   4096 |   40 | True   | 2017-09-18 |
        | 013efc26-de0d-4455-aaf9-023a6c9138de | m1.large              | 4     | Cloudlab - ErikOS |   4 |   8192 |   80 | True   | 2017-09-18 |
        | 8e2b76c3-d988-4721-ac44-191e8186f416 | m1.xlarge             | 5     | Cloudlab - ErikOS |   8 |  16384 |  160 | True   | 2017-09-18 |
        +--------------------------------------+-----------------------+-------+-------------------+-----+--------+------+--------+------------+
        """

  Scenario: Show all the available sizes (instance configurations) filtered by a provider
    Given a new working directory
    When I run "atmo size list --provider-id 2"
    Then it should pass
    And the command output should contain:
        """
        """

  Scenario: Show all the details for size m1.large
    Given a new working directory
    When I run "atmo size show 013efc26-de0d-4455-aaf9-023a6c9138de"
    Then it should pass
    And the command output should contain:
        """
        +---------------+--------------------------------------+
        | Field         | Value                                |
        +---------------+--------------------------------------+
        | id            | 5                                    |
        | uuid          | 013efc26-de0d-4455-aaf9-023a6c9138de |
        | name          | m1.large                             |
        | alias         | 4                                    |
        | provider_id   | 4                                    |
        | provider_name | Cloudlab - ErikOS                    |
        | provider_uuid | e367f6fa-e834-4fe6-873c-bba4344d1464 |
        | cpu           | 4                                    |
        | memory        | 8192                                 |
        | disk          | 80                                   |
        | active        | True                                 |
        | root          | 0                                    |
        | start_date    | 2017-09-18                           |
        | end_date      |                                      |
        +---------------+--------------------------------------+
        """
