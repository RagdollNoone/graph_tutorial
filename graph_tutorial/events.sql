/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50727
Source Host           : localhost:3306
Source Database       : meeting

Target Server Type    : MYSQL
Target Server Version : 50727
File Encoding         : 65001

Date: 2019-08-06 10:54:42
*/
use meeting;
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for events
-- ----------------------------
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Subject` varchar(255) DEFAULT NULL,
  `Organizer` varchar(255) DEFAULT NULL,
  `Start` datetime DEFAULT NULL,
  `Attendees` varchar(255) DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `1233` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
