package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
)

type robot struct {
	x  int
	y  int
	vx int
	vy int
}

type xy struct {
	x int
	y int
}

func main() {
	fmt.Println("AoC 2024 Day 14")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	answer_1 := 0
	answer_2 := 0
	width := 101
	height := 103
	// group names not used but I kept them
	re := regexp.MustCompile(`(?P<x>\d{1,5}),(?P<y>\d{1,5})[^=]*=(?P<vx>-?\d{1,5}),(?P<xy>-?\d{1,5})`)
	var robots []robot
	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)
	// Read each line of the file
	for scanner.Scan() {
		line := scanner.Text()
		// Split the line into fields using space as the delimiter
		_s := re.FindStringSubmatch(line)[1:]
		_v := [4]int{}
		for i := range _s {
			_v[i], _ = strconv.Atoi(_s[i])
		}
		robots = append(robots, robot{_v[0], _v[1], _v[2], _v[3]})
	}

	iterations := 100
	p1_positions := make(map[xy]int)
	for _, r := range robots {
		p1_positions[xy{modulo_b(r.x+iterations*r.vx, width), modulo_b(r.y+iterations*r.vy, height)}] += 1
	}
	// now process positons to safety factor
	var q1, q2, q3, q4 int
	for pos, count := range p1_positions {
		if pos.x == width/2 || pos.y == height/2 {
			count = 0
		}
		left := pos.x < width/2
		top := pos.y < height/2
		switch {
		case !left && top:
			q1 += count
		case left && top:
			q2 += count
		case left && !top:
			q3 += count
		case !left && !top:
			q4 += count
		}
	}
	answer_1 = q1 * q2 * q3 * q4
findtree:
	for iter := range math.MaxInt64 {
		p2_positions := make(map[xy]int)
		for i, r := range robots {
			robots[i] = robot{modulo_b(r.x+r.vx, width), modulo_b(r.y+r.vy, height), r.vx, r.vy}
			p2_positions[xy{r.x, r.y}] += 1
		}
		// manually calcuated from visible harmonic clusterings
		if (iter-18)%103 == (iter-77)%101 {
			fmt.Printf("SECONDS: %d\n\n", iter)

			for i := range height {
				for j := range width {
					catch := p2_positions[xy{j, i}]
					if catch == 0 {
						fmt.Print(" ")
					} else {
						fmt.Print("X")
					}
				}
				fmt.Println()
			}
			// by my understanding of time, this should actually be iter + 1
			// seeing as iteration 0 is an elapsed second
			// but AoC did not accept that and they couldnt even show us the tree ahead of time
			answer_2 = iter
			break findtree
		}
	}
	fmt.Printf("P1 %d\n", answer_1)
	fmt.Printf("P2 %d\n", answer_2)
}

// golang modulo returns with sign matching a. for this, we want to match b
func modulo_b(a, b int) int {
	return (a%b + b) % b
}
