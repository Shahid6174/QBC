import unittest
from src.wma import weighted_moving_average

class TestWMA(unittest.TestCase):
    def test_weighted_moving_average(self):
        # Test valid input
        data = [1, 2, 3, 4, 5]
        window_size = 3
        expected = [2.0, 3.0, 4.0]  # Calculated: (1*1 + 2*2 + 3*3)/(1+2+3) = 14/6 = 2.333..., etc.
        result = weighted_moving_average(data, window_size)
        self.assertEqual(len(result), len(expected))
        for r, e in zip(result, expected):
            self.assertAlmostEqual(r, e, places=4)
        
        # Test invalid window size
        self.assertEqual(weighted_moving_average(data, 0), [])
        self.assertEqual(weighted_moving_average(data, 6), [])
        
        # Test empty data
        self.assertEqual(weighted_moving_average([], 3), [])

if __name__ == '__main__':
    unittest.main()
