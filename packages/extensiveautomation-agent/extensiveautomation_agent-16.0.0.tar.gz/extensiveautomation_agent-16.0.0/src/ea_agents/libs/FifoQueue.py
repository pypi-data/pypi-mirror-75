#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------
# Copyright (c) 2010-2019 Denis Machard
# This file is part of the extensive automation project
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA
# -------------------------------------------------------------------

"""
Provide a fifo queue
"""

import threading

try:
    import Queue
except ImportError: # support python 3
    import queue as Queue
    
class FifoCallbackThread(threading.Thread):
    """
    Fifo with callback and thread
    """
    def __init__(self):
        """
        Construct a fifo callback function thread
        """
        threading.Thread.__init__(self)
        self.queue = Queue.Queue(0) # FIFO size is infinite 
        self.running = True
        self.event = threading.Event()

    def removeAll(self):
        """
        Remove All
        """
        while not self.queue.empty():
            callback = self.queue.get(False)
            del callback

    def putItem(self, item):
        """
        Adds callback in the queue

        @param callback:
        @type callback:
        """
        self.queue.put( item )
        self.event.set()

    def run(self):
        """
        Main loop
        """
        while self.running: 
            self.event.wait()
            if self.running:
                while not self.queue.empty():
                    try:
                        callback = self.queue.get(False)
                        callback()
                    except Queue.Empty:
                        self.event.clear()
                    except Exception:
                        pass
                self.event.clear()
        self.event.clear()
        self.onStop()

    def onStop(self):
        """
        On stop
        """
        pass

    def stop(self):
        """
        Stops the thread
        """
        self.running = False
        self.event.set()