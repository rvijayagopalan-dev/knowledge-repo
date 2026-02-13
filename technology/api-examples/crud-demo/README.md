# CRUD Demo - REST, GraphQL, and gRPC

A comprehensive demonstration project showcasing simple CRUD (Create, Read, Update, Delete) operations for a User entity using three different API paradigms:
- **REST API** - Traditional HTTP endpoints
- **GraphQL API** - Query language for APIs
- **gRPC API** - High-performance RPC framework

## Features

- **Three API Implementations** sharing the same business logic
- **In-Memory Storage** using ConcurrentHashMap (thread-safe)
- **Sample Data** pre-loaded for testing
- **Spring Boot** best practices
- **Validation** using Jakarta Bean Validation
- **GraphiQL** interactive GraphQL IDE
- **Protocol Buffers** for gRPC

## Prerequisites

- Java 17 or higher
- Maven 3.6 or higher
- (Optional) `curl` for testing REST API
- (Optional) `grpcurl` for testing gRPC API

## Build & Run

### 1. Build the Project

```bash
cd technology/api-examples/crud-demo
mvn clean install
```

This will:
- Download dependencies
- Compile Java code
- Generate gRPC stub classes from `.proto` files

### 2. Run the Application

```bash
mvn spring-boot:run
```

The application will start with:
- REST API on port **8080**
- GraphQL endpoint at **/graphql**
- GraphiQL UI at **/graphiql**
- gRPC server on port **9090**

## API Documentation

### User Model

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "createdAt": "2024-01-15T10:30:00"
}
```

## 1. REST API

Base URL: `http://localhost:8080/api/users`

### Create User
```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'
```

**Response:**
```json
{
  "id": 4,
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-02-12T15:30:45.123"
}
```

### Get All Users
```bash
curl http://localhost:8080/api/users
```

### Get User by ID
```bash
curl http://localhost:8080/api/users/1
```

### Update User
```bash
curl -X PUT http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com"}'
```

### Delete User
```bash
curl -X DELETE http://localhost:8080/api/users/1
```

### Get User Count
```bash
curl http://localhost:8080/api/users/count
```

## 2. GraphQL API

### GraphiQL Interactive UI

Open your browser and navigate to:
```
http://localhost:8080/graphiql
```

This provides an interactive interface for testing GraphQL queries and mutations.

### GraphQL Endpoint

URL: `http://localhost:8080/graphql`

### Query Examples

#### Get All Users
```graphql
query {
  users {
    id
    name
    email
    createdAt
  }
}
```

#### Get User by ID
```graphql
query {
  user(id: 1) {
    id
    name
    email
    createdAt
  }
}
```

#### Get User Count
```graphql
query {
  userCount
}
```

### Mutation Examples

#### Create User
```graphql
mutation {
  createUser(name: "John Doe", email: "john@example.com") {
    id
    name
    email
    createdAt
  }
}
```

#### Update User
```graphql
mutation {
  updateUser(id: 1, name: "Jane Doe", email: "jane@example.com") {
    id
    name
    email
    createdAt
  }
}
```

#### Delete User
```graphql
mutation {
  deleteUser(id: 1)
}
```

### Using curl with GraphQL

```bash
curl -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { users { id name email } }"
  }'
```

## 3. gRPC API

### Install grpcurl (Optional)

For Windows (using Chocolatey):
```bash
choco install grpcurl
```

For macOS:
```bash
brew install grpcurl
```

For Linux:
```bash
# Download from https://github.com/fullstorydev/grpcurl/releases
```

### gRPC Service Details

- **Server:** `localhost:9090`
- **Service:** `UserService`
- **Package:** `user`

### List Available Services
```bash
grpcurl -plaintext localhost:9090 list
```

### Describe UserService
```bash
grpcurl -plaintext localhost:9090 describe user.UserService
```

### Create User
```bash
grpcurl -plaintext -d '{
  "name": "John Doe",
  "email": "john@example.com"
}' localhost:9090 user.UserService/CreateUser
```

### Get User by ID
```bash
grpcurl -plaintext -d '{
  "id": 1
}' localhost:9090 user.UserService/GetUser
```

### Get All Users
```bash
grpcurl -plaintext -d '{}' localhost:9090 user.UserService/GetAllUsers
```

### Update User
```bash
grpcurl -plaintext -d '{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane@example.com"
}' localhost:9090 user.UserService/UpdateUser
```

### Delete User
```bash
grpcurl -plaintext -d '{
  "id": 1
}' localhost:9090 user.UserService/DeleteUser
```

## Project Structure

```
crud-demo/
├── pom.xml
├── README.md
└── src/
    └── main/
        ├── java/com/example/crud/
        │   ├── CrudDemoApplication.java      # Main application
        │   ├── model/
        │   │   └── User.java                  # User entity
        │   ├── repository/
        │   │   └── UserRepository.java        # In-memory storage
        │   ├── rest/
        │   │   └── UserRestController.java    # REST endpoints
        │   ├── graphql/
        │   │   └── UserGraphQLController.java # GraphQL resolvers
        │   └── grpc/
        │       └── UserGrpcService.java       # gRPC service
        ├── proto/
        │   └── user.proto                     # gRPC protocol buffer
        └── resources/
            ├── application.yml                # Spring configuration
            └── graphql/
                └── schema.graphqls            # GraphQL schema
```

## Key Technologies

- **Spring Boot 3.2.2** - Application framework
- **Spring Web** - REST API support
- **Spring GraphQL** - GraphQL API support
- **gRPC Spring Boot Starter** - gRPC integration
- **Protocol Buffers** - gRPC serialization
- **Jakarta Validation** - Bean validation
- **Maven** - Build tool

## Comparison: REST vs GraphQL vs gRPC

| Feature | REST | GraphQL | gRPC |
|---------|------|---------|------|
| **Protocol** | HTTP/JSON | HTTP/JSON | HTTP/2 + Protobuf |
| **Data Format** | JSON | JSON | Binary (Protocol Buffers) |
| **Schema** | OpenAPI (optional) | Strong typed schema | Protocol Buffers (.proto) |
| **Over-fetching** | Common | Eliminated | N/A |
| **Under-fetching** | Common | Eliminated | N/A |
| **Performance** | Good | Good | Excellent |
| **Browser Support** | Native | Native | Limited (requires proxy) |
| **Tooling** | Excellent | Growing | Good |
| **Learning Curve** | Easy | Moderate | Moderate-Hard |
| **Best For** | Public APIs, CRUD | Complex queries, mobile | Microservices, high performance |

## Sample Data

The application comes pre-loaded with three sample users:

1. **Alice Johnson** - alice@example.com
2. **Bob Smith** - bob@example.com
3. **Charlie Brown** - charlie@example.com

## Validation

The User model includes validation:
- **Name**: Cannot be blank
- **Email**: Must be a valid email format

Invalid requests will return appropriate error responses.

## Notes

- Data is stored **in-memory** and will be reset when the application restarts
- All three APIs share the **same UserRepository** instance
- The application uses **thread-safe** ConcurrentHashMap for storage
- IDs are auto-generated using AtomicLong

## Learning Resources

### REST
- [Spring Boot REST Tutorial](https://spring.io/guides/tutorials/rest/)
- [RESTful Web Services](https://restfulapi.net/)

### GraphQL
- [GraphQL Official Documentation](https://graphql.org/)
- [Spring for GraphQL](https://spring.io/projects/spring-graphql)

### gRPC
- [gRPC Official Documentation](https://grpc.io/)
- [gRPC Spring Boot Starter](https://github.com/grpc-ecosystem/grpc-spring-boot-starter)

## Troubleshooting

### Port Already in Use

If port 8080 or 9090 is already in use, modify `src/main/resources/application.yml`:

```yaml
server:
  port: 8081  # Change REST port

grpc:
  server:
    port: 9091  # Change gRPC port
```

### gRPC Generation Issues

If gRPC stub classes are not generated, run:
```bash
mvn clean compile
```

### GraphiQL Not Working

Ensure GraphiQL is enabled in `application.yml`:
```yaml
spring:
  graphql:
    graphiql:
      enabled: true
```

## License

This is a demonstration project for educational purposes.

## Contributing

This project is part of a knowledge repository. Feel free to use it as a learning resource and reference implementation.
