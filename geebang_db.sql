-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : lun. 10 jan. 2022 à 16:29
-- Version du serveur : 10.4.21-MariaDB
-- Version de PHP : 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `geebang_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `admin_db`
--

CREATE TABLE `admin_db` (
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `motdepasse` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `admin_db`
--

INSERT INTO `admin_db` (`nom`, `prenom`, `mail`, `motdepasse`) VALUES
('Gaultier', 'Melissa', 'melissa@geebang.com', 'melissageebang');

-- --------------------------------------------------------

--
-- Structure de la table `promotions_db`
--

CREATE TABLE `promotions_db` (
  `id_promo` int(11) NOT NULL,
  `restaurant` varchar(100) DEFAULT NULL,
  `points_necessaires` int(11) NOT NULL,
  `description` text NOT NULL,
  `nb_scan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `promotions_db`
--

INSERT INTO `promotions_db` (`id_promo`, `restaurant`, `points_necessaires`, `description`, `nb_scan`) VALUES
(1, 'Burger King', 50, 'Menu Maxi Best-of Offert', 0),
(2, 'Burger King', 40, 'Best of Offert', 0),
(8, 'Burger King', 15, 'Fites Bacon', 0),
(9, 'Burger King', 15, 'burger', 0);

-- --------------------------------------------------------

--
-- Structure de la table `restaurants_db`
--

CREATE TABLE `restaurants_db` (
  `restaurant` varchar(100) NOT NULL,
  `code_restau` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `restaurants_db`
--

INSERT INTO `restaurants_db` (`restaurant`, `code_restau`) VALUES
('Burger King', 'QSDFGHJKLM');

-- --------------------------------------------------------

--
-- Structure de la table `restaurateurs_db`
--

CREATE TABLE `restaurateurs_db` (
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `mail` varchar(100) NOT NULL,
  `motdepasse` varchar(100) NOT NULL,
  `nom_restau` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `restaurateurs_db`
--

INSERT INTO `restaurateurs_db` (`nom`, `prenom`, `mail`, `motdepasse`, `nom_restau`) VALUES
('Dupont', 'Sandrine', 'sandrine@bk.fr', '$2b$12$4oGeLx65IO0syUQQyAUeBOXqdZ2CXvwcKbDDN5nVHfAhfJ6b.Uqi6', 'Burger King');

-- --------------------------------------------------------

--
-- Structure de la table `users_db`
--

CREATE TABLE `users_db` (
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  `mail` varchar(50) NOT NULL,
  `motdepasse` varchar(100) DEFAULT NULL,
  `points` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `users_db`
--

INSERT INTO `users_db` (`nom`, `prenom`, `mail`, `motdepasse`, `points`) VALUES
('Dubois', 'Quentin', 'quentin@mail.fr', '$2b$12$UQ6ydVqQV.Jb4SSm1SaCRul2mKThVVpJkYlqMWXjQWkJwFoixtKG2', 2),
('Dupont', 'Sandrine', 'sandrine@bk.fr', '$2b$12$4oGeLx65IO0syUQQyAUeBOXqdZ2CXvwcKbDDN5nVHfAhfJ6b.Uqi6', 0);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `admin_db`
--
ALTER TABLE `admin_db`
  ADD PRIMARY KEY (`mail`);

--
-- Index pour la table `promotions_db`
--
ALTER TABLE `promotions_db`
  ADD PRIMARY KEY (`id_promo`) USING BTREE,
  ADD KEY `fk_restau_promo` (`restaurant`);

--
-- Index pour la table `restaurants_db`
--
ALTER TABLE `restaurants_db`
  ADD PRIMARY KEY (`restaurant`);

--
-- Index pour la table `restaurateurs_db`
--
ALTER TABLE `restaurateurs_db`
  ADD PRIMARY KEY (`mail`),
  ADD KEY `fk_restau` (`nom_restau`);

--
-- Index pour la table `users_db`
--
ALTER TABLE `users_db`
  ADD PRIMARY KEY (`mail`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `promotions_db`
--
ALTER TABLE `promotions_db`
  MODIFY `id_promo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `promotions_db`
--
ALTER TABLE `promotions_db`
  ADD CONSTRAINT `fk_restau_promo` FOREIGN KEY (`restaurant`) REFERENCES `restaurants_db` (`restaurant`);

--
-- Contraintes pour la table `restaurateurs_db`
--
ALTER TABLE `restaurateurs_db`
  ADD CONSTRAINT `fk_restau` FOREIGN KEY (`nom_restau`) REFERENCES `restaurants_db` (`restaurant`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
