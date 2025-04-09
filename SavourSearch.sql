-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: savoursearch
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `ingredients_nutrition`
--

DROP TABLE IF EXISTS `ingredients_nutrition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients_nutrition` (
  `Ingredient` varchar(255) DEFAULT NULL,
  `Calories_kcal` int DEFAULT NULL,
  `Protein_g` float DEFAULT NULL,
  `Fat_g` float DEFAULT NULL,
  `Carbohydrates_g` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients_nutrition`
--

LOCK TABLES `ingredients_nutrition` WRITE;
/*!40000 ALTER TABLE `ingredients_nutrition` DISABLE KEYS */;
INSERT INTO `ingredients_nutrition` VALUES ('Chicken breast',165,31,3.6,0),('Salmon',208,20,13,0),('Rice',130,2.7,0.3,28),('Broccoli',55,3.7,0.6,11),('Almonds',579,21,50,22),('Milk',42,3.4,1,5),('Eggs',155,13,11,1.1),('Avocado',160,2,15,9),('Banana',89,1.1,0.3,23),('Sweet potato',86,1.6,0.1,20),('Spinach',23,2.9,0.4,3.6),('Beef (lean)',250,26,17,0),('Tofu',144,15,8,3.9),('Lentils',116,9,0.4,20),('Cheese (cheddar)',402,25,33,1.3),('Yogurt (plain)',59,10,0.4,3.6),('Olive oil',884,0,100,0),('Oats',389,17,6.9,66),('Peanut butter',588,25,50,20),('Carrot',41,0.9,0.2,10);
/*!40000 ALTER TABLE `ingredients_nutrition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipes_nutrition`
--

DROP TABLE IF EXISTS `recipes_nutrition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipes_nutrition` (
  `Recipe_Name` varchar(255) DEFAULT NULL,
  `Main_Ingredients` text,
  `Calories_per_serving` int DEFAULT NULL,
  `Protein_g` float DEFAULT NULL,
  `Fat_g` float DEFAULT NULL,
  `Carbohydrates_g` float DEFAULT NULL,
  `Flavor_Profile` varchar(50) DEFAULT NULL,
  `Allergy_Info` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes_nutrition`
--

LOCK TABLES `recipes_nutrition` WRITE;
/*!40000 ALTER TABLE `recipes_nutrition` DISABLE KEYS */;
INSERT INTO `recipes_nutrition` VALUES ('Grilled Chicken Salad','Chicken breast, lettuce, tomato, cucumber',350,40,10,15,'Savory','None'),('Spaghetti Bolognese','Spaghetti, ground beef, tomato sauce',600,30,18,75,'Savory','Gluten'),('Avocado Toast','Bread, avocado, egg',320,10,18,30,'Savory','Gluten'),('Chicken Stir-fry','Chicken, bell peppers, soy sauce, rice',450,35,12,50,'Savory','Soy'),('Beef Tacos','Tortilla, ground beef, cheese, lettuce',500,28,22,45,'Savory','Gluten, Dairy'),('Vegetable Soup','Carrots, potatoes, celery, broth',200,6,2,35,'Savory','None'),('Scrambled Eggs with Spinach','Eggs, spinach, butter',250,20,18,5,'Savory','Dairy'),('Banana Smoothie','Banana, milk, yogurt, honey',300,8,5,60,'Sweet','Dairy'),('Baked Salmon with Asparagus','Salmon, asparagus, olive oil',450,40,25,10,'Savory','None'),('Lentil Soup','Lentils, carrots, onion, broth',350,22,5,50,'Savory','None'),('Oatmeal with Peanut Butter','Oats, peanut butter, honey',400,15,18,55,'Sweet','Nuts, Gluten'),('Greek Yogurt with Berries','Greek yogurt, berries, honey',250,15,5,30,'Sweet','Dairy'),('Sweet Potato Hash','Sweet potato, eggs, onion',300,12,10,45,'Savory','None'),('Quinoa and Chickpea Salad','Quinoa, chickpeas, tomato, cucumber',400,18,12,50,'Savory','None'),('Grilled Cheese Sandwich','Bread, cheese, butter',450,15,25,40,'Savory','Gluten, Dairy'),('Almond Butter Energy Balls','Almond butter, oats, honey',350,10,20,40,'Sweet','Nuts'),('Roasted Carrots with Honey','Carrots, honey, olive oil',200,2,8,30,'Sweet','None'),('Classic Pancakes','Flour, milk, eggs, sugar',450,12,15,60,'Sweet','Gluten, Dairy'),('Chicken and Rice Bowl','Chicken, rice, broccoli',500,45,10,55,'Savory','None'),('Tuna Salad','Tuna, lettuce, mayo, cucumber',350,30,15,10,'Savory','None');
/*!40000 ALTER TABLE `recipes_nutrition` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-09 12:57:29
