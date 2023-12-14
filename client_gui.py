# client_gui.py

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import scrolledtext
from network import Network
import re


class ClientGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("DiSUcord Client")

        # Server Connection Frame
        connection_frame = ttk.LabelFrame(master, text="Server Connection", padding=10)
        connection_frame.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)

        tk.Label(connection_frame, text="Server:").grid(row=0, column=0, sticky=tk.W)
        self.host_entry = tk.Entry(connection_frame, width=15)
        self.host_entry.grid(row=0, column=1, sticky=tk.W)
        self.host_entry.insert(0, "127.0.0.1")

        tk.Label(connection_frame, text="Port:").grid(row=0, column=2, sticky=tk.W)
        self.port_entry = tk.Entry(connection_frame, width=5)
        self.port_entry.grid(row=0, column=3, sticky=tk.W)
        self.port_entry.insert(0, "8080")

        tk.Label(connection_frame, text="Username:").grid(row=1, column=0, sticky=tk.W)
        self.username_entry = tk.Entry(connection_frame, width=15)
        self.username_entry.grid(row=1, column=1, sticky=tk.W)

        self.connect_button = tk.Button(
            connection_frame, text="Connect", command=self.connect
        )
        self.connect_button.grid(row=1, column=2)
        self.disconnect_button = tk.Button(
            connection_frame,
            text="Disconnect",
            command=self.disconnect,
            state=tk.DISABLED,
        )
        self.disconnect_button.grid(row=1, column=3)

        # Chat Frame
        chat_frame = ttk.LabelFrame(master, text="Chat", padding=10)
        chat_frame.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)

        self.messages_area = scrolledtext.ScrolledText(
            chat_frame, state="disabled", height=15, width=50
        )
        self.messages_area.grid(row=0, column=0, columnspan=4, sticky=tk.EW)

        self.message_entry = tk.Entry(chat_frame, width=40)
        self.message_entry.grid(row=1, column=0, columnspan=3, sticky=tk.EW)
        self.send_button = tk.Button(chat_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=3)

        # Subscription Frame
        subscription_frame = ttk.LabelFrame(
            master, text="Channel Subscriptions", padding=10
        )
        subscription_frame.grid(row=2, column=0, sticky=tk.EW, padx=5, pady=5)

        self.subscribe_button = tk.Button(
            subscription_frame,
            text="Subscribe to IF 100",
            command=lambda: self.subscribe("IF 100"),
        )
        self.subscribe_button.grid(row=0, column=0, columnspan=2, sticky=tk.EW)
        self.unsubscribe_button = tk.Button(
            subscription_frame,
            text="Unsubscribe from IF 100",
            command=lambda: self.unsubscribe("IF 100"),
        )
        self.unsubscribe_button.grid(row=0, column=2, columnspan=2, sticky=tk.EW)

        self.subscribe_sps_button = tk.Button(
            subscription_frame,
            text="Subscribe to SPS 101",
            command=lambda: self.subscribe("SPS 101"),
        )
        self.subscribe_sps_button.grid(row=1, column=0, columnspan=2, sticky=tk.EW)
        self.unsubscribe_sps_button = tk.Button(
            subscription_frame,
            text="Unsubscribe from SPS 101",
            command=lambda: self.unsubscribe("SPS 101"),
        )
        self.unsubscribe_sps_button.grid(row=1, column=2, columnspan=2, sticky=tk.EW)

        # Channel Selector
        tk.Label(subscription_frame, text="Message Channel:").grid(
            row=2, column=0, sticky=tk.W
        )
        self.channels = ["IF 100", "SPS 101"]
        self.selected_channel = tk.StringVar()
        self.channel_selector = ttk.Combobox(
            subscription_frame, textvariable=self.selected_channel
        )
        self.channel_selector["values"] = self.channels
        self.channel_selector.current(0)
        self.channel_selector.grid(row=3, column=0, columnspan=4, sticky=tk.EW)

        self.network = None

    def connect(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        self.network = Network(host, port, self.receive_message, self._disconnect_ui)
        if self.network.connect(username):
            self.messages_area.config(state="normal")
            self.messages_area.insert(tk.END, "Connected to server\n")
            self.messages_area.config(state="disabled")
            # set button states
            self.connect_button["state"] = tk.DISABLED
            self.disconnect_button["state"] = tk.NORMAL
        else:
            self.messages_area.config(state="normal")
            self.messages_area.insert(tk.END, "Failed to connect to server\n")
            self.messages_area.config(state="disabled")
            # set button states
            self.connect_button["state"] = tk.NORMAL
            self.disconnect_button["state"] = tk.DISABLED

    def disconnect(self):
        self._disconnect_ui()
        self.network.disconnect()

    def _disconnect_ui(self):
        self.disconnect_button["state"] = tk.DISABLED
        self.connect_button["state"] = tk.NORMAL

        # indicate connection lost at the logs
        self.messages_area.config(state="normal")
        self.messages_area.insert(tk.END, "Disconnected from server\n")
        self.messages_area.see(tk.END)  # Auto-scroll to the bottom
        self.messages_area.config(state="disabled")

    def send_message(self):
        message = self.message_entry.get()
        channel = self.selected_channel.get()
        self.network.send_message(channel, message)
        self.message_entry.delete(0, tk.END)

    def subscribe(self, channel):
        self.network.subscribe(channel)

    def unsubscribe(self, channel):
        self.network.unsubscribe(channel)

    def receive_message(self, message):
        self.messages_area.config(state="normal")
        self.messages_area.insert(tk.END, message + "\n")
        self.messages_area.see(tk.END)  # Auto-scroll to the bottom
        self.messages_area.config(state="disabled")
