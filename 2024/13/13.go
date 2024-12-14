package main

import (
	"bufio"
	"fmt"
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
		// scan 1 is button A
		// scan 2 is button B
		// scan 3 is prize info
		// scan 4 is null
		line := scanner.Text()
		button_A := re_button.FindAllStringSubmatch(line, -1)
		A_x := atoi(button_A[0][1])
		A_y := atoi(button_A[1][1])
		_ = A_x
		_ = A_y
		scanner.Scan()
		line = scanner.Text()
		button_B := re_button.FindAllStringSubmatch(line, -1)
		B_x := atoi(button_B[0][1])
		B_y := atoi(button_B[1][1])
		_ = B_x
		_ = B_y
		scanner.Scan()
		line = scanner.Text()
		prize := re_prize.FindAllStringSubmatch(line, -1)
		P_x := atoi(prize[0][1])
		P_y := atoi(prize[1][1])
		scanner.Scan()
		// A_limit := min(P_x/A_x, P_y/A_y)
		// B_limit := min(P_x/B_x, P_y/B_y)
		// preferB := A_limit * A_cost > B_limit * B_cost

		// fmt.Printf("With Prize at %d,%d, A+%d,+%d can be pressed up to %d times.\n", P_x, P_y, A_x, A_y, A_limit)
		// fmt.Printf("With Prize at %d,%d, B+%d,+%d can be pressed up to %d times.\n\n", P_x, P_y, B_x, B_y, B_limit)
		// scores := []Solution{}

		// for i := range min(A_limit, 100) {
		// 	for j := range min(B_limit, 100) {
		// 		if A_x*i+B_x*j == P_x && A_y*i+B_y*j == P_y {
		// 			//prize found.
		// 			scores = append(scores, Solution{i, j, i*A_cost + j*B_cost})
		// 		}
		// 	}
		// }
		// sort.Sort(ByScore(scores))
		// if len(scores) > 0 {
		// 	answer_1 += scores[0].score
		// }

		scores := []Solution{}
		offset := 10000000000000
		P_x += offset
		P_y += offset
		// A_limit = min(P_x/A_x, P_y/A_y)
		// B_limit = min(P_x/B_x, P_y/B_y)
		// now that we are in P2 let us do the non-naive solution
		// rather than check if the values of each button appear in the factors of the prize location
		// for P(x,y), both components of at least one button must be in the factors to be worth checking.

		// we can also assume some minimum number of button presses to start the search
		// the prize is un

		// if the remainder of P_x%B_x is not a factor of A_x or 0, that cannot be a solution

		// Button A: X+94, Y+34
		// Button B: X+22, Y+67
		// Prize: X=8400, Y=5400

		// 8400%94 = 12
		//
		// PRIME FACTORIZATION
		for i := range P_x {
			// we can split a prize location into two components, and if both halves can be respectively %==0, than it is a possible split location
			// after we mark it as a candidate, we can test on P_y in the next step.
			if i%A_x == 0 && (P_x-i)%B_x == 0 {
				// find multiples and check y axis
				_a_p := i / A_x
				_b_p := (P_x - i) / B_x
				if _a_p*A_y+_b_p*B_y == P_y {
					// solution found
					scores = append(scores, Solution{_a_p, _b_p, _a_p*A_cost + _b_p*B_cost})
				}
			}

			sort.Sort(ByScore(scores))
			if len(scores) > 0 {
				answer_2 += scores[0].score
			}

		}
		fmt.Printf("P1 %d\n", answer_1)
		fmt.Printf("P2 %d\n", answer_2)

	}
}

func atoi(s string) int {
	r, _ := strconv.Atoi(s)
	return r
}
