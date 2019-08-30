/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50727
Source Host           : localhost:3306
Source Database       : meeting

Target Server Type    : MYSQL
Target Server Version : 50727
File Encoding         : 65001

Date: 2019-08-06 15:44:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for attendees
-- ----------------------------
DROP TABLE IF EXISTS `attendees`;
CREATE TABLE `attendees` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `eventid` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
