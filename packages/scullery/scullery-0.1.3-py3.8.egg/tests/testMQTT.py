import unittest
import time
import scullery.mqtt 


class VirtualServer(unittest.TestCase):
    def test_loop(self):
        d = [0]
        def p(*x):
            d[0]=1
            
        c = scullery.mqtt.getConnection("__virtual__","foo")
        
        c.subscribe("test", p)
        
        c.publish("test","someData")
        
        time.sleep(0.2)
        
        self.assertEqual(d[0], 1)
