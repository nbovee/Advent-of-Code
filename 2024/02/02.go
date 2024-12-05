package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("AoC 2024 Day 2")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)

	// Control values
	passing := 0
	passing_damped := 0

	// Read each line of the file
	for scanner.Scan() {

		// Split the line into fields using space as the delimiter
		line := scanner.Text()

		fields := strings.Fields(line)
		report := reportInInt(fields)
		valid, damp := validateReport(report)

		if valid {
			passing += 1
			passing_damped += 1
		} else {
			// Since the index
			valid_0, _ := validateReport(prune(report, damp))
			valid_1, _ := validateReport(prune(report, damp-1))
			valid_2, _ := validateReport(prune(report, damp-2))

			valid = valid_0 || valid_1 || valid_2
			if valid {
				passing_damped += 1
			}
		}
		if !valid {
			fmt.Printf("Failed 3x %v\n", report)
		}
	}

	// Print the resulting array
	fmt.Print("P1: ")
	fmt.Println(passing)
	fmt.Print("P2: ")
	fmt.Println(passing_damped)

}

func reportInInt(report []string) []int {
	var converted []int
	for _, field := range report {
		val, err := strconv.Atoi(field)
		converted = append(converted, val)
		if err != nil {
			panic(err)
		}
	}
	return converted
}

func validateReport(report []int) (bool, int) {
	// Simply ignoring a single validity error doesnt work, in case that error set direction in base case
	// For logical, if not programming simplicity, lets simply reslice without the offending value
	type result struct {
		valid bool
		index int
	}
	valid := result{true, 0}
	limit := 3
	direction := true

val_loop:
	for i := 1; i < len(report); i++ {
		step := float64(report[i] - report[i-1])
		control := int(math.Abs(step))
		// fmt.Printf("%+2.f ", step)
		switch {
		case control <= limit && control != 0:
			// in safe band, check direction
			sign := math.Signbit(step)
			if i == 1 {
				direction = sign
			}

			if sign != direction {
				valid = result{false, i}
				break val_loop
			}

		default:
			valid = result{false, i}
			break val_loop
		}
	}
	return valid.valid, valid.index
}

func prune(report []int, remove int) []int {
	if remove < 0 {
		return make([]int, 2)
	}
	dupeReport := make([]int, len(report))
	copy(dupeReport, report)
	return append(dupeReport[:remove], dupeReport[remove+1:]...)
}
