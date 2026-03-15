DROP DATABASE IF EXISTS aglet_movies;

CREATE DATABASE IF NOT EXISTS aglet_movies;
USE aglet_movies;

DROP TABLE IF EXISTS `languages`;
CREATE TABLE languages (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT NOT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT '1',
    `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT '',
    FULLTEXT `descriptionx` (`description`),
    UNIQUE (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `contactus`;
CREATE TABLE contactus (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL,
    `company_name` VARCHAR(100) NOT NULL,
    `message` TEXT NOT NULL,
    `is_actioned` TINYINT(1) NOT NULL DEFAULT '0',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT '',
    FULLTEXT `descriptionx` (`description`),
    UNIQUE (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phonenumber` varchar(191) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 0,
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
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
    `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
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
    `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
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
    `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
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
    `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
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
    `language_id` INT UNSIGNED NOT NULL,
    FOREIGN KEY (`language_id`) REFERENCES languages(`id`),
    `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    `edited_by` varchar(100) NOT NULL DEFAULT ''
);

-- seed data
INSERT INTO `languages` (`name`, `description`, `is_active`, `is_deleted`, `edited_by`) VALUES
('English', 'A West Germanic language originating in England, and the first language for most people in the United Kingdom, the United States, Canada, Australia, New Zealand, and Ireland. It is widely used as a lingua franca across the globe.', 1, 0, 'system'),
('Spanish', 'A Romance language that originated in the Iberian Peninsula and is now spoken by over 500 million people worldwide, primarily in Spain and the Americas.', 1, 0, 'system'),
('French', 'A Romance language of the Indo-European family that originated in northern France and is spoken as a first language in France, Canada, Belgium, Switzerland, and many African countries.', 1, 0, 'system'),
('German', 'A West Germanic language mainly spoken in Central Europe, official language in Germany, Austria, Switzerland, and Liechtenstein.', 1, 0, 'system'),
('Mandarin Chinese', 'The most spoken language in the world, part of the Sino-Tibetan language family, and the official language of China and Taiwan.', 1, 0, 'system'),
('Arabic', 'A Central Semitic language that is the liturgical language of Islam and official language in over 20 countries across the Middle East and North Africa.', 1, 0, 'system'),
('Portuguese', 'A Romance language originating in the Iberian Peninsula and the official language of Portugal, Brazil, Angola, and several other African nations.', 1, 0, 'system'),
('Russian', 'An East Slavic language and the official language of Russia, Belarus, Kazakhstan, and Kyrgyzstan, widely spoken throughout Eastern Europe and Central Asia.', 1, 0, 'system'),
('Japanese', 'An East Asian language spoken primarily in Japan, known for its three writing systems: Hiragana, Katakana, and Kanji.', 1, 0, 'system'),
('Italian', 'A Romance language that originated in Italy and is spoken primarily in Italy, Switzerland, San Marino, and Vatican City.', 1, 0, 'system'),
('Dutch', 'A West Germanic language spoken in the Netherlands, Belgium, and Suriname, and official language of several Caribbean islands.', 1, 0, 'system'),
('Afrikaans', 'A West Germanic language derived from Dutch, spoken in South Africa and Namibia, and one of the eleven official languages of South Africa.', 1, 0, 'system'),
('Zulu', 'A Southern Bantu language and one of the eleven official languages of South Africa, spoken primarily by the Zulu people.', 1, 0, 'system'),
('Xhosa', 'A Nguni Bantu language and one of the official languages of South Africa, known for its distinctive click consonants.', 1, 0, 'system'),
('Swahili', 'A Bantu language widely spoken in East Africa, serving as a lingua franca in countries like Kenya, Tanzania, and Uganda.', 1, 0, 'system');

INSERT INTO `users` (`email`, `password`, `phonenumber`, `name`, `is_active`, `is_deleted`, `token`, `created_at`, `updated_at`, `edited_by`) VALUES
('jointheteam@aglet.co.za', '$2y$10$YourHashedPasswordHere', '+27 11 123 4567', 'Aglet Team User', 1, 0, '79f04878-a79d-4ea9-ba40-8ee21abab16c', NOW(), NULL, 'system'),
('admin@aglet.co.za', '$2y$10$YourHashedPasswordHere', '+27 11 234 5678', 'Admin User', 1, 0, 'fb30e810-3269-43f1-bc06-09c5e0bf23df', NOW(), NULL, 'system'),
('john.doe@aglet.co.za', '$2y$10$YourHashedPasswordHere', '+27 12 345 6789', 'John Doe', 1, 0, '34b71731-e4fe-4383-9904-9e370b2ece72', NOW(), NULL, 'system'),
('jane.smith@aglet.co.za', '$2y$10$YourHashedPasswordHere', '+27 21 456 7890', 'Jane Smith', 1, 0, 'cda10113-023b-4cfb-87c7-9d27ac083cdf', NOW(), NULL, 'system'),
('mike.wilson@aglet.co.za', '$2y$10$YourHashedPasswordHere', '+27 31 567 8901', 'Mike Wilson', 1, 0, '5ccf33e3-c920-4f1d-b2da-2c0f3f1db2d7', NOW(), NULL, 'system'),
('sarah.jones@aglet.co.za', '$2y$10$YourHashedPasswordHere', '+27 41 678 9012', 'Sarah Jones', 0, 0, '1e9fcf7b-b3eb-41bc-904c-1d2a405a9677', NOW(), NULL, 'system'),
('inactive.user@aglet.co.za', '$2y$10$YourHashedPasswordHere', '+27 51 789 0123', 'Inactive User', 0, 0, 'ac74a95c-2886-487e-8c3f-86accc14f9a0', NOW(), NULL, 'system');

INSERT INTO `permissions` (`name`, `description`, `is_active`, `is_deleted`, `edited_by`) VALUES
('view_users', 'View user information and profiles', 1, 0, 'system'),
('create_users', 'Create new user accounts', 1, 0, 'system'),
('edit_users', 'Edit existing user information', 1, 0, 'system'),
('delete_users', 'Delete user accounts', 1, 0, 'system'),
('view_roles', 'View role definitions', 1, 0, 'system'),
('create_roles', 'Create new roles', 1, 0, 'system'),
('edit_roles', 'Edit existing roles', 1, 0, 'system'),
('delete_roles', 'Delete roles', 1, 0, 'system'),
('assign_roles', 'Assign roles to users', 1, 0, 'system'),
('view_permissions', 'View permission definitions', 1, 0, 'system'),
('edit_permissions', 'Edit permission definitions', 1, 0, 'system'),
('view_languages', 'View language entries', 1, 0, 'system'),
('create_languages', 'Create new language entries', 1, 0, 'system'),
('edit_languages', 'Edit existing language entries', 1, 0, 'system'),
('delete_languages', 'Delete language entries', 1, 0, 'system'),
('view_contact_submissions', 'View contact form submissions', 1, 0, 'system'),
('action_contact_submissions', 'Mark contact submissions as actioned', 1, 0, 'system'),
('delete_contact_submissions', 'Delete contact form submissions', 1, 0, 'system'),
('system_config', 'Configure system settings', 1, 0, 'system'),
('view_audit_logs', 'View system audit logs', 1, 0, 'system');

INSERT INTO `roles` (`name`, `description`, `is_active`, `is_admin`, `is_deleted`, `edited_by`) VALUES
('Super Admin', 'Full system access with all permissions and administrative capabilities', 1, 1, 0, 'system'),
('Admin', 'Administrative access with most permissions except system configuration', 1, 1, 0, 'system'),
('Content Manager', 'Manages language content and can view contact submissions', 1, 0, 0, 'system'),
('User Manager', 'Manages user accounts and role assignments', 1, 0, 0, 'system'),
('Viewer', 'Read-only access to view information', 1, 0, 0, 'system'),
('Support Agent', 'Can view and action contact submissions', 1, 0, 0, 'system');

INSERT INTO `role_permissions` (`role_id`, `permission_id`, `is_active`, `is_deleted`, `edited_by`)
SELECT 
    (SELECT id FROM roles WHERE name = 'Super Admin'),
    id,
    1, 0, 'system'
FROM permissions 
WHERE is_active = 1;

INSERT INTO `role_permissions` (`role_id`, `permission_id`, `is_active`, `is_deleted`, `edited_by`)
SELECT 
    (SELECT id FROM roles WHERE name = 'Admin'),
    id,
    1, 0, 'system'
FROM permissions 
WHERE name NOT IN ('system_config', 'delete_users');

INSERT INTO `role_permissions` (`role_id`, `permission_id`, `is_active`, `is_deleted`, `edited_by`)
SELECT 
    (SELECT id FROM roles WHERE name = 'Content Manager'),
    id,
    1, 0, 'system'
FROM permissions 
WHERE name IN ('view_languages', 'create_languages', 'edit_languages', 'delete_languages', 'view_contact_submissions');

INSERT INTO `role_permissions` (`role_id`, `permission_id`, `is_active`, `is_deleted`, `edited_by`)
SELECT 
    (SELECT id FROM roles WHERE name = 'User Manager'),
    id,
    1, 0, 'system'
FROM permissions 
WHERE name IN ('view_users', 'create_users', 'edit_users', 'view_roles', 'assign_roles');

INSERT INTO `role_permissions` (`role_id`, `permission_id`, `is_active`, `is_deleted`, `edited_by`)
SELECT 
    (SELECT id FROM roles WHERE name = 'Viewer'),
    id,
    1, 0, 'system'
FROM permissions 
WHERE name IN ('view_languages', 'view_users', 'view_roles', 'view_permissions');

INSERT INTO `role_permissions` (`role_id`, `permission_id`, `is_active`, `is_deleted`, `edited_by`)
SELECT 
    (SELECT id FROM roles WHERE name = 'Support Agent'),
    id,
    1, 0, 'system'
FROM permissions 
WHERE name IN ('view_contact_submissions', 'action_contact_submissions', 'view_users');

INSERT INTO `user_roles` (`user_id`, `role_id`, `is_active`, `is_deleted`, `edited_by`) VALUES
((SELECT id FROM users WHERE email = 'jointheteam@aglet.co.za'), (SELECT id FROM roles WHERE name = 'Super Admin'), 1, 0, 'system'),
((SELECT id FROM users WHERE email = 'admin@aglet.co.za'), (SELECT id FROM roles WHERE name = 'Admin'), 1, 0, 'system'),
((SELECT id FROM users WHERE email = 'john.doe@aglet.co.za'), (SELECT id FROM roles WHERE name = 'Content Manager'), 1, 0, 'system'),
((SELECT id FROM users WHERE email = 'john.doe@aglet.co.za'), (SELECT id FROM roles WHERE name = 'Viewer'), 1, 0, 'system'),
((SELECT id FROM users WHERE email = 'jane.smith@aglet.co.za'), (SELECT id FROM roles WHERE name = 'User Manager'), 1, 0, 'system'),
((SELECT id FROM users WHERE email = 'mike.wilson@aglet.co.za'), (SELECT id FROM roles WHERE name = 'Support Agent'), 1, 0, 'system'),
((SELECT id FROM users WHERE email = 'sarah.jones@aglet.co.za'), (SELECT id FROM roles WHERE name = 'Viewer'), 1, 0, 'system');

INSERT INTO `contactus` (`name`, `email`, `phone_number`, `company_name`, `message`, `is_actioned`, `created_at`, `edited_by`) VALUES
('Peter Williams', 'peter.williams@techcorp.co.za', '+27 82 123 4567', 'TechCorp SA', 'I am interested in learning more about your language learning platform. We have a team of 15 people who would like to improve their business English skills. Can you provide information about corporate rates?', 0, DATE_SUB(NOW(), INTERVAL 5 DAY), 'system'),
('Linda Nkosi', 'linda.nkosi@edusolutions.co.za', '+27 83 234 5678', 'EduSolutions Africa', 'We are looking for a language training partner for our school. We need programs for isiZulu and English for our students. Please send me your brochure and pricing information.', 1, DATE_SUB(NOW(), INTERVAL 12 DAY), 'system'),
('Thabo Mbeki', 'thabo.m@globalconnect.com', '+27 84 345 6789', 'Global Connect', 'I would like to book a consultation to discuss language translation services for our upcoming international conference. We need interpreters for English, French, and Portuguese.', 0, DATE_SUB(NOW(), INTERVAL 2 DAY), 'system'),
('Sarah van der Merwe', 'sarah.vdm@afrilang.co.za', '+27 81 456 7890', 'AfriLang Institute', 'We are interested in partnering with your platform to offer Afrikaans and isiXhosa courses to our students. Please contact me to discuss partnership opportunities.', 0, DATE_SUB(NOW(), INTERVAL 1 DAY), 'system'),
('David Naidoo', 'david.n@durbanimports.com', '+27 72 567 8901', 'Durban Imports', 'We have several employees who need to learn Mandarin Chinese for business trips to China. Do you offer intensive courses? Please send information.', 1, DATE_SUB(NOW(), INTERVAL 8 DAY), 'system'),
('Grace Mahlangu', 'grace.m@joburgtech.co.za', '+27 73 678 9012', 'Joburg Tech Hub', 'I am an individual learner interested in learning Spanish. I saw your platform online and would like to know if you offer one-on-one tutoring sessions.', 0, NOW(), 'system'),
('Robert du Plessis', 'robert.dp@capewinery.co.za', '+27 74 789 0123', 'Cape Winery Estates', 'We host many international visitors and need our staff to improve their English and learn basic German and French. Can you provide a quote for group training?', 0, DATE_SUB(NOW(), INTERVAL 3 DAY), 'system');