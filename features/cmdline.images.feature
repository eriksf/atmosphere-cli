Feature: Get information about images & image versions

  As a user
  I want to find out about the images/image versions offered by Atmoshere

  Scenario: Show all the available images
    Given a new working directory
    When I run "atmo image list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+-----------------------------------+------------+-----------+------------+
        | uuid                                 | name                              | created_by | is_public | start_date |
        +--------------------------------------+-----------------------------------+------------+-----------+------------+
        | 977e1233-54a4-51f5-97a9-560efd53b975 | Centos 7 (7.4) Development GUI    | jfischer   | True      | 2018-03-20 |
        | 5cc1e738-3d45-5d4f-be5b-4ab53acc5670 | Intel Development (CentOS 7)      | jfischer   | True      | 2018-03-09 |
        | 314739aa-d15f-5a92-976a-3a0d371fc5f6 | R with GCC (CentOS 7)             | jfischer   | True      | 2018-03-09 |
        | 1bc63adf-58e1-53ba-832b-85c2f38c9ec6 | R with Intel compilers (CentOS 7) | jfischer   | True      | 2018-03-09 |
        | c97c4d5e-fe15-5156-b519-0cdb4021492b | Ubuntu 16.04 Devel and Docker     | jfischer   | True      | 2018-03-07 |
        | 225ddf20-c6ef-51e9-973a-dbc49aef05f7 | MATLAB (Based on CentOS 6)        | jfischer   | True      | 2018-02-22 |
        | ead21e76-20e0-5ebd-8df6-e1262a6c1b56 | Ubuntu 14.04.3 Development GUI    | jfischer   | True      | 2018-02-13 |
        | ea2cfe00-fdd1-5288-8cfd-0fe40509ab4f | CentOS 6 (6.9) Development GUI    | jfischer   | True      | 2018-02-13 |
        | ca948f10-c47e-5d06-a2b0-1674cfc002ee | BioLinux 8                        | jfischer   | True      | 2018-02-13 |
        | 54cda684-f7eb-5e4a-84cd-62c998ff4340 | Galaxy Standalone                 | eafgan     | True      | 2017-10-25 |
        +--------------------------------------+-----------------------------------+------------+-----------+------------+
        """

  Scenario: Show all the available images filtered by tag 'docker'
    Given a new working directory
    When I run "atmo image list --tag-name docker"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+--------------------------------+------------+-----------+------------+
        | uuid                                 | name                           | created_by | is_public | start_date |
        +--------------------------------------+--------------------------------+------------+-----------+------------+
        | 977e1233-54a4-51f5-97a9-560efd53b975 | Centos 7 (7.4) Development GUI | jfischer   | True      | 2017-09-15 |
        | c97c4d5e-fe15-5156-b519-0cdb4021492b | Ubuntu 16.04 Devel and Docker  | jfischer   | True      | 2017-09-15 |
        | 70a1df79-fed7-5996-81b1-b5fa711d3d1d | BWW Project Docker and TDS     | atmoadmin  | True      | 2017-08-15 |
        | c7f36646-068c-53f4-a814-4fed48291d5b | Amans Awesome R image          | atmoadmin  | True      | 2017-07-20 |
        | eac2e69e-36d6-541e-ac36-c55491d0d7c0 | Ubuntu_REU_BrandonL            | atmoadmin  | True      | 2017-07-20 |
        | db449f88-2eac-5d6a-8cab-3aa2d59aff8e | Dedalus Ubuntu                 | atmoadmin  | True      | 2017-06-30 |
        | 4c3cc877-efbe-5822-bd35-2b76273a3003 | Ubuntu with Python ML modules  | atmoadmin  | True      | 2017-06-30 |
        | 7754191a-329b-52e5-8199-07f73e8edd58 | PoreCampUSA_TAMU_TxGen_Jun17_2 | noushin    | True      | 2017-06-02 |
        | 0ec12e8b-5c57-5fa3-b617-ca79b5f08313 | Ubuntu 14.04.3 Dev w Docker CE | atmoadmin  | True      | 2017-04-17 |
        | b5b07045-83a8-539d-883a-9b33240c7f78 | trusty-docker                  | atmoadmin  | True      | 2016-11-15 |
        | bdd5cc03-8af6-50a4-ab71-1044ff84cb8d | Docker                         | cboettig   | True      | 2016-05-16 |
        +--------------------------------------+--------------------------------+------------+-----------+------------+
        """

  Scenario: Show all the available images filtered by creator 'jfischer'
    Given a new working directory
    When I run "atmo image list --created-by jfischer"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+-----------------------------------+------------+-----------+------------+
        | uuid                                 | name                              | created_by | is_public | start_date |
        +--------------------------------------+-----------------------------------+------------+-----------+------------+
        | 977e1233-54a4-51f5-97a9-560efd53b975 | Centos 7 (7.4) Development GUI    | jfischer   | True      | 2017-09-15 |
        | c97c4d5e-fe15-5156-b519-0cdb4021492b | Ubuntu 16.04 Devel and Docker     | jfischer   | True      | 2017-09-15 |
        | 1bc63adf-58e1-53ba-832b-85c2f38c9ec6 | R with Intel compilers (CentOS 7) | jfischer   | True      | 2017-09-15 |
        | 314739aa-d15f-5a92-976a-3a0d371fc5f6 | R with GCC (CentOS 7)             | jfischer   | True      | 2017-09-15 |
        | ead21e76-20e0-5ebd-8df6-e1262a6c1b56 | Ubuntu 14.04.3 Development GUI    | jfischer   | True      | 2017-09-15 |
        | ea2cfe00-fdd1-5288-8cfd-0fe40509ab4f | CentOS 6 (6.9) Development GUI    | jfischer   | True      | 2017-09-15 |
        | ca948f10-c47e-5d06-a2b0-1674cfc002ee | BioLinux 8                        | jfischer   | True      | 2017-09-14 |
        | 6bd82a17-0211-5443-8efe-f9f731416a2c | Myers L533 Image                  | jfischer   | True      | 2017-02-09 |
        | 0520cc77-586a-5902-9f5a-d5624dec964e | NeuroDebian - Ubuntu 14.04 GUI    | jfischer   | True      | 2016-11-07 |
        +--------------------------------------+-----------------------------------+------------+-----------+------------+
        """

  Scenario: Show all the available images by searching with text 'galaxy'
    Given a new working directory
    When I run "atmo image search galaxy"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+----------------------+------------+-----------+------------+
        | uuid                                 | name                 | created_by | is_public | start_date |
        +--------------------------------------+----------------------+------------+-----------+------------+
        | 54cda684-f7eb-5e4a-84cd-62c998ff4340 | Galaxy Standalone    | eafgan     | True      | 2017-09-15 |
        | 15a94d1a-4823-52dc-92cb-aec08b55995a | galaxy-workflow      | atmoadmin  | True      | 2017-05-04 |
        | 2cb2e848-7879-5afd-8a2f-dae443ac8c8b | Galaxy in worm world | hokim1     | True      | 2016-09-08 |
        +--------------------------------------+----------------------+------------+-----------+------------+
        """

  Scenario: Show all the details for image 'BioLinux 8'
    Given a new working directory
    When I run "atmo image show ca948f10-c47e-5d06-a2b0-1674cfc002ee"
    Then it should pass
    And the command output should contain:
        """
        +-------------+-------------------------------------------------------------------------------------------------------------------------------+
        | Field       | Value                                                                                                                         |
        +-------------+-------------------------------------------------------------------------------------------------------------------------------+
        | id          | 55                                                                                                                            |
        | uuid        | ca948f10-c47e-5d06-a2b0-1674cfc002ee                                                                                          |
        | name        | BioLinux 8                                                                                                                    |
        | description | Based on Ubuntu 14.04.3 -Trusty Tahr - server - cloudimg                                                                      |
        |             |                                                                                                                               |
        |             | -- **REQUIRES m1.small instance size or larger**                                                                              |
        |             | --  Installed BioLinux 8 (http://environmentalomics.org/bio-linux/)                                                           |
        |             |                                                                                                                               |
        |             | -- x2go installed (http://wiki.x2go.org/doku.php)                                                                             |
        |             |    -- Instructions for x2go are here: https://iujetstream.atlassian.net/wiki/display/JWT/Using+x2go+with+the+BioLinux+8+image |
        |             |                                                                                                                               |
        |             | Installation size ~ 11G                                                                                                       |
        | created_by  | jfischer                                                                                                                      |
        | versions    | 1.8 (201bc19a-d635-4c10-88be-6c3d310d6afd)                                                                                    |
        |             | 1.9 (08e8b08c-a9d9-4e6d-b11c-399f49eb74e2)                                                                                    |
        |             | 1.10 (32c477cc-4fba-41f4-b30f-7db46c2a2651)                                                                                   |
        |             | 1.11 (c602b2a7-6fa6-475c-a2c1-3c2cabba1085)                                                                                   |
        |             | 1.12 (3a7d5262-4184-4e02-a236-7a008fb8986e)                                                                                   |
        | tags        | desktop, gui, Ubuntu, Featured, x2go, bioinformatics, m1_small                                                                |
        | url         | https://use.jetstream-cloud.org/api/v2/images/ca948f10-c47e-5d06-a2b0-1674cfc002ee?format=json                                |
        | is_public   | True                                                                                                                          |
        | start_date  | 2018-04-11                                                                                                                    |
        | end_date    |                                                                                                                               |
        +-------------+-------------------------------------------------------------------------------------------------------------------------------+
        """

  Scenario: Show all the details for image 'BioLinux 8' with all versions
    Given a new working directory
    When I run "atmo image show ca948f10-c47e-5d06-a2b0-1674cfc002ee --show-all-versions"
    Then it should pass
    And the command output should contain:
        """
        +-------------+-------------------------------------------------------------------------------------------------------------------------------+
        | Field       | Value                                                                                                                         |
        +-------------+-------------------------------------------------------------------------------------------------------------------------------+
        | id          | 55                                                                                                                            |
        | uuid        | ca948f10-c47e-5d06-a2b0-1674cfc002ee                                                                                          |
        | name        | BioLinux 8                                                                                                                    |
        | description | Based on Ubuntu 14.04.3 -Trusty Tahr - server - cloudimg                                                                      |
        |             |                                                                                                                               |
        |             | -- **REQUIRES m1.small instance size or larger**                                                                              |
        |             | --  Installed BioLinux 8 (http://environmentalomics.org/bio-linux/)                                                           |
        |             |                                                                                                                               |
        |             | -- x2go installed (http://wiki.x2go.org/doku.php)                                                                             |
        |             |    -- Instructions for x2go are here: https://iujetstream.atlassian.net/wiki/display/JWT/Using+x2go+with+the+BioLinux+8+image |
        |             |                                                                                                                               |
        |             | Installation size ~ 11G                                                                                                       |
        | created_by  | jfischer                                                                                                                      |
        | versions    | 1.0 (20911195-5f31-48e7-8d1a-d36b5af466ac)                                                                                    |
        |             | 1.1 (55a39902-677a-4667-9da0-eef612660d1f)                                                                                    |
        |             | 1.3 (4faaa97e-e3a1-47f3-bf93-e83e4ed7f18c)                                                                                    |
        |             | 1.4 (dd137e13-71f0-4464-b387-39cfd176c59d)                                                                                    |
        |             | 1.6 (cb2c86d3-6256-4a5c-a994-6c5c47f61de9)                                                                                    |
        |             | 1.7 (40440e67-8644-4949-ba2f-b36c66f9d40b)                                                                                    |
        |             | 1.2 (483e936f-2b97-4272-9959-a554767f21c9)                                                                                    |
        |             | 1.8 (201bc19a-d635-4c10-88be-6c3d310d6afd)                                                                                    |
        |             | 1.9 (08e8b08c-a9d9-4e6d-b11c-399f49eb74e2)                                                                                    |
        |             | 1.5 (c852e607-1c87-4d63-a503-c6c924ee17d6)                                                                                    |
        |             | 1.10 (32c477cc-4fba-41f4-b30f-7db46c2a2651)                                                                                   |
        |             | 1.12 (3a7d5262-4184-4e02-a236-7a008fb8986e)                                                                                   |
        |             | 1.11 (c602b2a7-6fa6-475c-a2c1-3c2cabba1085)                                                                                   |
        | tags        | desktop, gui, Ubuntu, Featured, x2go, bioinformatics, m1_small                                                                |
        | url         | https://use.jetstream-cloud.org/api/v2/images/ca948f10-c47e-5d06-a2b0-1674cfc002ee?format=json                                |
        | is_public   | True                                                                                                                          |
        | start_date  | 2018-04-11                                                                                                                    |
        | end_date    |                                                                                                                               |
        +-------------+-------------------------------------------------------------------------------------------------------------------------------+
        """

  Scenario: Show all the details for image version 'BioLinux 8 version 1.7'
    Given a new working directory
    When I run "atmo image version show 40440e67-8644-4949-ba2f-b36c66f9d40b"
    Then it should pass
    And the command output should contain:
        """
        +-------------------+-------------------------------------------------------------------------------------------------------------------------------+
        | Field             | Value                                                                                                                         |
        +-------------------+-------------------------------------------------------------------------------------------------------------------------------+
        | id                | 40440e67-8644-4949-ba2f-b36c66f9d40b                                                                                          |
        | name              | 1.7                                                                                                                           |
        | image_name        | BioLinux 8                                                                                                                    |
        | image_description | Based on Ubuntu 14.04.3 -Trusty Tahr - server - cloudimg                                                                      |
        |                   |                                                                                                                               |
        |                   | -- **REQUIRES m1.small instance size or larger**                                                                              |
        |                   | --  Installed BioLinux 8 (http://environmentalomics.org/bio-linux/)                                                           |
        |                   |                                                                                                                               |
        |                   | -- x2go installed (http://wiki.x2go.org/doku.php)                                                                             |
        |                   |    -- Instructions for x2go are here: https://iujetstream.atlassian.net/wiki/display/JWT/Using+x2go+with+the+BioLinux+8+image |
        | created_by        | jfischer                                                                                                                      |
        | change_log        | v1.7 - patched up to 9-14-17                                                                                                  |
        | machines          | Jetstream - Indiana University (1be8ac59-54e4-4421-b370-f6cf584cea85)                                                         |
        |                   | Jetstream - TACC (1be8ac59-54e4-4421-b370-f6cf584cea85)                                                                       |
        | allow_imaging     | True                                                                                                                          |
        | min_mem           | None                                                                                                                          |
        | min_cpu           | None                                                                                                                          |
        | start_date        | 2017-09-14T19:18:04.091069Z                                                                                                   |
        +-------------------+-------------------------------------------------------------------------------------------------------------------------------+
        """

  Scenario: Show all the available image versions for image 'BioLinux 8'
    Given a new working directory
    When I run "atmo image version list ca948f10-c47e-5d06-a2b0-1674cfc002ee"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+------+------------+------------+-----------------------------------------------------------------------+------------+
        | id                                   | name | image_name | created_by | machines                                                              | start_date |
        +--------------------------------------+------+------------+------------+-----------------------------------------------------------------------+------------+
        | 201bc19a-d635-4c10-88be-6c3d310d6afd | 1.8  | BioLinux 8 | jfischer   | Jetstream - Indiana University (bbcadf9a-f18c-4111-b083-dcbdbd5830f6) | 2017-11-03 |
        |                                      |      |            |            | Jetstream - TACC (bbcadf9a-f18c-4111-b083-dcbdbd5830f6)               |            |
        | 08e8b08c-a9d9-4e6d-b11c-399f49eb74e2 | 1.9  | BioLinux 8 | jfischer   | Jetstream - Indiana University (c2049632-7631-447d-99ff-63aefc977f4f) | 2017-12-06 |
        |                                      |      |            |            | Jetstream - TACC (c2049632-7631-447d-99ff-63aefc977f4f)               |            |
        | 32c477cc-4fba-41f4-b30f-7db46c2a2651 | 1.10 | BioLinux 8 | jfischer   | Jetstream - Indiana University (e461276d-938c-4df6-b352-b56f44add78a) | 2018-01-10 |
        |                                      |      |            |            | Jetstream - TACC (e461276d-938c-4df6-b352-b56f44add78a)               |            |
        | c602b2a7-6fa6-475c-a2c1-3c2cabba1085 | 1.11 | BioLinux 8 | jfischer   | Jetstream - Indiana University (a6980af1-c438-4834-8202-5cbfdcfb094e) | 2018-02-13 |
        |                                      |      |            |            | Jetstream - TACC (a6980af1-c438-4834-8202-5cbfdcfb094e)               |            |
        | 3a7d5262-4184-4e02-a236-7a008fb8986e | 1.12 | BioLinux 8 | jfischer   | Jetstream - Indiana University (108a3472-7425-49c5-8aae-afe2f7e4ae42) | 2018-04-11 |
        |                                      |      |            |            | Jetstream - TACC (108a3472-7425-49c5-8aae-afe2f7e4ae42)               |            |
        +--------------------------------------+------+------------+------------+-----------------------------------------------------------------------+------------+
        """
