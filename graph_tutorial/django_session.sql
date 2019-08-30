/*
Navicat SQLite Data Transfer

Source Server         : sqlite
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2019-08-06 11:36:03
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_session";
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "main"."django_session_expire_date_a5c62663"
ON "django_session" ("expire_date" ASC);
