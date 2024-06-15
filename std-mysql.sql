-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: std-mysql
-- Время создания: Июн 16 2024 г., 07:52
-- Версия сервера: 5.7.26-0ubuntu0.16.04.1
-- Версия PHP: 8.1.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `std_2453_parinovadiana_exam`
--
CREATE DATABASE IF NOT EXISTS `std_2453_parinovadiana_exam` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `std_2453_parinovadiana_exam`;

-- --------------------------------------------------------

--
-- Структура таблицы `book`
--

CREATE TABLE `book` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `publisher_year` int(11) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `short_desc` text NOT NULL,
  `author` varchar(255) NOT NULL,
  `size` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `book`
--

INSERT INTO `book` (`id`, `name`, `publisher_year`, `publisher`, `short_desc`, `author`, `size`) VALUES
(48, '451° по Фаренгейту', 2008, 'АТС', 'Мастер мирового масштаба, совмещающий в литературе несовместимое. Создатель таких ярчайших шедевров, как \"Марсианские хроники\", \"451° по Фаренгейту\", \"Вино из одуванчиков\" и так далее и так далее. Лауреат многочисленных премий. Это Рэй Брэдбери. Его увлекательные истории прославили автора не только как непревзойденного рассказчика, но и как философа, мыслителя и психолога.', 'Рэй Брэдбери', 321),
(49, 'Мастер и Маргарита', 2006, 'Триумф', 'Один из самых загадочных и удивительных романов XX века. «Мастер и Маргарита» – визитная карточка Михаила Булгакова. Более десяти лет он работал над книгой, которая стала его романом-судьбой, романом-завещанием. В «Мастере и Маргарите» есть всё: весёлое озорство и щемящая печаль, романтическая любовь и колдовское наваждение, магическая тайна и безрассудная игра с нечистой силой.', 'Михаил Булгаков', 254),
(50, 'Три товарища', 2000, 'Росмэн', 'Трое друзей - Робби, отчаянный автогонщик Кестер и \"последний романтик\" Ленц прошли Первую мировую войну. Вернувшись в гражданскую жизнь, они основали небольшую автомастерскую. И хотя призраки прошлого преследуют их, они не унывают - ведь что может быть лучше дружбы, крепкой и верной, ради которой можно отдать последнее?', 'Эрих Мария Ремарк', 174),
(51, 'Цветы для Элджернона', 2012, 'Эксмо', 'Сорок лет назад это считалось фантастикой. Сорок лет назад это читалось как фантастика. Исследующая и расширяющая границы жанра, жадно впитывающая всевозможные новейшие веяния, примеряющая общечеловеческое лицо, отважно игнорирующая каинову печать \"жанрового гетто\".', 'Дэниел Киз', 189),
(52, 'Портрет Дориана Грея', 1980, 'Издательство АСТ', '«Портрет Дориана Грея» – одно из величайших произведений последних полутора столетий, роман, который пытались запретить, а автора осуждали за «непристойное поведение». Превращение прекрасного и невинного юноши Дориана в чудовище под влиянием гедонистических идей и циничных афоризмов лорда Генри – в романе, породившем культ вечной молодости.', 'Оскар Уайльд', 245),
(53, 'Преступление и наказание', 2008, 'Public Domain', 'Ф.М.Достоевский - один из тех немногих писателей, которые повлияли на умы не только современников, но и потомков. В своем творчестве он ставит самые главные, самые трудные - непосильные - вопросы. Роман \"Преступление и наказание\" - детектив со всеми необходимыми атрибутами: \"хождение по мукам\" нищего студента Родиона Раскольникова, убийство старухи-процентщицы, последовавшее за ним расследование, наказание и, конечно же, любовь... Но не этим прежде всего он привлекает читателя.', 'Фёдор Достоевский', 265),
(54, 'Сто лет одиночества', 2007, 'Издательство АСТ', 'Странная, поэтичная, причудливая история города Макондо, затерянного где-то в джунглях, - от сотворения до упадка. История рода Буэндиа - семьи, в которой чудеса столь повседневны, что на них даже не обращают внимания. Клан Буэндиа порождает святых и грешников, революционеров, героев и предателей, лихих авантюристов - и женщин, слишком прекрасных для обычной жизни.', 'Габриэль Гарсиа Маркес', 314),
(55, 'Граф Монте-Кристо', 2009, 'Public Domain', '\"Граф Монте-Кристо\"- книга, которую вот уже полтора столетия с увлечением читают и взрослые, и дети. Это история о том, как невинно осужденный моряк стал сказочно богатым графом и о том, как он вознаградил своих верных друзей и отомстил врагам.', 'Александр Дюма', 243),
(56, 'Евгений Онегин', 1999, 'Public Domain', '«Евгений Онегин» — роман в стихах Александра Сергеевича Пушкина, написанный в 1823—1831 годах, одно из самых значительных произведений русской словесности. Пушкин работал над этим романом свыше семи лет. На широком фоне картин русской жизни показана драматическая судьба лучших людей дворянской интеллигенции. В центре романа — любовная интрига. А главной проблемой является вечная проблема чувства и долга.', 'Александр Пушкин', 278),
(57, 'Гордость и предубеждение', 2012, 'Эксмо', 'Широко известный роман Д.Остен. Англия, конец XVIII века. Родители пятерых сестер Беннет озабочены тем, чтобы удачно выдать дочерей замуж. И потому размеренная жизнь солидного семейства переворачивается вверх дном, когда по соседству появляется молодой джентльмен — мистер Бингли… Само собой, среди друзей нового соседа оказывается немало утонченных аристократов, которые не прочь поухаживать за очаровательными сестрами.', 'Джейн Остин', 321),
(58, 'Герой нашего времени', 2012, 'Public Domain', '«Герой нашего времени» (написан в 1838—1840) — знаменитый роман Михаила Юрьевича Лермонтова, классика русской литературы. Роман состоит из нескольких частей, хронологический порядок которых нарушен. Образ Печорина — одно из художественных открытий Лермонтова. Печоринский тип поистине эпохален, и прежде всего потому, что в нем получили концентрированное выражение особенности последекабристской эпохи, когда на поверхности «видны были только потери, жестокая реакция», внутри же «совершалась великая работа… глухая и безмолвная, но деятельная и беспрерывная …»', 'Михаил Лермонтов', 273);

-- --------------------------------------------------------

--
-- Структура таблицы `books_category`
--

CREATE TABLE `books_category` (
  `id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `books_category`
--

INSERT INTO `books_category` (`id`, `book_id`, `category_id`) VALUES
(90, 48, 3),
(91, 48, 6),
(92, 49, 1),
(93, 49, 8),
(94, 50, 3),
(95, 51, 1),
(96, 51, 6),
(97, 52, 1),
(98, 52, 6),
(99, 53, 1),
(100, 53, 8),
(101, 54, 1),
(102, 55, 1),
(103, 56, 2),
(104, 56, 6),
(105, 57, 1),
(106, 57, 6),
(107, 58, 1),
(108, 58, 3);

-- --------------------------------------------------------

--
-- Структура таблицы `books_collection`
--

CREATE TABLE `books_collection` (
  `id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `collection_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `category`
--

INSERT INTO `category` (`id`, `name`) VALUES
(1, 'Роман'),
(2, 'Поэма'),
(3, 'Повесть'),
(4, 'Эпопея'),
(5, 'Трагедия'),
(6, 'Драма'),
(7, 'Комедия'),
(8, 'Хоррор ');

-- --------------------------------------------------------

--
-- Структура таблицы `collection`
--

CREATE TABLE `collection` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `cover`
--

CREATE TABLE `cover` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  `book_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `cover`
--

INSERT INTO `cover` (`id`, `file_name`, `mime_type`, `md5_hash`, `book_id`) VALUES
('0a316270-b351-4d73-b62c-8bd1deee72e6', 'jpg', 'image/jpeg', 'c4eb99b4935dfd8ea3f4809ba6cb97dc', 54),
('0cd481b9-3d3f-4617-b5f4-171dd3470134', 'jpg', 'image/jpeg', '7d7da27016e2f040f0c6bf583995b71e', 55),
('0e81cdec-3448-46c1-87ee-c7a7c70a5061', 'jpg', 'image/jpeg', '8715befc9b05ac9b1608f02dc67bbbb5', 52),
('10a320e6-2152-4ff6-baf1-1c84e3027a12', 'jpg', 'image/jpeg', 'ed73fcef0a92a03042cdc86539b198ee', 49),
('61ef2f6c-646a-4797-ba43-94de8a70845e', 'jpg', 'image/jpeg', '697aa007b5e1e7c630f0c601020742f8', 48),
('7137f2f8-97e4-4699-9749-d5b817a04051', 'jpg', 'image/jpeg', 'e7bd0260e07ded4640d302bd3446935a', 56),
('79cb4c81-c93a-43ec-bc8d-442aa4161e5d', 'jpg', 'image/jpeg', 'fd7ffcde92191b57ada550a8ab594fb5', 58),
('853db8be-28e3-4820-a981-dba885ca57f8', 'jpg', 'image/jpeg', 'b8d1f73c41843a858a6b4fa9add7154b', 53),
('a699f726-0d43-4ed9-8716-e6eaacca832a', 'jpg', 'image/jpeg', 'ec1747b5f38af94495f4214f4adc2942', 57),
('ed8c537b-f3f5-4843-a6c3-4743bcc4194d', 'jpg', 'image/jpeg', 'ac6efab23bb70dc320d2053145b7b536', 50),
('fdcb5184-0263-4097-b6f4-ad11f9490af7', 'jpg', 'image/jpeg', '84812adf295826fe332257287777da7b', 51);

-- --------------------------------------------------------

--
-- Структура таблицы `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `review`
--

INSERT INTO `review` (`id`, `book_id`, `user_id`, `rating`, `text`, `created_at`) VALUES
(37, 48, 2, 5, 'Горящий хит!', '2024-06-16 09:58:16'),
(38, 52, 2, 5, 'Нестареющая классика ', '2024-06-16 09:58:16'),
(39, 54, 2, 4, 'муд', '2024-06-16 09:58:16'),
(40, 51, 2, 3, 'Ну хоть кому-то цветы дарят', '2024-06-16 09:58:16'),
(41, 49, 3, 5, 'Может тоже на патриарши сходить ', '2024-06-16 09:58:16'),
(42, 48, 3, 2, 'Или 233 градуса по Цельсию ', '2024-06-16 09:58:16');

-- --------------------------------------------------------

--
-- Структура таблицы `role`
--

CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `role`
--

INSERT INTO `role` (`id`, `name`, `description`) VALUES
(1, 'admin', 'суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),
(2, 'moderator', 'может редактировать данные книг'),
(3, 'user', 'может оставлять рецензии');

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `user`
--

INSERT INTO `user` (`id`, `first_name`, `last_name`, `middle_name`, `login`, `password_hash`, `role_id`) VALUES
(1, 'admin', 'admin', 'admin', 'admin', 'scrypt:32768:8:1$SeX5GqFG9J6WswaZ$dd3cbe9f404acceb5d359e7d7807652a6f2a5ad4fc4ad58bf72abc25555df8d98462106f858be1cedaae41d387b7136c374a826cedaa179fa8936bcb4a1f6ae7', 1),
(2, 'moderator', 'moderator', 'moderator', 'moder', 'scrypt:32768:8:1$SeX5GqFG9J6WswaZ$dd3cbe9f404acceb5d359e7d7807652a6f2a5ad4fc4ad58bf72abc25555df8d98462106f858be1cedaae41d387b7136c374a826cedaa179fa8936bcb4a1f6ae7', 2),
(3, 'user', 'user', 'user', 'user', 'scrypt:32768:8:1$SeX5GqFG9J6WswaZ$dd3cbe9f404acceb5d359e7d7807652a6f2a5ad4fc4ad58bf72abc25555df8d98462106f858be1cedaae41d387b7136c374a826cedaa179fa8936bcb4a1f6ae7', 3);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `books_category`
--
ALTER TABLE `books_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Индексы таблицы `books_collection`
--
ALTER TABLE `books_collection`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `collection_id` (`collection_id`);

--
-- Индексы таблицы `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `collection`
--
ALTER TABLE `collection`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `cover`
--
ALTER TABLE `cover`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `md5_hash` (`md5_hash`),
  ADD KEY `book_id` (`book_id`);

--
-- Индексы таблицы `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `book`
--
ALTER TABLE `book`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT для таблицы `books_category`
--
ALTER TABLE `books_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=109;

--
-- AUTO_INCREMENT для таблицы `books_collection`
--
ALTER TABLE `books_collection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT для таблицы `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT для таблицы `collection`
--
ALTER TABLE `collection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT для таблицы `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT для таблицы `role`
--
ALTER TABLE `role`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `books_category`
--
ALTER TABLE `books_category`
  ADD CONSTRAINT `books_category_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  ADD CONSTRAINT `books_category_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`);

--
-- Ограничения внешнего ключа таблицы `books_collection`
--
ALTER TABLE `books_collection`
  ADD CONSTRAINT `books_collection_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  ADD CONSTRAINT `books_collection_ibfk_2` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`id`);

--
-- Ограничения внешнего ключа таблицы `collection`
--
ALTER TABLE `collection`
  ADD CONSTRAINT `collection_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ограничения внешнего ключа таблицы `cover`
--
ALTER TABLE `cover`
  ADD CONSTRAINT `cover_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`);

--
-- Ограничения внешнего ключа таблицы `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ограничения внешнего ключа таблицы `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
