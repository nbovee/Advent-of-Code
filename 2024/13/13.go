package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"regexp"
	"sort"
	"strconv"
)

type xy struct {
	x int
	y int
}

type Solution struct {
	a_press int
	b_press int
	score   int
}
type ByScore []Solution

func (a ByScore) Len() int           { return len(a) }
func (a ByScore) Less(i, j int) bool { return a[i].score < a[j].score }
func (a ByScore) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }

func main() {
	fmt.Println("AoC 2024 Day 13")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	answer_1 := 0
	answer_2 := 0
	re_button := regexp.MustCompile(`\+(\d{1,5})`)
	re_prize := regexp.MustCompile(`=(\d{1,9})`)
	A_cost := 3
	B_cost := 1
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// scan 4 is null
		line := scanner.Text()
		button_A := re_button.FindAllStringSubmatch(line, -1)
		scanner.Scan()
		line = scanner.Text()
		button_B := re_button.FindAllStringSubmatch(line, -1)
		scanner.Scan()
		line = scanner.Text()
		prize := re_prize.FindAllStringSubmatch(line, -1)
		scanner.Scan()

		A_x, _ := strconv.Atoi(button_A[0][1])
		A_y, _ := strconv.Atoi(button_A[1][1])
		B_x, _ := strconv.Atoi(button_B[0][1])
		B_y, _ := strconv.Atoi(button_B[1][1])
		P_x, _ := strconv.Atoi(prize[0][1])
		P_y, _ := strconv.Atoi(prize[1][1])

		// for part 1 we process the naive solution as usual
		A_limit := min(P_x/A_x, P_y/A_y, 100)
		B_limit := min(P_x/B_x, P_y/B_y, 100)
		scores := []Solution{}

		for i := range A_limit {
			for j := range B_limit {
				if A_x*i+B_x*j == P_x && A_y*i+B_y*j == P_y {
					scores = append(scores, Solution{i, j, i*A_cost + j*B_cost})
				}
			}
		}
		sort.Sort(ByScore(scores))
		if len(scores) > 0 {
			answer_1 += scores[0].score
		}

		// in p2 lets just solve with linear algebra (we probably need to use floats  )
		// set up a matrix, check the determinant, and proceed accordingly
		// Px = Ax Bx * Ap
		// Py   Ay By   Bp
		//
		// Px = Ap*Ax + Bp*Bx
		// Py   Ap*Ay + Bp*By
		// The determinant tells us if the matrix is linearly dependant (if a row is some combination of another)
		// For our 2d matrix that is simply Ax*By - Ay*Bx
		// if it is 0, there are multiple solutions and we must use the token costs of a press to find the optimal
		// if it is not 0. there is only one solution and we can solve the system of equations
		offset := 10000000000000
		P_x += offset
		P_y += offset
		var A_p, B_p, r_a, r_b float64
		determinant := float64(A_x)*float64(B_y) - float64(B_x)*float64(A_y)
		if determinant != 0 {
			// system of equations with Cramer's Rule
			detA := float64(P_x)*float64(B_y) - float64(P_y)*float64(B_x)
			detB := float64(A_x)*float64(P_y) - float64(P_x)*float64(A_y)
			A_p = detA / determinant
			B_p = detB / determinant

		} else {
			// find the cheapest solution by comparing our two buttons number of presses and cost
			// how many presses of each would be required?
			_A_p := P_x / A_x
			_B_p := P_x / B_x

			if int(_A_p)*A_cost < int(_B_p)*B_cost {
				A_p = float64(P_x) / float64(A_x)
				B_p = float64(P_x%A_x) / float64(B_x)
			} else {
				A_p = float64(P_x%B_x) / float64(A_x)
				B_p = float64(P_x) / float64(A_x)
			}
		}
		// A_p and B_p are floats, we need to check if they are whole numbers and therefore a valid solution
		// this is simplest with checking with a tolerance, math.Modf() is also a good candidate
		A_p, r_a = math.Modf(A_p)
		B_p, r_b = math.Modf(B_p)
		if A_p >= 0 && B_p >= 0 && r_a == 0 && r_b == 0 {
			answer_2 += int(A_p)*A_cost + int(B_p)*B_cost
		}
	}
	fmt.Printf("P1 %d\n", answer_1)
	fmt.Printf("P2 %d\n", answer_2)
}
