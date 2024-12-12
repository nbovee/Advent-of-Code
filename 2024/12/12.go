package main

import (
	"bufio"
	"fmt"
	"os"
)

type xy struct {
	x int
	y int
}
type side struct {
	st xy
	sp xy
}

func main() {
	fmt.Println("AoC 2024 Day 12")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	answer_1 := 0
	answer_2 := 0
	y := 0
	m := make(map[xy]rune)
	m_unvisited := make(map[xy]rune)
	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)
	// Read each line of the file
	for scanner.Scan() {
		line := scanner.Text()
		// Split the line into fields using space as the delimiter
		for x, val := range line {
			// Enter into map
			m[xy{x, y}] = val
			m_unvisited[xy{x, y}] = val
		}
		y++
	}
	for _xy, char := range m {
		if m_unvisited[_xy] == 0 {
			continue
		}
		score_p1, score_p2 := evaluateRegion(m, m_unvisited, _xy, char)
		answer_1 += score_p1
		answer_2 += score_p2
	}
	fmt.Printf("P1 %d\n", answer_1)
	fmt.Printf("P2 %d\n", answer_2)
}

func evaluateRegion(m map[xy]rune, _m_fresh map[xy]rune, _loc xy, plant rune) (int, int) {
	region := make(map[xy]rune)
	_findRegion(_m_fresh, region, _loc, plant)
	area := len(region)
	perimeter := scoreRegionPerimeter(m, region, plant)
	side_score, _ := calculateSides(m, region, plant)
	// fmt.Printf("Region of %s, A=%d P=%d S=%d Found\n", string(plant), area, perimeter, side_score)
	// for side, key := range sides {
	// 	fmt.Print(side)
	// 	fmt.Println(key)
	// }
	return area * perimeter, side_score * area
}

func calculateSides(m map[xy]rune, within map[xy]rune, plant rune) (int, map[side]string) {

	sides_found := make(map[side]string)
	// if the plant has four matching neighbors, ignore
	for _xy, _p := range within {
		if scorePlantPerimeter(m, _xy, _p) == 0 {
			continue
		}
		// take a completed region map, and the pristine map
		// if an element in the region map has no different neighbors, no sides are made
		// if a differing neighbor exists, trace the line on x or y between the pair
		// add that side to our map-set
		// rather than track loop around the region, let us instead remove
		// the plant + neighbor pair from further consideration, winnowing the candidates
		// plants that create the same side will simply re-add to our map-set
		_x := _xy.x
		_y := _xy.y

		if m[xy{_x, _y - 1}] != plant {
			// horizontal line above inspected plant
			x_l, y_l, x_h, y_h := sideEndpoints(m, _xy, xy{_x, _y - 1})
			sides_found[side{xy{x_l, y_l}, xy{x_h, y_h}}] = "H^"
		}
		if m[xy{_x, _y + 1}] != plant {
			// horizontal line below inspected plant
			x_l, y_l, x_h, y_h := sideEndpoints(m, _xy, xy{_x, _y + 1})
			sides_found[side{xy{x_l, y_l}, xy{x_h, y_h}}] = "H_"
		}
		if m[xy{_x - 1, _y}] != plant {
			// vertical line left of inspected plant
			x_l, y_l, x_h, y_h := sideEndpoints(m, _xy, xy{_x - 1, _y})
			sides_found[side{xy{x_l, y_l}, xy{x_h, y_h}}] = "|V"
		}
		if m[xy{_x + 1, _y}] != plant {
			// vertical line right of plant
			x_l, y_l, x_h, y_h := sideEndpoints(m, _xy, xy{_x + 1, _y})
			sides_found[side{xy{x_l, y_l}, xy{x_h, y_h}}] = "V|"
		}
	}
	// fmt.Println(sides_found)
	return len(sides_found), sides_found
}

func sideEndpoints(m map[xy]rune, _loc xy, _nei xy) (int, int, int, int) {
	//offset values help us declare the edge position
	// BA
	// AA
	// considering B, we define the left and above sides as 0 offset, and the right and below as 1
	// this can be calculated by checking if the neighbor.x > loc.x, or the same on y
	// at the same time, a side must have a magnitude of at least 1 or it will collide with perpandicular sides
	plant := m[_loc]

	if _loc.y == _nei.y {
		// trace on the y axis (horizontal side)
		// find min y
		min_y := _loc.y
		for m[xy{_nei.x, min_y - 1}] != plant && m[xy{_loc.x, min_y - 1}] == plant {
			min_y--
		}
		//find max y
		max_y := min_y
		for m[xy{_nei.x, max_y + 1}] != plant && m[xy{_loc.x, max_y + 1}] == plant {
			max_y++
		}
		offset := 0
		if _loc.x < _nei.x {
			offset = 1
		}
		return _loc.x + offset, min_y, _loc.x + offset, max_y + 1
	} else {
		// trace on the x axis (vertical side)
		// find min x
		min_x := _loc.x
		for m[xy{min_x - 1, _nei.y}] != plant && m[xy{min_x - 1, _loc.y}] == plant {
			min_x--
		}
		//find max x
		max_x := min_x
		for m[xy{max_x + 1, _nei.y}] != plant && m[xy{max_x + 1, _loc.y}] == plant {
			max_x++
		}
		offset := 0
		if _loc.y < _nei.y {
			offset = 1
		}
		return min_x, _loc.y + offset, max_x + 1, _loc.y + offset
	}
}

func _findRegion(_m_fresh map[xy]rune, within map[xy]rune, _loc xy, plant rune) {
	if _m_fresh[_loc] == plant {
		within[_loc] = plant
		delete(_m_fresh, _loc)
		_findRegion(_m_fresh, within, xy{_loc.x - 1, _loc.y}, plant)
		_findRegion(_m_fresh, within, xy{_loc.x + 1, _loc.y}, plant)
		_findRegion(_m_fresh, within, xy{_loc.x, _loc.y - 1}, plant)
		_findRegion(_m_fresh, within, xy{_loc.x, _loc.y + 1}, plant)
	}
}

func scoreRegionPerimeter(m map[xy]rune, within map[xy]rune, plant rune) int {
	result := 0
	for _xy := range within {
		result += scorePlantPerimeter(m, _xy, plant)
	}
	return result
}

func scorePlantPerimeter(m map[xy]rune, _l xy, plant rune) int {
	_x := _l.x
	_y := _l.y
	result := 0
	if m[xy{_x, _y - 1}] != plant {
		result += 1
	}
	if m[xy{_x, _y + 1}] != plant {
		result += 1
	}
	if m[xy{_x - 1, _y}] != plant {
		result += 1
	}
	if m[xy{_x + 1, _y}] != plant {
		result += 1
	}
	return result
}
