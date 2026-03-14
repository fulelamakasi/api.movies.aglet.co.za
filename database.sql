DROP DATABASE IF EXISTS aglet_movies;

CREATE DATABASE IF NOT EXISTS aglet_movies;
USE aglet_movies;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phonenumber` varchar(191) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 0,
  `token` VARCHAR(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `edited_by` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `permissions`;
CREATE TABLE permissions (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT NOT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT '1',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT '',
    FULLTEXT `descriptionx` (`description`),
    UNIQUE (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `roles`;
CREATE TABLE roles (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT NOT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT '1',
    `is_admin` TINYINT(1) NOT NULL DEFAULT '0',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT '',
    FULLTEXT `descriptionx` (`description`),
    UNIQUE (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE role_permissions (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `role_id` INT UNSIGNED NOT NULL,
    FOREIGN KEY (`role_id`) REFERENCES roles(`id`),
    `permission_id` INT UNSIGNED NOT NULL,
    FOREIGN KEY (`permission_id`) REFERENCES permissions(`id`),
    `is_active` TINYINT(1) NOT NULL DEFAULT '1',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT '',
    UNIQUE `role_permission` (`role_id`, `permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `user_roles`;
CREATE TABLE user_roles (
    `id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` INT UNSIGNED NOT NULL,
    `role_id` INT UNSIGNED NOT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT '1',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT '',
    FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    FOREIGN KEY (`role_id`) REFERENCES roles(`id`),
    UNIQUE `user_role` (`user_id`, `role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `movies`;
CREATE TABLE movies(
    `id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tmdb_id` INT NOT NULL UNIQUE,
    `title` VARCHAR(255),
    `overview` TEXT,
    `release_date` DATE,
    `poster_path` VARCHAR(255),
    `backdrop_path` VARCHAR(255),
    `popularity` DECIMAL(10,2),
    `vote_average` DECIMAL(3,1),
    `vote_count` INT,
    `language` VARCHAR(10),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT ''
);