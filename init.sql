CREATE DATABASE IF NOT EXISTS `records`;

USE `records`;

CREATE TABLE IF NOT EXISTS `certifications` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `personid` varchar(12)  DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  `first` varchar(50) DEFAULT NULL,
  `second` varchar(50) DEFAULT NULL,
  `third` varchar(50) DEFAULT NULL,
  `fourth` varchar(50) DEFAULT NULL,
  `comment` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 ;
