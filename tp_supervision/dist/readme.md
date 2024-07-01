# TP d'INF4218 Systèmes Distribués

Ceci est l'agent de collecte de la quantité de ressources utilisées sur une machine Linux. Il collecte périodiquement des informations sur le CPU, la RAM, le cache, la température, l'état de la batterie, le débit entrant et sortant de l'interface réseau, ainsi que d'autres ressources additionnelles.

## Objectifs

- **Surveillance des ressources** : Fournir une solution de surveillance des ressources système en temps réel.
- **Optimisation des performances** : Aider à l'identification des goulots d'étranglement et à l'optimisation des performances système.
- **Facilité d'utilisation** : Fournir un outil facile à installer et à utiliser pour les administrateurs système.

## Technologies

- **Bash** : Pour les scripts d'installation et de gestion de services.
- **Systemd** : Pour la gestion du service de collecte en arrière-plan.
- **Linux** : Environnement cible pour l'agent de collecte.

## Installation

Suivez les étapes ci-dessous pour installer et configurer l'agent de collecte :

1. **Décompresser l'archive de l'agent :**
    ```bash
    tar -xzf agent_collector.zip
    cd agent_collector
    ```

2. **S'assurer que l'exécutable `agent` est présent dans le répertoire décompressé.**

3. **Exécuter le script d'installation :**
    ```bash
    chmod +x install_deamon.sh
    ./install_deamon.sh
    ```

4. **Vérifier le statut du service :**
    ```bash
    sudo systemctl status agent_collector.service
    ```

5. **Les logs sont disponibles dans :**
    ```bash
    tail -f $HOME/.agent_collector/agent.log
    ```

## License

Ce projet est sous licence MIT. Veuillez consulter le fichier [LICENSE](LICENSE) pour plus de détails.

## Contributeurs

- [ Serge Noah ](https://github.com/SergeNoah000)
- [ TOKO Bonice ](https://github.com/jbbonice2)
- [ Kenfact Jaures ](https://github.com/Jaures-ngahou)
- [ Mebenga Jean ](https://github.com/Mebenga1)
- [ Mohammed Ahmed ](https://github.com/mohammed-ainz)

## Remarques

Pour toute question ou problème, veuillez ouvrir une issue sur le [dépôt GitHub](https://github.com/jbbonice2/TP_surveillance_reseau.git).
