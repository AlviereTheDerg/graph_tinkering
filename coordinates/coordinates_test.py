
import unittest
from coordinates.coordinates import *

class zero_pad_test(unittest.TestCase):
    def test_empty_tuple(self):
        self.assertEqual(zero_pad(tuple(),2), (0,0))

    def test_shorter_tuple(self):
        self.assertEqual(zero_pad((1,),2), (1,0))
    
    def test_exact_length_tuple(self):
        self.assertEqual(zero_pad((1,2),2), (1,2))
    
    def test_too_long_tuple(self):
        self.assertEqual(zero_pad((1,2,3),2), (1,2))
    
    def test_impossible_short_length(self):
        self.assertEqual(zero_pad((1,2,3),-4), tuple())
    
    def test_absurdly_long_length(self):
        self.assertEqual(zero_pad((1,2,3),8000), tuple(i if i <= 3 else 0 for i in range(1,8001)))

class length_match_test(unittest.TestCase):
    def test_one_coord_default_length(self):
        self.assertEqual(length_match([(6,2)]), [(6,2)])
    
    def test_one_coord_shorter_length(self):
        self.assertEqual(length_match([(6,2)], length=1), [(6,)])
    
    def test_one_coord_longer_length(self):
        self.assertEqual(length_match([(6,2)], length=4), [(6,2,0,0)])
    
    def test_two_same_coords_default_length(self):
        self.assertEqual(length_match([(6,2),(3,1)]), [(6,2),(3,1)])
    
    def test_two_same_coords_shorter_length(self):
        self.assertEqual(length_match([(6,2),(3,1)], length=1), [(6,),(3,)])
    
    def test_two_same_coords_longer_length(self):
        self.assertEqual(length_match([(6,2),(3,1)], length=3), [(6,2,0),(3,1,0)])
    
    def test_three_diff_coords_default_length(self):
        self.assertEqual(length_match([(6,2,5),(3,),(8,4)]), [(6,2,5),(3,0,0),(8,4,0)])
    
    def test_three_diff_coords_shorter_length(self):
        self.assertEqual(length_match([(6,2,5),(3,),(8,4)], length=1), [(6,),(3,),(8,)])
    
    def test_three_diff_coords_longer_length(self):
        self.assertEqual(length_match([(6,2,5),(3,),(8,4)], length=5), [(6,2,5,0,0),(3,0,0,0,0),(8,4,0,0,0)])

class distance_between_test(unittest.TestCase):
    #manhattan distances
    def test_manhattan_identical_coords_unnamed(self):
        self.assertAlmostEqual(distance_between((5,2),(5,2),1), 0)

    def test_manhattan_identical_coords_named(self):
        self.assertAlmostEqual(distance_between((5,2),(5,2),L=1), 0)
        
    def test_manhattan_diff_coords_unnamed(self):
        self.assertAlmostEqual(distance_between((5,2),(6,5),1), 4)

    def test_manhattan_diff_coords_named(self):
        self.assertAlmostEqual(distance_between((5,2),(6,5),L=1), 4)
        
    def test_manhattan_diff_len_coords_unnamed(self):
        self.assertAlmostEqual(distance_between((5,2,4),(6,5),1), 8)

    def test_manhattan_diff_len_coords_named(self):
        self.assertAlmostEqual(distance_between((5,2,4),(6,5),L=1), 8)
    
    #euclidean distances
    def test_euclidean_identical_coords_unnamed(self):
        self.assertAlmostEqual(distance_between((5,2),(5,2),2), 0)

    def test_euclidean_identical_coords_named(self):
        self.assertAlmostEqual(distance_between((5,2),(5,2),L=2), 0)
        
    def test_euclidean_diff_coords_unnamed(self):
        self.assertAlmostEqual(distance_between((5,2),(6,5),2), 10**(1/2))

    def test_euclidean_diff_coords_named(self):
        self.assertAlmostEqual(distance_between((5,2),(6,5),L=2), 10**(1/2))
        
    def test_euclidean_diff_len_coords_unnamed(self):
        self.assertAlmostEqual(distance_between((5,2,4),(6,5),2), 26**(1/2))

    def test_euclidean_diff_len_coords_named(self):
        self.assertAlmostEqual(distance_between((5,2,4),(6,5),L=2), 26**(1/2))

class sum_coords_test(unittest.TestCase):
    def test_two_same_length_coords(self):
        self.assertEqual(sum_coords((4,3),(1,6)), (5,9))

    def test_two_diff_length_coords(self):
        self.assertEqual(sum_coords((4,),(1,6)), (5,6))

    def test_one_empty(self):
        self.assertEqual(sum_coords((4,),tuple(),(1,6)), (5,6))

class scale_coord_test(unittest.TestCase):
    def test_empty_tuple(self):
        self.assertEqual(scale_coord(tuple(), 1), tuple())
        
    def test_non_empty_tuple(self):
        self.assertEqual(scale_coord((5,3,1), 3), (15,9,3))

class cosine_of_test(unittest.TestCase):
    def test_2d_right_triangle_90(self):
        self.assertAlmostEqual(cosine_of((0,0),(1,0),(0,1)), 0, msg="up right")
        self.assertAlmostEqual(cosine_of((0,0),(-1,0),(0,1)), 0, msg="down right")
        self.assertAlmostEqual(cosine_of((0,0),(1,0),(0,-1)), 0, msg="up left")
        self.assertAlmostEqual(cosine_of((0,0),(-1,0),(0,-1)), 0, msg="down left")

    def test_2d_right_triangle_45(self):
        self.assertAlmostEqual(cosine_of((0,0),(1,0),(1,1)), (1/2)**(1/2), msg="up right")
        self.assertAlmostEqual(cosine_of((0,0),(1,0),(1,-1)), (1/2)**(1/2), msg="down right")
        self.assertAlmostEqual(cosine_of((0,0),(-1,0),(-1,1)), (1/2)**(1/2), msg="up left")
        self.assertAlmostEqual(cosine_of((0,0),(-1,0),(-1,-1)), (1/2)**(1/2), msg="down left")

    def test_2d_obtuse_triangle_135(self):
        self.assertAlmostEqual(cosine_of((0,0),(1,0),(-1,1)), -(1/2)**(1/2), msg="up right")
        self.assertAlmostEqual(cosine_of((0,0),(1,0),(-1,-1)), -(1/2)**(1/2), msg="down right")
        self.assertAlmostEqual(cosine_of((0,0),(-1,0),(1,1)), -(1/2)**(1/2), msg="up left")
        self.assertAlmostEqual(cosine_of((0,0),(-1,0),(1,-1)), -(1/2)**(1/2), msg="down left")

    def test_3d_right_triangle_90(self):
        self.assertAlmostEqual(cosine_of((0,0,0), (0,0,1), (1,1,0)), 0, msg="Coords typed out")
        self.assertAlmostEqual(cosine_of(tuple(), (0,0,1), (1,1,0)), 0, msg="tuple() origin")
        self.assertAlmostEqual(cosine_of(tuple(), (0,0,1), (1,1)), 0, msg="tuple() origin, truncated XY")

    def test_2d_line(self):
        self.assertAlmostEqual(cosine_of(tuple(),(1,),(-1,)), -1, msg="Straight line: cos(180)")