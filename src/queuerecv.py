import socket
import pickle
import threading
from queue import Queue
import pygame


class QueueRecv:

    def __init__(self, conn):
        self.queue = Queue()
        self.server = conn

        self.recv_thread = threading.Thread(target=self.recv_thread_method)

        self.running = True

    def get_queue(self): return self.queue

    def running(self, state: bool):
        self.queue = state

    def stop(self): self.running = False

    def start_thread(self): self.recv_thread.start()

    def stop_thread(self):
        self.running = False
        self.recv_thread.join()
        print("Thread stop")

    def recv_thread_method(self):
        while self.running:
            try:
                data_recv = self.server.recv(2048)
                #print(data_recv)
                data = pickle.loads(data_recv)  # pickle.loads() recompose l'object
                #print(data)
                # Mettez les données dans la file pour que le thread principal les récupère
                self.queue.put(data)

            except socket.error as e:
                print(e)


