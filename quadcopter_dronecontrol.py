# Tobias Schwarz
# Stand: 2024-07-26

import time
import telnetlib
import pygame
import threading


class QuadcopterDroneController:

    def _init_(self):
        self.HOST = (
            "192.168.50.32"  # Ersetze dies mit der Adresse deines Telnet-Servers
        )
        self.PORT = (
            23  # Standard-Telnet-Port, ändere dies entsprechend deiner Konfiguration
        )
        print("Connecting to Telnet server...")
        try:
            self.tn = telnetlib.Telnet(
                self.HOST, self.PORT
            )  # Verbindung zum Telnet-Server herstellen
            print("Telnet-Verbindung hergestellt.")
        except Exception as e:
            print(f"Telnet-Verbindung konnte nicht hergestellt werden: {e}")
            self.tn = None

    def up(self):
        if self.tn:
            print("QUADCOPTER GOES UP!")
            self.tn.write("s".encode("ascii") + b"\n")

    def left(self):
        if self.tn:
            print("QUADCOPTER GOES LEFT!")
            self.tn.write("a".encode("ascii") + b"\n")

    def right(self):
        if self.tn:
            print("QUADCOPTER GOES RIGHT!")
            self.tn.write("d".encode("ascii") + b"\n")

    def forward(self):
        if self.tn:
            print("QUADCOPTER GOES FORWARD!")
            self.tn.write("w".encode("ascii") + b"\n")

    def stop(self):
        if self.tn:
            print("QUADCOPTER STOPS.")
            self.tn.write("x".encode("ascii") + b"\n")
