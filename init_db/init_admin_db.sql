CREATE DATABASE IF NOT EXISTS `kea_cars_admin_dev` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `kea_cars_admin_dev`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: kea-cars.mysql.database.azure.com    Database: kea_cars_admin_dev
-- ------------------------------------------------------
-- Server version	8.0.37-azure

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `id` char(36) DEFAULT (UUID()) NOT NULL,
  `email` varchar(100) NOT NULL,
  `hashed_password` varchar(130) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `role` ENUM('admin', 'manager', 'sales_person') DEFAULT 'sales_person' NOT NULL,
  `is_deleted` BOOLEAN DEFAULT FALSE NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP() NOT NULL,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP() NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_email_UNIQUE` (`email`),
  KEY `idx_is_deleted` (`is_deleted`),
  CONSTRAINT `check_role` CHECK (`role` IN ('admin', 'manager', 'sales_person'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES 
('d096d2e1-f06a-4555-9cd1-afa9f930f10c','james@gmail.com','$2b$10$sB6/ocJJK9HodVv7qEozKO826Ik5gmZH/1GU/xReM1ijIjlA7hvTa','James','Jamesen','sales_person',FALSE,'2025-03-26T03:53:58', '2025-03-26T03:53:58'),
('f9097a97-eca4-49b6-85a0-08423789c320','hans@gmail.com','$2b$12$BKrnHSqhmb8NsKnUhhSGWeOj0Pnyx0so0xeXlUrDrNLplk2VnjDyK','Hans','Hansen','manager',FALSE,'2025-03-26T03:53:58', '2025-03-26T03:53:58'),
('24bd8a11-2310-46bc-aebf-0887325ebdbd','tom@gmail.com','$2b$12$O8wDPpEJYPorIgSR5F/QTO2l277gsYPOcvxc/nKUHyggBh374mcyW','Tom','Tomsen','admin',FALSE,'2025-03-26T03:53:58', '2025-03-26T03:53:58');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;


-- Drop the application user if the user exists
DROP USER IF EXISTS 'application_user'@'%';

-- Create the application user
CREATE USER 'application_user'@'%' IDENTIFIED BY 'supersecretpassword';

-- Grant privileges for the application user at the table level
GRANT SELECT, INSERT, UPDATE ON `kea_cars_admin_dev`.`employees` TO 'application_user'@'%';

-- Apply the granted privileges
FLUSH PRIVILEGES;