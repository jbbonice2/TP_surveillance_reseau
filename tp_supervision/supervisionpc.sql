-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : jeu. 20 juin 2024 à 15:26
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `supervisionpc`
--

-- --------------------------------------------------------

--
-- Structure de la table `Donnees`
--

CREATE TABLE `Donnees` (
  `id` int(11) NOT NULL,
  `machine_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `used_memory` bigint(20) DEFAULT NULL,
  `memory_percentage` float DEFAULT NULL,
  `cached_memory` bigint(20) DEFAULT NULL,
  `swap_total` bigint(20) DEFAULT NULL,
  `swap_used` bigint(20) DEFAULT NULL,
  `swap_percentage` float DEFAULT NULL,
  `used_disk` bigint(20) DEFAULT NULL,
  `disk_percentage` float DEFAULT NULL,
  `cpu_load_per_core` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`cpu_load_per_core`)),
  `net_bytes_sent` bigint(20) DEFAULT NULL,
  `net_bytes_recv` bigint(20) DEFAULT NULL,
  `active_processes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`active_processes`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Machine`
--

CREATE TABLE `Machine` (
  `id` int(11) NOT NULL,
  `machine_type` varchar(50) DEFAULT NULL,
  `mac_address` varchar(17) DEFAULT NULL,
  `system` varchar(50) DEFAULT NULL,
  `node_name` varchar(100) DEFAULT NULL,
  `machine_architecture` varchar(20) DEFAULT NULL,
  `processor` varchar(100) DEFAULT NULL,
  `cores` int(11) DEFAULT NULL,
  `logical_cores` int(11) DEFAULT NULL,
  `cpu_frequency` float DEFAULT NULL,
  `total_memory` bigint(20) DEFAULT NULL,
  `total_disk` bigint(20) DEFAULT NULL,
  `version` varchar(100) NOT NULL,
  `releases` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Machine`
--

INSERT INTO `Machine` (`id`, `machine_type`, `mac_address`, `system`, `node_name`, `machine_architecture`, `processor`, `cores`, `logical_cores`, `cpu_frequency`, `total_memory`, `total_disk`, `version`, `releases`) VALUES
(1, 'Unknown', 'ed:d8:b9:ca:93:3f', 'Linux', 'bonice-Latitude-E6430', 'x86_64', 'x86_64', 2, 4, 3300, 6110388224, 158992801792, '#112~20.04.1-Ubuntu SMP Thu Mar 14 14:28:24 UTC 2024', '5.15.0-102-generic');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `prenom` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `nom`, `prenom`, `email`, `password`) VALUES
(1, 'James', 'bonice', 'bonicetok904@gmail.com', 'bonjour');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Donnees`
--
ALTER TABLE `Donnees`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Machine`
--
ALTER TABLE `Machine`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mac_address` (`mac_address`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Donnees`
--
ALTER TABLE `Donnees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Machine`
--
ALTER TABLE `Machine`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
