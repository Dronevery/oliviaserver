# Olivia Server

## Introduction

Olivia Server 是整个Olivia项目的核心，其目的是一套兼容的，用于控制／指挥多种飞行器的系统

Olivia Server 将用于东北航校和本实验室自己的无人机项目。

## 设计
Olivia Server使用Python写成。

使用的框架包括Twisted与Tornado

前者负责大量的通信，后者负责一个简易的控制台

## 由飞行器传入信息

Olivia Server 接收数据类型很多，但是这部分的处理工作并不由主程序来完成，主程序只负责每次

## 与Client通信

使用Socket通信，选用1026端口（妹子生日）

