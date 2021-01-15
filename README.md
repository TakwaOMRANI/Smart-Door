De nombreuses implémentations existent dans le monde pour la reconnaissance et la commande vocale. Et dans cette réalité l'interface homme-machine remplit ce rôle, dans ce cadre se situe la réalisation de mon projet dans le cours #système_temps_réel à l'#ENIT.

Ouvrir et fermer la porte de garage en mode Wi-Fi, si vous êtes dans ou près de votre maison.
Par une interface d'entrée d'un système informatique #Application_Android l'utilisateur parle dans le microphone de son téléphone, couplé à l'application qui permet la reconnaissance vocale, analyse  automatique ses paroles #Speech_to_Text et détermine la commande à exécuter et l'envoie par le protocole messagerie #publish_subscribe #MQTT à la carte #Raspberry_pi, pour faire tourner le moteur pas à pas #5V_stepper_motor_4_phase.

Et pour  créer une sorte d'historique de sécurité de la porte, on a utilisé le modèle de données #Cloud_Firestore qui prend en charge de stocker en #temps_réel les commandes d'ouverture, fermeture et arrêt de la porte dans des documents, organisés en collections qui prennent l'action et le temps de commande.
