package com.example.crud.grpc;

import com.example.crud.grpc.proto.*;
import com.example.crud.model.User;
import com.example.crud.repository.UserRepository;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Optional;

@GrpcService
public class UserGrpcService extends UserServiceGrpc.UserServiceImplBase {

    private final UserRepository userRepository;
    private static final DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    @Autowired
    public UserGrpcService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Create a new user
     */
    @Override
    public void createUser(CreateUserRequest request, StreamObserver<com.example.crud.grpc.proto.User> responseObserver) {
        User user = new User(request.getName(), request.getEmail());
        User savedUser = userRepository.save(user);

        com.example.crud.grpc.proto.User grpcUser = convertToGrpcUser(savedUser);

        responseObserver.onNext(grpcUser);
        responseObserver.onCompleted();
    }

    /**
     * Get user by ID
     */
    @Override
    public void getUser(GetUserRequest request, StreamObserver<com.example.crud.grpc.proto.User> responseObserver) {
        Optional<User> userOpt = userRepository.findById(request.getId());

        if (userOpt.isPresent()) {
            com.example.crud.grpc.proto.User grpcUser = convertToGrpcUser(userOpt.get());
            responseObserver.onNext(grpcUser);
            responseObserver.onCompleted();
        } else {
            responseObserver.onError(new RuntimeException("User not found with id: " + request.getId()));
        }
    }

    /**
     * Get all users
     */
    @Override
    public void getAllUsers(GetAllUsersRequest request, StreamObserver<UserListResponse> responseObserver) {
        List<User> users = userRepository.findAll();

        UserListResponse.Builder responseBuilder = UserListResponse.newBuilder();
        for (User user : users) {
            responseBuilder.addUsers(convertToGrpcUser(user));
        }

        responseObserver.onNext(responseBuilder.build());
        responseObserver.onCompleted();
    }

    /**
     * Update user
     */
    @Override
    public void updateUser(UpdateUserRequest request, StreamObserver<com.example.crud.grpc.proto.User> responseObserver) {
        User updateData = new User();
        if (request.getName() != null && !request.getName().isEmpty()) {
            updateData.setName(request.getName());
        }
        if (request.getEmail() != null && !request.getEmail().isEmpty()) {
            updateData.setEmail(request.getEmail());
        }

        Optional<User> updatedUserOpt = userRepository.update(request.getId(), updateData);

        if (updatedUserOpt.isPresent()) {
            com.example.crud.grpc.proto.User grpcUser = convertToGrpcUser(updatedUserOpt.get());
            responseObserver.onNext(grpcUser);
            responseObserver.onCompleted();
        } else {
            responseObserver.onError(new RuntimeException("User not found with id: " + request.getId()));
        }
    }

    /**
     * Delete user
     */
    @Override
    public void deleteUser(DeleteUserRequest request, StreamObserver<DeleteUserResponse> responseObserver) {
        boolean deleted = userRepository.deleteById(request.getId());

        DeleteUserResponse response = DeleteUserResponse.newBuilder()
                .setSuccess(deleted)
                .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    /**
     * Convert domain User to gRPC User
     */
    private com.example.crud.grpc.proto.User convertToGrpcUser(User user) {
        return com.example.crud.grpc.proto.User.newBuilder()
                .setId(user.getId())
                .setName(user.getName())
                .setEmail(user.getEmail())
                .setCreatedAt(user.getCreatedAt().format(formatter))
                .build();
    }
}
