package com.example.crud.graphql;

import com.example.crud.model.User;
import com.example.crud.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
public class UserGraphQLController {

    private final UserRepository userRepository;

    @Autowired
    public UserGraphQLController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Query: Get all users
     */
    @QueryMapping
    public List<User> users() {
        return userRepository.findAll();
    }

    /**
     * Query: Get user by ID
     */
    @QueryMapping
    public User user(@Argument Long id) {
        return userRepository.findById(id).orElse(null);
    }

    /**
     * Query: Get user count
     */
    @QueryMapping
    public Long userCount() {
        return userRepository.count();
    }

    /**
     * Mutation: Create a new user
     */
    @MutationMapping
    public User createUser(@Argument String name, @Argument String email) {
        User user = new User(name, email);
        return userRepository.save(user);
    }

    /**
     * Mutation: Update an existing user
     */
    @MutationMapping
    public User updateUser(@Argument Long id, @Argument String name, @Argument String email) {
        User updateData = new User();
        updateData.setName(name);
        updateData.setEmail(email);
        return userRepository.update(id, updateData).orElse(null);
    }

    /**
     * Mutation: Delete a user
     */
    @MutationMapping
    public Boolean deleteUser(@Argument Long id) {
        return userRepository.deleteById(id);
    }
}
