#!/bin/bash

# Nom de l'exécutable
EXECUTABLE_NAME="agent"
EXECUTABLE_DEST="$HOME/.agent_collector/$EXECUTABLE_NAME"

# Nom du fichier de service
SERVICE_NAME="agent_collector.service"

# Chemin du répertoire de données
DATA_DIR="$HOME/.agent_collector/data"

# Contenu du fichier de service avec journalisation
SERVICE_CONTENT="[Unit]
Description=Agent Collector Daemon
After=network.target

[Service]
ExecStart=$EXECUTABLE_DEST
StandardOutput=append:$HOME/.agent_collector/agent.log
StandardError=append:$HOME/.agent_collector/agent.log
Restart=always

[Install]
WantedBy=multi-user.target
"

# Vérifier si l'exécutable existe dans le répertoire actuel
if [ ! -f "$EXECUTABLE_NAME" ]; then
    echo "Erreur : L'exécutable $EXECUTABLE_NAME n'existe pas dans le répertoire actuel."
    exit 1
fi

# Créer le répertoire de destination s'il n'existe pas
mkdir -p "$HOME/.agent_collector"

# Déplacer l'exécutable vers le répertoire de destination
echo "Déplacement de l'exécutable vers $EXECUTABLE_DEST..."
cp "$EXECUTABLE_NAME" "$EXECUTABLE_DEST"
chmod +x "$EXECUTABLE_DEST"

# Créer le répertoire de données s'il n'existe pas
sudo chown -hR $USER "$HOME/.agent_collector"
mkdir "/$HOME/.agent_collector/data"

# Créer le fichier de service
echo "Création du fichier de service $SERVICE_NAME..."
echo "$SERVICE_CONTENT" | sudo tee /etc/systemd/system/$SERVICE_NAME > /dev/null

# Recharger systemd
echo "Rechargement de systemd..."
sudo systemctl daemon-reload

# Activer et démarrer le service
echo "Activation et démarrage du service..."
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "Installation terminée. Vérifiez le statut du service avec : sudo systemctl status $SERVICE_NAME"
echo "Les logs sont disponibles dans : $HOME/.agent_collector/agent.log"
