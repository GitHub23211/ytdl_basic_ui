import threading

class SongQueue:
    def __init__(self):
        self.queue = []
        self.song_list = ''
        self.mutex = threading.Lock()
    
    def add(self, song):
        self.mutex.acquire()
        self.queue.append(song)
        self.mutex.release()
    
    def remove(self):
        self.mutex.acquire()
        if(len(self.queue) > 0):
            self.queue.pop(0)
        self.mutex.release()

    def hasNext(self):
        has = False
        self.mutex.acquire()
        has = len(self.queue) > 0
        self.mutex.release()
        return has

    def getAt(self, i):
        return self.queue[i]
    
    def get(self):
        return self.queue
    
    def clear(self):
        self.mutex.acquire()
        self.queue.clear()
        self.mutex.release()

    def to_string(self):
        string = ''
        for i, song in enumerate(self.queue):
            string += str(i) + '. ' + song + "\n"
        return string