# Проект интернет-магазина
## Проект еще находится в разработке

В рамках данного проекта реализован интернет магазин, в котором можно просматривать список всех товар(страница "Главная), просматривать список категорий товаров и товаров, входящих в эти категории,  более подробную информацию по конкретному товару; реализована возможности добавление, редактирования и удаления товаров, а также добавление актуальных версий.
Присутствует часть "Блог", где публикуются новости магазина, записи блога доступны для редактирования и удаления.

Пользователь может заргестрироваться, пройдя верефикацию через почту, затем залогиниться на сайте и после этого у ему становится доступна возможность добавлять свои товары.

В проекте присутствует функционал рассылок, которые отправляются с определенной периодичностью клиенам, которые входят в то или иную рассылку.
Рассылки, клиентов и сообщения может добавлять только зарегестрированный пользователь, который в дальнейшем может управлять только своими рассылками, клиентами, сообщениями.

Пользователь, который входит в группу Manager:
- может просматривать любые рассылки
- может просматривать список пользователей сервиса
- может блокировать пользователей сервиса
- может отключать рассылки
- не может редактировать рассылки
- не может управлять списком рассылок
- не может изменять рассылки и сообщения

Добавлена часть блога для рассылок, три рандомные блоговые записи выводятся на главную страницу рассылок. Управляет блоговыми записями пользователь, входящий в группу ContentManager.

В проекте использовано низкоуровневое кеширование и кеширование контроллера

