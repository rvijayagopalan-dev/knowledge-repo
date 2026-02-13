package com.example.crud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CrudDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(CrudDemoApplication.class, args);

        System.out.println("\n" + "=".repeat(80));
        System.out.println("CRUD Demo Application Started Successfully!");
        System.out.println("=".repeat(80));
        System.out.println("\nAvailable APIs:");
        System.out.println("  1. REST API:");
        System.out.println("     - Base URL: http://localhost:8080/api/users");
        System.out.println("     - Endpoints: POST, GET, PUT, DELETE");
        System.out.println();
        System.out.println("  2. GraphQL API:");
        System.out.println("     - GraphQL Endpoint: http://localhost:8080/graphql");
        System.out.println("     - GraphiQL UI: http://localhost:8080/graphiql");
        System.out.println();
        System.out.println("  3. gRPC API:");
        System.out.println("     - Server running on: localhost:9090");
        System.out.println("     - Service: UserService");
        System.out.println();
        System.out.println("Sample data has been loaded. Try querying the APIs!");
        System.out.println("=".repeat(80) + "\n");
    }
}
