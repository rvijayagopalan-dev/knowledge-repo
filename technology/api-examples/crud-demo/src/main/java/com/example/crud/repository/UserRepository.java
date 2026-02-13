package com.example.crud.repository;

import com.example.crud.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class UserRepository {
    private final ConcurrentHashMap<Long, User> users = new ConcurrentHashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);

    public UserRepository() {
        // Initialize with sample data for testing
        User user1 = new User("Alice Johnson", "alice@example.com");
        user1.setId(idGenerator.getAndIncrement());
        users.put(user1.getId(), user1);

        User user2 = new User("Bob Smith", "bob@example.com");
        user2.setId(idGenerator.getAndIncrement());
        users.put(user2.getId(), user2);

        User user3 = new User("Charlie Brown", "charlie@example.com");
        user3.setId(idGenerator.getAndIncrement());
        users.put(user3.getId(), user3);
    }

    /**
     * Save a new user to the repository
     */
    public User save(User user) {
        if (user.getId() == null) {
            user.setId(idGenerator.getAndIncrement());
        }
        users.put(user.getId(), user);
        return user;
    }

    /**
     * Find a user by ID
     */
    public Optional<User> findById(Long id) {
        return Optional.ofNullable(users.get(id));
    }

    /**
     * Find all users
     */
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }

    /**
     * Update an existing user
     */
    public Optional<User> update(Long id, User updatedUser) {
        User existingUser = users.get(id);
        if (existingUser == null) {
            return Optional.empty();
        }

        if (updatedUser.getName() != null) {
            existingUser.setName(updatedUser.getName());
        }
        if (updatedUser.getEmail() != null) {
            existingUser.setEmail(updatedUser.getEmail());
        }

        users.put(id, existingUser);
        return Optional.of(existingUser);
    }

    /**
     * Delete a user by ID
     */
    public boolean deleteById(Long id) {
        return users.remove(id) != null;
    }

    /**
     * Check if a user exists by ID
     */
    public boolean existsById(Long id) {
        return users.containsKey(id);
    }

    /**
     * Get the total count of users
     */
    public long count() {
        return users.size();
    }

    /**
     * Clear all users (useful for testing)
     */
    public void clear() {
        users.clear();
        idGenerator.set(1);
    }
}
