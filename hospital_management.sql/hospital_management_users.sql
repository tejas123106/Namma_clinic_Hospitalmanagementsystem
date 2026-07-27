-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hospital_management
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','Doctor','Receptionist','Accountant') NOT NULL,
  `phone` varchar(15) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'System Administrator','admin','admin@hospital.com','scrypt:32768:8:1$h9JCqkZyJqD2rZ8B$81cdb7f90afe66d0f2381261d17802006d6eeb1294b693d77e155793b8e0c50fed939109e16f97b39517e3547b00e4c3e3d1c273d7346331e357b11b1da5ae7c','Admin','9876543210',1,'2026-07-26 12:07:45'),(2,'Dr. Ravi Kumar','dr_ravi','ravi@hospital.com','scrypt:32768:8:1$WTyb5tOr2NPmzzQh$3e09a566c621399efc801a466df63eebf36451ca019cf00337d25b0c22410cd1d0e1889b830a7379ebd12bf65a7445973bbc356eb87d81d3057c337c8e71ab17','Doctor','9876500001',1,'2026-07-26 12:07:45'),(3,'Anjali Sharma','reception1','anjali@hospital.com','scrypt:32768:8:1$65KzG7Hfr7xC5QyD$a6b1887bcc8a83770fb83c57684b08328d326d94b82f6c8e9cee56a3877a142753c10e921f086c911061fe8a1600add125561e4b8e70db879583cec9a66ee4db','Receptionist','9876500002',1,'2026-07-26 12:07:45'),(4,'Kiran Rao','account1','kiran@hospital.com','scrypt:32768:8:1$cEBHmEzgkMJVn5oU$70022acf111899f20fc0091fb913e1314d6aa892321c9ee7f8ff9f44b1e6600e9548b437ff0d8562547c44eaa1a2e5348d91264bb0632a9a6564a0c07f375caf','Accountant','9876500003',1,'2026-07-26 12:07:45');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-27 23:57:20
