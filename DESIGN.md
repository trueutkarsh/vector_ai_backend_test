
# Design Ideas

*   Database Table Initial Design [Part 1]
    *   Ideas
        *   The design is pretty straightforward from the description. We need three separate tables for each continent, country and city and two relationship tables between continent and country and country and city. Following will be database design 
        *   CONTINENT
            *   name (P.K)
            *   population
        *   COUNTRY
            *   name(P.K)
            *   population
            *   num_hospitals
            *   num_rivers
            *   num_schools
        *   CITY
            *   name(P.K)
            *   area
            *   num_roads
            *   num_trees
            *   num_shops
            *   num_schools
        *   CITY_COUNTRY
            *   city_name (F.K) (City.name) (unique key) (On delete cascade)
            *   country_name (F.K) (Country.name) (dup key) (On delete cascade)
        *   COUNTRY_CONTINENT
            *   country_name (F.K) (Country.name) (unique key) (On delete cascade)
            *   continent_name (F.K) (Country.name) (dup key) (On delete cascade)
*   Database Table Validations
    <!-- *   APPROACH 1
        *   Plain inserts into table continent, country, and city can take place without any validation (individual field validations) [The design as of now allows isolated cities, countries and continents to exist in database. We can later decide if we want to allow this throughs service apis]
        *   Inserts into relation tables will definitely require validations which can be implemented through usage of triggers
            *   Triggers for tables
                *   COUNTRY_CONTINENT
                    *   On CREATE
                        *   Check that the total sum of population in countries in the targeted continent (including the one to be inserted ) is less than population of targeted continent
                    *   On UPDATE
                        *   Check that the total sum of population in countries in the targeted continent (including the one to be inserted ) is less than population of targeted continent
                *   CITY_COUNTRY
                    *   ON CREATE
                        *   Check that the total sum of population in countries in the targeted continent (including the one to be inserted ) is less than population of targeted continent
                        *   Check that the total sum of schools in cities in the targeted country (including the one to be inserted ) is less than number of schools of targeted country
                    *   ON UPDATE
                        *   Check that the total sum of population in countries in the targeted continent (including the one to be inserted ) is less than population of targeted continent
                        *   Check that the total sum of schools in cities in the targeted country (including the one to be inserted ) is less than number of schools of targeted country -->
    *   APPROACH
        *   I am not sure about the performance of database triggers but I kinda believe it’ll be faster than implementing it in service code but, anything more than these validations would make the sql a bit cluttered. But unless we are expecting very high volume (can be checked and verified through  calculating time) writing data validations in service DB layer also doesn’t seem like a bad idea to me
            *   We can maintain an in-memory cache of total sum of population for every continent and country and total sum of number of schools for each insert of city, country we can verify if adding it would surpass the desired population for continent, country and city or for desired number of schools for each country and city
            *   Since the limit for number of continents and cities is pretty limited,  \
Not more than 1000 at max, storing this in-memory shouldn’t be an issue. And we can also add more custom validations other than simple sum check and reduce the number of database interactions [for future use]
            *   I’ve looked at the further design for this application, as of now we have just one writer. Hence this doesn’t even leave a scope for race conditions or thread safety and in future if we want to scale this application to multiple writers to db, we can protect this cache by a reader writer lock. 
            *   This approach has one downside that if the machine restarts or goes down, the cache will be lost but we can warm up the cache or recreate it using simple queries from db. If any time the cache is empty or the service is restarting we can build it. 

    _I am fine implementing any of the approaches but IMO this approach produces more clear and extensible code so I’ll prefer this but I want to discuss it with you._

*   Client and Message Broker [PART 2]
    *   Initial Design
        *   As mentioned in the problem statement due to high volume of reads, writes and updates, the requests have to be managed via Kafka
        *   _Client_
            *   Each Client would act as 
                *   **Kafka Producer - **sending a request for read, write or update on topic - _kf.vector.ai.requests_
                *   **Kafka Consumer - **receiving a response from writers on topic kf.vector.ai.reponses.[client_id/unique_id]
        *   Writer
            *   Each Writer would act as
                *   **Kafka Consumer - **receiving a request from clients on topic _kf.vector.ai.requests_
                *   **Kafka Produce - **sending a reponse for read, write or update on topic - kf.vector.ai.reponses.[client_id/unique_id]


## Logging and Packaging [Part 3]

*   Logging
    *   Create a logging module
    *   Implement logging at following places
        *   For clients [logs on client’s machine]
            *   Clients sending request 
            *   Clients receiving response
        *   For writer [logs on writer’s machine]
            *   Writer receiving request
            *   Writer returning response [Successful/Unsuccessful operation]
            *   Re-Building up cache
*   Docker
    *   Find all dependencies of client and writer’s application
    *   Make a docker file
        *   For Clients [client.docker]
            *   _Application layer_
                *   Dependencies of service layer
                *   Kafka Library 
            *   _Middleware layer _
                *   Create a separate docker instance which can spin up a kafka instance
        *   For Writers [writer.service.docker]
            *   _Application/Service layer _
                *   Dependencies of service layer
                *   Kafka library
                *   Database accessor library
            *   _Middleware layer_
                *   Create a separate docker instance which can spin up a kafka instance
            *   _Database layer [writer.database.docker]_
                *   Create a separate docker instance which can spin up a sql database
    *   Make one docker file which has every dependencies for Clients and Writers in one docker file and test everything works fine.
        *   Write integration tests
    *   Create a docker compose file with networks connecting application applications layer to middleware layer for clients and application layer to middleware layer and database layer


## Design Discussions and Deployment [Part 4]



*   Database validation
    *   Discussed above ? Although since the problem statements mentions specifically add validation to database, looks like the approach 1 would seem more appropriate ? We can discuss more
    *   Client and Message Design
        *   To me it was a pretty straightforward problem
            *   Clients will make requests through kafka
            *   Writers will process the request, make db operations and send the response
    *   Deployment
        *   I will deploy this whole application, client and writers on AWS  as well create database on AWS. This is a long shot but for me, I’ll look for deploying docker instances directly to cloud with correct credentials, database names and kafka topics. I can tell more when I reach this stage
